from models.chat_message import ChatMessage

from service.memory_service import MemoryService
from service.company_context_service import CompanyContextService
from service.pending_intent_service import PendingIntentService


class ChatService:

    def __init__(self, rag_chain, memory_service: MemoryService):

        self.rag_chain = rag_chain
        self.memory_service = memory_service

        self.company_context = CompanyContextService(memory_service)
        self.pending_service = PendingIntentService()

    def chat(self, session_id: str, question: str) -> str:

        company, detected = self.company_context.resolve_company(
            session_id, question
        )

        # CASE 1: no company yet → store pending question
        if company is None:
            self.pending_service.set(session_id, question)
            return "Which company's privacy policy are you asking about?"

        # CASE 2: pending question exists → combine automatically
        pending = self.pending_service.get(session_id)

        if pending:
            effective_question = f"{company} {pending}"
            self.pending_service.clear(session_id)
        else:
            effective_question = question

        chat_history = self.memory_service.get_langchain_messages(
            session_id=session_id,
            limit=6
        )

        response = self.rag_chain.invoke({
            "question": effective_question,
            "chat_history": chat_history,
            "company": company
        })

        self.memory_service.save_message(
            ChatMessage(session_id, "user", question)
        )

        self.memory_service.save_message(
            ChatMessage(session_id, "assistant", response)
        )

        return response
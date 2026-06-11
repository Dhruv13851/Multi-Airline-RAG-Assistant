from models.chat_message import ChatMessage

from service.memory_service import MemoryService
from service.company_context_service import CompanyContextService
from service.pending_intent_service import PendingIntentService
from service.query_rewriter_service import QueryRewriter


class ChatService:

    def __init__(
        self,
        rag_chain,
        memory_service: MemoryService,
        query_rewriter: QueryRewriter
    ):

        self.rag_chain = rag_chain
        self.memory_service = memory_service
        self.query_rewriter = query_rewriter

        self.company_context = CompanyContextService(
            memory_service
        )

        self.pending_service = PendingIntentService()

    def chat(
        self,
        session_id: str,
        question: str
    ) -> str:

        # -----------------------------
        # Load Chat History
        # -----------------------------

        chat_history = (
            self.memory_service
            .get_langchain_messages(
                session_id=session_id,
                limit=6
            )
        )

        # -----------------------------
        # Rewrite Query
        # -----------------------------

        rewritten_query = (
            self.query_rewriter.rewrite(
                question=question,
                chat_history=chat_history
            )
        )

        print(
            f"\nRewritten Query: "
            f"{rewritten_query}"
        )

        # -----------------------------
        # Detect Companies
        # -----------------------------

        context = (
            self.company_context
            .resolve_context(
                session_id=session_id,
                question=rewritten_query
            )
        )

        print(
            f"\nDetected Companies: "
            f"{context.companies}"
        )

        # -----------------------------
        # Missing Company
        # -----------------------------

        if not context.companies:

            clarification = (
                "Which company's privacy policy "
                "are you asking about?"
            )

            self.pending_service.set(
                session_id=session_id,
                question=question
            )

            self.memory_service.save_message(
                ChatMessage(
                    session_id,
                    "user",
                    question
                )
            )

            self.memory_service.save_message(
                ChatMessage(
                    session_id,
                    "assistant",
                    clarification
                )
            )

            return clarification

        # -----------------------------
        # Pending Intent Recovery
        # -----------------------------

        pending_question = (
            self.pending_service.get(
                session_id
            )
        )

        if pending_question:

            companies_text = ", ".join(
                context.companies
            )

            effective_question = (
                f"{companies_text} "
                f"{pending_question}"
            )

            self.pending_service.clear(
                session_id
            )

        else:

            effective_question = (
                rewritten_query
            )

        print(
            f"\nEffective Query: "
            f"{effective_question}"
        )

        # -----------------------------
        # Invoke RAG
        # -----------------------------

        response = (
            self.rag_chain.invoke(
                {
                    "question": effective_question,
                    "chat_history": chat_history,
                    "companies": context.companies
                }
            )
        )

        # -----------------------------
        # Save Conversation
        # -----------------------------

        self.memory_service.save_message(
            ChatMessage(
                session_id,
                "user",
                question
            )
        )

        self.memory_service.save_message(
            ChatMessage(
                session_id,
                "assistant",
                response
            )
        )

        return response
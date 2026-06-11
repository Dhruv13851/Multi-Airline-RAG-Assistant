# from retrieval.company_detector import CompanyDetector
# from service.memory_service import MemoryService


# class CompanyContextService:

#     def __init__(self, memory_service: MemoryService):
#         self.memory_service = memory_service
#         self.company_detector = CompanyDetector()

#     def resolve_company(self, session_id: str, question: str):

#         detected = self.company_detector.detect(question)

#         if detected:
#             self.memory_service.set_active_company(session_id, detected)
#             return detected, True

#         stored = self.memory_service.get_active_company(session_id)

#         return stored, False
from retrieval.company_detector import (
    CompanyDetector
)

from service.memory_service import (
    MemoryService
)

from models.conversation_context import (
    ConversationContext
)


class CompanyContextService:

    def __init__(
        self,
        memory_service: MemoryService
    ):
        self.memory_service = memory_service
        self.company_detector = CompanyDetector()

    def resolve_context(
        self,
        session_id: str,
        question: str
    ) -> ConversationContext:

        context = (
            self.memory_service
            .get_context(session_id)
        )

        detected = (
            self.company_detector
            .detect_all(question)
        )

        if detected:

            context.companies = detected

            self.memory_service.save_context(
                session_id,
                context
            )

        return context
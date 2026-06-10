class PendingIntentService:

    def __init__(self):
        self._pending_question: dict[str, str] = {}

    def set(self, session_id: str, question: str) -> None:
        self._pending_question[session_id] = question

    def get(self, session_id: str) -> str | None:
        return self._pending_question.get(session_id)

    def clear(self, session_id: str) -> None:
        self._pending_question.pop(session_id, None)
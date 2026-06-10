from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from database.sqlite_manager import SQLiteManager
from models.chat_message import ChatMessage


class MemoryService:

    def __init__(self):
        self.db = SQLiteManager()

        self._active_companies: dict[str, str] = {}

    # ---------------- DB CHAT MEMORY ----------------

    def save_message(self, message: ChatMessage) -> None:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO messages (session_id, role, content)
                VALUES (?, ?, ?)
                """,
                (message.session_id, message.role, message.content)
            )
            conn.commit()

    def get_last_messages(self, session_id: str, limit: int = 6):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT session_id, role, content
                FROM messages
                WHERE session_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (session_id, limit)
            )
            rows = cursor.fetchall()

        messages = [
            ChatMessage(r[0], r[1], r[2]) for r in rows
        ]

        return list(reversed(messages))

    def get_langchain_messages(self, session_id: str, limit: int = 6) -> list[BaseMessage]:
        messages = self.get_last_messages(session_id, limit)

        history = []
        for m in messages:
            if m.role == "user":
                history.append(HumanMessage(content=m.content))
            else:
                history.append(AIMessage(content=m.content))

        return history

    # ---------------- COMPANY STATE ----------------

    def set_active_company(self, session_id: str, company: str):
        self._active_companies[session_id] = company

    def get_active_company(self, session_id: str):
        return self._active_companies.get(session_id)

    def clear_active_company(self, session_id: str):
        self._active_companies.pop(session_id, None)
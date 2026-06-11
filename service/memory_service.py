from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from database.sqlite_manager import SQLiteManager
from models.chat_message import ChatMessage
from models.conversation_context import (
    ConversationContext
)

class MemoryService:

    def __init__(self):
        self.db = SQLiteManager()
        self._contexts: dict[
            str,
            ConversationContext
        ] = {}

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
    
    def get_context(
        self,
        session_id: str
    ) -> ConversationContext:

        return self._contexts.get(
            session_id,
            ConversationContext()
        )


    def save_context(
        self,
        session_id: str,
        context: ConversationContext
    ):

        self._contexts[session_id] = context
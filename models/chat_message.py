from dataclasses import dataclass
from datetime import datetime


@dataclass
class ChatMessage:

    session_id: str

    role: str

    content: str

    created_at: datetime | None = None
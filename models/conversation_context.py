from dataclasses import dataclass, field


@dataclass
class ConversationContext:

    companies: list[str] = field(
        default_factory=list
    )
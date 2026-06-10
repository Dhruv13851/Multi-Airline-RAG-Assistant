from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser

from prompts.Query_rewriter import (
    QUERY_REWRITER_PROMPT
)


class QueryRewriter:

    def __init__(
        self,
        llm
    ):

        self.chain = (
            QUERY_REWRITER_PROMPT
            | llm
            | StrOutputParser()
        )

    def rewrite(
        self,
        question: str,
        chat_history: list[BaseMessage]
    ) -> str:

        return self.chain.invoke(
            {
                "question": question,
                "chat_history": chat_history
            }
        )
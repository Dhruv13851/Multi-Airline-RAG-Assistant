from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

from prompts.chatbot_prompt import CHATBOT_PROMPT
from chatbot.utils import format_docs

from service.query_rewriter_service import QueryRewriter
from retrieval.filtered_retriever import FilteredRetriever


def build_rag_chain(vector_store, llm):

    query_rewriter = QueryRewriter(llm=llm)
    retriever = FilteredRetriever(vector_store)

    def rewrite(inputs):

        rewritten = query_rewriter.rewrite(
            question=inputs["question"],
            chat_history=inputs["chat_history"]
        )

        return {
            **inputs,
            "rewritten_query": rewritten
        }

    def retrieve(inputs):

        docs = retriever.retrieve(
            query=inputs["rewritten_query"],
            company=inputs.get("company"),
            k=5
        )

        return {
            **inputs,
            "context": format_docs(docs)
        }

    chain = (
        RunnableLambda(rewrite)
        | RunnableLambda(retrieve)
        | CHATBOT_PROMPT
        | llm
        | StrOutputParser()
    )

    return chain
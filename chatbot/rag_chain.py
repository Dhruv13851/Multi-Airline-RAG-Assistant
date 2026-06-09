# from langchain_core.runnables import RunnableLambda
# from langchain_core.output_parsers import StrOutputParser

# from prompts.chatbot_prompt import CHATBOT_PROMPT
# from retrieval.filtered_retriever import retrieve_documents
# from chatbot.utils import format_docs


# def build_rag_chain(vector_store, llm):

#     def prepare_question(question):

#         return {
#             "question": question
#         }

#     def retrieve_context(inputs):

#         query = inputs["question"]

#         docs = retrieve_documents(
#             query=query,
#             vector_store=vector_store,
#             k=5
#         )

#         return {
#             "question": query,
#             "context": format_docs(docs)
#         }

#     prepare_question_step = RunnableLambda(
#         prepare_question
#     ).with_config(
#         {"run_name": "Prepare Question"}
#     )

#     retrieve_step = RunnableLambda(
#         retrieve_context
#     ).with_config(
#         {"run_name": "Retrieve Documents"}
#     )

#     output_parser = StrOutputParser().with_config(
#         {"run_name": "Parse Output"}
#     )

#     chain = (
#         prepare_question_step
#         | retrieve_step
#         | CHATBOT_PROMPT
#         | llm
#         | output_parser
#     ).with_config(
#         {"run_name": "Privacy Policy RAG Chain"}
#     )

#     return chain

from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser

from prompts.chatbot_prompt import CHATBOT_PROMPT
from retrieval.filtered_retriever import retrieve_documents
from chatbot.utils import format_docs
from service.query_rewriter_service import QueryRewriter


def build_rag_chain(vector_store, llm):

    query_rewriter = QueryRewriter(llm)

    def prepare_question(question):

        return {
            "question": question
        }

    def rewrite_query(inputs):

        rewritten_query = query_rewriter.rewrite(
            inputs["question"]
        )

        return {
            **inputs,
            "rewritten_query": rewritten_query
        }

    def retrieve_context(inputs):

        docs = retrieve_documents(
            query=inputs["rewritten_query"],
            vector_store=vector_store,
            k=5
        )

        return {
            "question": inputs["question"],
            "rewritten_query": inputs["rewritten_query"],
            "context": format_docs(docs)
        }

    prepare_question_step = RunnableLambda(
        prepare_question
    ).with_config(
        {"run_name": "Prepare Question"}
    )

    rewrite_query_step = RunnableLambda(
        rewrite_query
    ).with_config(
        {"run_name": "Rewrite Query"}
    )

    retrieve_step = RunnableLambda(
        retrieve_context
    ).with_config(
        {"run_name": "Retrieve Documents"}
    )

    output_parser = StrOutputParser().with_config(
        {"run_name": "Parse Output"}
    )

    chain = (
        prepare_question_step
        | rewrite_query_step
        | retrieve_step
        | CHATBOT_PROMPT
        | llm
        | output_parser
    ).with_config(
        {"run_name": "Privacy Policy RAG Chain"}
    )

    return chain
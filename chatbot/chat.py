import uuid

from retrieval.vector_store import (
    load_vector_store
)

from chatbot.rag_chain import (
    build_rag_chain
)

from service.llm_service import (
    get_llm
)

from service.memory_service import (
    MemoryService
)

from service.chat_service import (
    ChatService
)

from service.query_rewriter_service import (
    QueryRewriter
)


def main():

    print("\nLoading vector store...")
    vector_store = load_vector_store()

    print("Loading LLM...")
    llm = get_llm()

    rag_chain = build_rag_chain(
        vector_store=vector_store,
        llm=llm
    )

    query_rewriter = QueryRewriter(
        llm=llm
    )

    memory_service = MemoryService()

    chat_service = ChatService(
        rag_chain=rag_chain,
        memory_service=memory_service,
        query_rewriter=query_rewriter
    )

    session_id = str(
        uuid.uuid4()
    )

    print(
        "\nChatbot ready! Type 'exit' to quit\n"
    )

    while True:

        question = input(
            "Question: "
        ).strip()

        if question.lower() == "exit":
            break

        if not question:
            continue

        response = chat_service.chat(
            session_id=session_id,
            question=question
        )

        print("\nAnswer:")
        print(response)
        print()


if __name__ == "__main__":
    main()
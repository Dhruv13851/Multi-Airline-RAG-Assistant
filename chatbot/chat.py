from retrieval.vector_store import load_vector_store
from chatbot.rag_chain import build_rag_chain
from service.llm_service import get_llm


def main():

    print("\nLoading vector store...")
    vector_store = load_vector_store()

    print("Loading LLM...")
    llm = get_llm()

    rag_chain = build_rag_chain(
        vector_store=vector_store,
        llm=llm
    )

    print("\nChatbot ready! Type 'exit' to quit\n")

    while True:

        query = input("Question: ")

        if query.lower() == "exit":
            break

        response = rag_chain.invoke(query)

        print("\nAnswer:")
        print(response)
        print()


if __name__ == "__main__":
    main()
from retrieval.company_detector import detect_company


def retrieve_documents(query, vector_store, k=5):

    company = detect_company(query)

    if company:

        print(f"\nDetected Company: {company}")

        docs = vector_store.similarity_search(
            query=query,
            k=k,
            filter={"company": company}
        )

    else:

        print("\nNo company detected")

        docs = vector_store.similarity_search(
            query=query,
            k=k
        )

    return docs
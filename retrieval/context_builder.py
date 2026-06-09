from retrieval.filtered_retriever import retrieve_documents
from retrieval.metadata_filter import build_filter
from retrieval.company_detector import detect_company


def retrieve_context(inputs):
    query = inputs["question"]
    vector_store = inputs["vector_store"]

    # Step 1: detect metadata
    company = detect_company(query)

    # Step 2: build filter
    filter_dict = build_filter(company=company)

    # Step 3: retrieve docs
    docs = retrieve_documents(
        query=query,
        vector_store=vector_store,
        k=10,
        filter_dict=filter_dict
    )

    # Step 4: format context
    context = "\n\n".join(doc.page_content for doc in docs)

    return {
        "question": query,
        "context": context,
        "metadata": {
            "company": company
        }
    }
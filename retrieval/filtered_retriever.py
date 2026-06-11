# class FilteredRetriever:

#     def __init__(self, vector_store):
#         self.vector_store = vector_store

#     def retrieve(self, query: str, company: str | None = None, k: int = 5):

#         if company:
#             print(f"\nUsing Company Filter: {company}")

#             return self.vector_store.similarity_search(
#                 query=query,
#                 k=k,
#                 filter={"company": company}
#             )

#         print("\nNo company filter applied")

#         return self.vector_store.similarity_search(query=query, k=k)
class FilteredRetriever:

    def __init__(
        self,
        vector_store
    ):
        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        companies: list[str],
        k: int = 8
    ):

        if not companies:

            print(
                "\nNo company filter applied"
            )

            return (
                self.vector_store
                .similarity_search(
                    query=query,
                    k=k
                )
            )

        docs = []

        for company in companies:

            print(
                f"\nUsing Company Filter: "
                f"{company}"
            )

            docs.extend(
                self.vector_store
                .similarity_search(
                    query=query,
                    k=k,
                    filter={
                        "company": company
                    }
                )
            )

        return docs
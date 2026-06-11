from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(documents):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=180,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = text_splitter.split_documents(documents)

    return chunks
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader


def load_documents(pdf_dir: str):

    documents = []

    for pdf_file in Path(pdf_dir).glob("*.pdf"):

        company = (
            pdf_file.stem
            .replace("_privacy_policy", "")
            .replace("_", " ")
            .title()
        )

        print(f"Loading {pdf_file.name}")

        loader = PyPDFLoader(str(pdf_file))
        pages = loader.load()

        for page in pages:
            page.metadata["company"] = company
            page.metadata["source_file"] = pdf_file.name
            page.metadata["page"] = page.metadata.get("page", 0)

        documents.extend(pages)

    return documents
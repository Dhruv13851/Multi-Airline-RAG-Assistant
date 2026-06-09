from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from config.settings import Settings


def build_vector_store(chunks):

    print("Loading embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name=Settings.EMBEDDING_MODEL
    )

    print("Creating FAISS index...")

    vector_store = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    print("Saving vector database...")

    vector_store.save_local(
        Settings.VECTOR_DB_PATH
    )

    return vector_store
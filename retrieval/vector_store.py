from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from config.settings import Settings


def load_vector_store():

    embeddings = HuggingFaceEmbeddings(
        model_name=Settings.EMBEDDING_MODEL
    )

    return FAISS.load_local(
        Settings.VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
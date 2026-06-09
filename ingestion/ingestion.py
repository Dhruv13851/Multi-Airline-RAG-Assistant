import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

from langchain_core.runnables import RunnableLambda

from config.settings import Settings

from ingestion.loader import load_documents
from ingestion.chunker import chunk_documents
from ingestion.vector_store import build_vector_store


def log_documents(documents):
    print(f"\nLoaded {len(documents)} pages")
    return documents


def log_chunks(chunks):
    print(f"\nCreated {len(chunks)} chunks")

    if chunks:
        print("\nSample Metadata:")
        print(chunks[0].metadata)

    return chunks


# =========================
# Pipeline Steps
# =========================

load_step = RunnableLambda(load_documents).with_config(
    {"run_name": "Load Documents"}
)

log_documents_step = RunnableLambda(log_documents).with_config(
    {"run_name": "Log Documents"}
)

chunk_step = RunnableLambda(chunk_documents).with_config(
    {"run_name": "Chunk Documents"}
)

log_chunks_step = RunnableLambda(log_chunks).with_config(
    {"run_name": "Log Chunks"}
)

vector_store_step = RunnableLambda(build_vector_store).with_config(
    {"run_name": "Build Vector Store"}
)


# =========================
# LangChain Pipeline
# =========================

ingestion_pipeline = (
    load_step
    | log_documents_step
    | chunk_step
    | log_chunks_step
    | vector_store_step
).with_config(
    {"run_name": "Privacy Policy Ingestion Pipeline"}
)


if __name__ == "__main__":

    print("=" * 60)
    print("Starting Privacy Policy Ingestion Pipeline")
    print("=" * 60)

    ingestion_pipeline.invoke(
        Settings.pdf_dir
    )

    print("\nIngestion completed successfully!")
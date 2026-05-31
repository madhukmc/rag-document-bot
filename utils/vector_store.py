from langchain_community.vectorstores import (
    FAISS
)

VECTOR_DB_PATH = "vectorstore"


def create_vector_store(
    chunks,
    embeddings
):

    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )

    vector_store.save_local(
        VECTOR_DB_PATH
    )

    return vector_store


def load_vector_store(
    embeddings
):

    return FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )


def save_vector_store(
    vector_store
):

    vector_store.save_local(
        VECTOR_DB_PATH
    )


def vector_store_exists():

    import os

    return os.path.exists(
        VECTOR_DB_PATH
    )
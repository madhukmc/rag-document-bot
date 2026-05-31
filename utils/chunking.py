from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)


def create_chunks(
    documents,
    chunk_size=2000,
    chunk_overlap=50
):
    """
    Split documents into smaller chunks
    for embedding and retrieval.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = splitter.split_documents(
        documents
    )

    return chunks
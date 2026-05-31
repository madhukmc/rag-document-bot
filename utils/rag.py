def retrieve_context(
    vector_store,
    question,
    k=3
):
    """
    Retrieve relevant chunks
    from vector database.
    """

    retriever = vector_store.as_retriever(
        search_kwargs={
            "k": k
        }
    )

    docs = retriever.invoke(
        question
    )

    return docs
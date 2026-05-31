from utils.loaders import (
    load_document
)

from utils.chunking import (
    create_chunks
)

from utils.embeddings import (
    get_embeddings
)

from utils.vector_store import (
    create_vector_store
)

from utils.rag import (
    retrieve_context
)

from utils.semantic_cache import (
    get_cached_answer,
    add_to_cache
)

from utils.llm import (
    generate_response
)

from prompts.rag_prompt import (
    RAG_PROMPT
)


def process_document(
    uploaded_file
):
    """
    Single file processing
    """

    docs = load_document(
        uploaded_file
    )

    chunks = create_chunks(
        docs
    )

    embeddings = get_embeddings()

    vector_store = create_vector_store(
        chunks,
        embeddings
    )

    return vector_store


def process_documents(
    uploaded_files
):
    """
    Multiple file processing
    """

    all_docs = []

    for file in uploaded_files:

        docs = load_document(
            file
        )

        all_docs.extend(
            docs
        )

    chunks = create_chunks(
        all_docs
    )

    embeddings = get_embeddings()

    vector_store = create_vector_store(
        chunks,
        embeddings
    )

    return vector_store


def generate_answer(
    vector_store,
    question
):
    """
    Complete RAG Pipeline
    """

    # Semantic Cache
    cached_answer = get_cached_answer(
        question
    )

    if cached_answer:

        return cached_answer

    # Retrieval
    retrieved_docs = retrieve_context(
        vector_store,
        question
    )

    context = "\n\n".join(
        [
            doc.page_content
            for doc in retrieved_docs
        ]
    )

    # Prompt
    prompt = RAG_PROMPT.format(
        context=context,
        question=question
    )

    # LLM
    answer = generate_response(
        prompt
    )

    # Cache Save
    add_to_cache(
        question,
        answer
    )

    return answer
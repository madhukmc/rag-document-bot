from sentence_transformers import (
    SentenceTransformer
)

from sklearn.metrics.pairwise import (
    cosine_similarity
)

from functools import (
    lru_cache
)

import numpy as np


@lru_cache(maxsize=1)
def get_model():

    return SentenceTransformer(
        "all-MiniLM-L6-v2"
    )


model = get_model()


# Cache Storage
cache_questions = []

cache_answers = []

cache_embeddings = []


def get_cached_answer(
    question,
    threshold=0.85
):
    """
    Check semantic similarity
    with cached questions.
    """

    if len(cache_questions) == 0:

        return None

    question_embedding = model.encode(
        [question]
    )

    similarities = cosine_similarity(
        question_embedding,
        cache_embeddings
    )[0]

    best_index = np.argmax(
        similarities
    )

    best_score = similarities[
        best_index
    ]

    if best_score >= threshold:

        print(
            f"Semantic Cache Hit: {best_score:.2f}"
        )

        return cache_answers[
            best_index
        ]

    return None


def add_to_cache(
    question,
    answer
):
    """
    Save Question + Answer
    + Embedding
    """

    cache_questions.append(
        question
    )

    cache_answers.append(
        answer
    )

    cache_embeddings.append(
        model.encode(
            question
        )
    )


def clear_cache():
    """
    Clear Cache
    """

    cache_questions.clear()

    cache_answers.clear()

    cache_embeddings.clear()


def cache_size():
    """
    Cache Count
    """

    return len(
        cache_questions
    )


def show_cache():
    """
    Debug Function
    """

    return {

        "questions":
        cache_questions,

        "answers":
        cache_answers

    }
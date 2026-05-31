from langchain_google_genai import (
    ChatGoogleGenerativeAI
)

_llm = None


def get_llm():

    global _llm

    if _llm is None:

        _llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.3
        )

    return _llm


def generate_response(
    prompt
):

    llm = get_llm()

    response = llm.invoke(
        prompt
    )

    return response.content
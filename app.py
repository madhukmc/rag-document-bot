

import streamlit as st
from dotenv import load_dotenv

from services.rag_service import (
    process_documents,
    generate_answer
)
st.write("Secrets:", list(st.secrets.keys()))
load_dotenv()

st.set_page_config(
    page_title="RAG Chat",
    page_icon="📄",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #0f1117;
    color: #e2e8f0;
}

section[data-testid="stSidebar"] {
    background: #1a1d27 !important;
    border-right: 1px solid #2d3148 !important;
}

div[data-testid="stFileUploader"] {
    background: #1a1d27 !important;
    border: 1.5px dashed #3d4263 !important;
    border-radius: 12px !important;
}

div[data-testid="stChatInput"] textarea {
    background: #1a1d27 !important;
    color: #e2e8f0 !important;
}

div[data-testid="stButton"] > button {
    width: 100% !important;
    background: #2d1f1f !important;
    color: #f87171 !important;
    border: 1px solid #4a2020 !important;
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# Session State
for k, v in [
    ("messages", []),
    ("vector_store", None),
    ("current_file", "")
]:
    if k not in st.session_state:
        st.session_state[k] = v

ss = st.session_state

# Sidebar
with st.sidebar:

    st.markdown(
        "### 📄 RAG Chat"
    )

    st.divider()

    if ss.current_file:

        st.success(
            f"📎 {ss.current_file}"
        )

    user_qs = [
        m
        for m in ss.messages
        if m["role"] == "user"
    ]

    if user_qs:

        st.markdown(
            "**History**"
        )

        for i, m in enumerate(
            user_qs
        ):

            st.caption(
                f"Q{i+1}: {m['content'][:55]}"
                f"{'…' if len(m['content']) > 55 else ''}"
            )

        st.divider()

        if st.button(
            "🗑️ Clear"
        ):

            ss.messages = []

            st.rerun()

    else:

        st.caption(
            "No questions yet."
        )

# Main
st.markdown(
    "## 📚 Multi-Document RAG Assistant"
)

uploaded = st.file_uploader(
    "Upload documents",
    type=[
        "pdf",
        "csv",
        "txt",
        "json",
        "docx",
        "xlsx",
        "png",
        "jpg",
        "jpeg"
    ],
    accept_multiple_files=True
)

if len(uploaded) == 0:

    st.info(
        "⬆️ Upload document(s) to start chatting."
    )

    st.stop()

try:

    current_names = "|".join(
        [
            file.name
            for file in uploaded
        ]
    )

    if (
        ss.current_file
        != current_names
    ):

        with st.spinner(
            "Processing documents..."
        ):

            ss.vector_store = (
                process_documents(
                    uploaded
                )
            )

            ss.current_file = (
                current_names
            )

        st.success(
            f"✅ Ready — {len(uploaded)} file(s)"
        )

    for msg in ss.messages:

        with st.chat_message(
            msg["role"]
        ):

            st.markdown(
                msg["content"]
            )

    question = st.chat_input(
        "Ask anything about your document..."
    )

    if question:

        ss.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message(
            "user"
        ):

            st.markdown(
                question
            )

        with st.chat_message(
            "assistant"
        ):

            with st.spinner(
                "Thinking..."
            ):

                answer = generate_answer(
                    ss.vector_store,
                    question
                )

            st.markdown(
                answer
            )

        ss.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

except Exception as e:

    st.error(
        f"⚠️ {str(e)}"
    )
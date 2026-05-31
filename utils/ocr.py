import streamlit as st
import easyocr

@st.cache_resource
def get_reader():

    return easyocr.Reader(
        ["en"],
        gpu=False
    )

def extract_text_from_image(
    image_path
):

    reader = get_reader()

    result = reader.readtext(
        image_path,
        detail=0
    )

    return " ".join(result)
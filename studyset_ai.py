import openai
import streamlit as st
import fitz  # PyMuPDF
import os

# 🔑 Add your OpenAI API Key here (you'll get it from https://platform.openai.com)
openai.api_key = st.secrets["openai_api_key"]


def extract_text(pdf_file):
    doc = fitz.open(streamlit_pdf.name)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def generate_study_material(text):
    prompt = f"""
    Summarize the following chapter:\n{text}

    Output format:
    - Key bullet notes
    - 5 MCQs with 4 options and correct answers
    - 5 flashcards (Q&A format)
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

st.title("📘 StudySet AI - Notes, MCQs & Flashcards Generator")
streamlit_pdf = st.file_uploader("📤 Upload your chapter PDF", type="pdf")

if streamlit_pdf:
    st.info("📖 Reading your file...")
    text = extract_text(streamlit_pdf)
    st.success("✅ Done reading PDF!")

    st.info("⚡ Generating StudySet with AI...")
    study_material = generate_study_material(text)

    st.text_area("📚 Your Study Material", study_material, height=400)

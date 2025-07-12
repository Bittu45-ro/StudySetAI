from fpdf import FPDF
import base64
import openai
import streamlit as st
import fitz
import os

import streamlit as st

st.set_page_config(page_title="StudySet AI")

st.markdown(
    """
    <meta name="google-site-verification" content="3nUbKNy7gdD9QJ-_H2NjrHTj_W5pHf5d-GiVQDz4ft4">
    """,
    unsafe_allow_html=True
)


openai.api_key = st.secrets["openai_api_key"]


def extract_text(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
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
def create_pdf(answer_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Split the AI-generated text into lines and write to PDF
    for line in answer_text.split('\n'):
        pdf.multi_cell(0, 10, line)

    pdf.output("studyset_output.pdf")

    with open("studyset_output.pdf", "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")

    return base64_pdf

st.title("📘 StudySet AI - Notes, MCQs & Flashcards Generator")
streamlit_pdf = st.file_uploader("📤 Upload your chapter PDF", type="pdf")

if streamlit_pdf:
    st.info("📖 Reading your file...")
    text = extract_text(streamlit_pdf)
    st.success("✅ Done reading PDF!")

    st.info("⚡ Generating StudySet with AI...")
    study_material = generate_study_material(text)

    st.text_area("📚 Your Study Material", study_material, height=400)
    st.markdown("---")
    st.write("📥 Download your StudySet as a PDF:")

    base64_pdf = create_pdf(study_material)
    download_link = f'<a href="data:application/pdf;base64,{base64_pdf}" download="StudySet_AI_Notes.pdf">📄 Click here to download PDF</a>'
    st.markdown(download_link, unsafe_allow_html=True)

import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import PyPDF2 as pdf

# Load environment variables from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini response function
def gemini_response(input):
    model = genai.GenerativeModel("gemini-1.5-pro-002")
    response = model.generate_content(input)
    return response.text

# PDF to text
def pdf_to_text(file):
    reader = pdf.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Prompt template
input_prompt = """
Hey Act Like a skilled or very experienced ATS(Application Tracking System)
with a deep understanding of tech field, software engineering, data science, data analyst,
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and provide 
the best assistance for improving the resumes. Assign a percentage match based 
on the job description and the missing keywords with high accuracy.
resume:{text}
description:{jd}
"""

# Page settings
st.set_page_config(page_title="AI ATS Resume Evaluator", layout="wide")

# Custom CSS for styling (Experiment 😅)
st.markdown("""
    <style>
        body {
            background-color: #f9f9f9;
            font-family: 'Segoe UI', sans-serif;
        }
        .hero {
            background: linear-gradient(90deg, #6366f1, #8b5cf6);
            padding: 2rem;
            border-radius: 10px;
            text-align: center;
            color: white;
            margin-bottom: 2rem;
        }
        .hero h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        .hero p {
            font-size: 1.2rem;
            margin: 0;
        }
        .footer {
            text-align: center;
            font-size: 0.9rem;
            color: #888;
            padding: 1rem 0;
            margin-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

#added Some CSS for styling😉
st.markdown("""
<div class="hero">
    <h1>🚀 AI-Powered ATS Resume Evaluator</h1>
    <p>Optimize your resume and stand out in tech hiring – with help from Gemini AI</p>
</div>
""", unsafe_allow_html=True)

# Main layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📋 Job Description")
    jd = st.text_area("", placeholder="Paste the job description here...", height=220)

with col2:
    st.subheader("📎 Upload Your Resume (PDF)")
    file = st.file_uploader("", type=["pdf"])
    st.markdown("")

submit = st.button("✅ Evaluate Resume", use_container_width=True)

# Handle submit
if submit:
    if file is not None and jd.strip() != "":
        with st.spinner("🔍 Analyzing your resume..."):
            resume_text = pdf_to_text(file)
            response = gemini_response(input_prompt.format(text=resume_text, jd=jd))

        st.success("✅ Evaluation Complete")
        st.markdown("### 📝 Your Resume Evaluation:")
        st.markdown(response)
    else:
        st.error("Please upload your resume and provide a job description.")

# Footer
st.markdown("""
<div class="footer">
    Created with ❤️ using Streamlit and Gemini AI | © 2025 ATS Evaluator
</div>
""", unsafe_allow_html=True)

import streamlit as st
from backend.parser import extract_text_from_pdf
from backend.score import evaluate_resume
from backend.utils import load_job_description

st.title("AI Resume Screening Agent")

st.write("Upload a resume PDF and compare it with a job description.")

job_description = load_job_description("examples/job_description.txt")

uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

if uploaded_file:
    st.success("Resume uploaded successfully!")

    if st.button("Analyze Resume"):
        with st.spinner("Extracting text..."):
            resume_text = extract_text_from_pdf(uploaded_file)

        with st.spinner("Evaluating using AI..."):
            result = evaluate_resume(resume_text, job_description)

        st.subheader("Resume Score")
        st.write(f"**Match Score:** {result['score']}%")

        st.subheader("Strengths")
        st.write(result["strengths"])

        st.subheader("Weaknesses")
        st.write(result["weaknesses"])

        st.subheader("Final Recommendation")
        st.write(result["recommendation"])

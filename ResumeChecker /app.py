# app.py
import os
import streamlit as st
import pandas as pd
from backend.parser import extract_text_from_upload
from backend.scorer import score_resume_with_openai
from dotenv import load_dotenv

load_dotenv()  # load OPENAI_API_KEY if present in .env

st.set_page_config(page_title="Resume Screening Agent", layout="wide")
st.title("Resume Screening Agent")

st.markdown(
    """
Upload one or more resumes (PDF or TXT) and paste a job description.
The app will call the OpenAI API to extract skills/experience and return
a score (0-100) and short reasoning for each candidate.
"""
)

with st.sidebar:
    st.header("Settings")
    model = st.selectbox("OpenAI model", options=["gpt-3.5-turbo", "gpt-4"], index=0)
    max_candidates = st.number_input("Max resumes to process", min_value=1, max_value=20, value=10)
    openai_key = st.text_input("OpenAI API Key (optional)", type="password")
    if openai_key:
        os.environ["OPENAI_API_KEY"] = openai_key

st.subheader("Job Description")
job_description = st.text_area("Paste the job description here", height=200)

st.subheader("Upload Resumes")
uploaded_files = st.file_uploader("Choose PDF or TXT files", type=["pdf", "txt"], accept_multiple_files=True)

if st.button("Process"):

    if not job_description or not uploaded_files:
        st.error("Please provide a job description and at least one resume.")
    else:
        processed = []
        progress_bar = st.progress(0)
        n = min(len(uploaded_files), int(max_candidates))

        for i, f in enumerate(uploaded_files[:n]):
            st.info(f"Processing: {f.name}")
            try:
                text = extract_text_from_upload(f)
                result = score_resume_with_openai(resume_text=text, jd=job_description, model=model)
            except Exception as e:
                result = {
                    "score": 0,
                    "matching_skills": [],
                    "missing_skills": [],
                    "summary": f"Failed to process: {str(e)}"
                }

            processed.append({
                "Candidate": f.name,
                "Score": result.get("score", 0),
                "Matching Skills": ", ".join(result.get("matching_skills", [])),
                "Missing Skills": ", ".join(result.get("missing_skills", [])),
                "Summary": result.get("summary", "")
            })

            progress_bar.progress(int((i + 1) / n * 100))

        df = pd.DataFrame(processed).sort_values(by="Score", ascending=False)
        st.subheader("Results (ranked)")
        st.dataframe(df.reset_index(drop=True))

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download results (CSV)", csv, "resume_screening_results.csv", "text/csv")

        st.success("Processing complete.")

import streamlit as st
from backend.scorer import score_resume
from backend.parser import extract_text
import pandas as pd

st.title("Resume Screening AI Agent")

jd = st.text_area("Paste Job Description:")

uploaded_files = st.file_uploader("Upload Resumes (PDF/TXT)", accept_multiple_files=True)

if st.button("Process"):
    results = []

    for file in uploaded_files:
        text = extract_text(file)
        score_data = score_resume(text, jd)

        results.append({
            "Candidate": file.name,
            "Score": score_data["score"],
            "Matching Skills": ", ".join(score_data["matching_skills"]),
            "Missing Skills": ", ".join(score_data["missing_skills"]),
            "Summary": score_data["summary"]
        })

    df = pd.DataFrame(results)
    st.dataframe(df)

    st.download_button("Download Results CSV", df.to_csv().encode("utf-8"), "results.csv")

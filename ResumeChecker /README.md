# Resume Screening Agent

A lightweight Resume Screening web app (Streamlit) that uses OpenAI to compare resumes with a job description and return a suitability score and short reasoning.

## Features
- Upload multiple resumes (PDF or TXT)
- Extract text from resumes
- Compare resume vs job description using OpenAI
- Produce: score (0-100), matching skills, missing skills, summary
- Download ranked CSV results

## Tech stack
- Python, Streamlit (UI)
- OpenAI API (GPT models) for semantic scoring
- PyPDF2 for PDF parsing
- Pandas for results display/export

## Project structure

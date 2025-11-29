# backend/scorer.py
import os
import json
import time
import openai
from .utils import extract_json_substring

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

DEFAULT_MODEL = "gpt-3.5-turbo"

def _call_openai_chat(messages, model=DEFAULT_MODEL, max_retries=3, temperature=0.0):
    """
    Simple wrapper with retries.
    """
    for attempt in range(max_retries):
        try:
            resp = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=800
            )
            return resp
        except Exception as e:
            if attempt + 1 == max_retries:
                raise
            time.sleep(1 + attempt * 2)

def score_resume_with_openai(resume_text: str, jd: str, model: str = DEFAULT_MODEL) -> dict:
    """
    Uses OpenAI chat to produce a JSON result with:
    - score (0-100) integer
    - matching_skills (list of strings)
    - missing_skills (list of strings)
    - summary (short text)
    """

    prompt = f"""
You are an assistant that compares a candidate's resume to a job description and produces a JSON result.

Resume:
\"\"\"\n{resume_text}\n\"\"\"

Job Description:
\"\"\"\n{jd}\n\"\"\"

Produce output as **ONLY** valid JSON (no extra commentary) with these keys:
- score: integer 0-100 representing suitability (100 best)
- matching_skills: array of strings (skills/keywords present in the resume that match the JD)
- missing_skills: array of strings (important skills in the JD not found in the resume)
- summary: short 1-3 sentence explanation of why you gave the score

Rules:
1) Be concise.
2) If you are unsure about presence of a skill in resume, lean conservative (i.e., put it in missing_skills).
3) Score should take into account skills match, years of experience if present, and role relevance.

Respond with ONLY JSON. Example:
{{"score": 77, "matching_skills":["python","pandas"], "missing_skills":["spark"], "summary":"Candidate has strong Python and pandas experience but lacks Spark and distributed systems experience."}}
"""

    messages = [
        {"role": "system", "content": "You are a helpful assistant that compares resumes to job descriptions."},
        {"role": "user", "content": prompt}
    ]

    resp = _call_openai_chat(messages, model=model)
    # Extract text content
    content = resp["choices"][0]["message"]["content"]

    # Try to parse JSON; some models wrap text — extract substring between first { and last }
    json_text = extract_json_substring(content)
    try:
        data = json.loads(json_text)
    except json.JSONDecodeError as e:
        # fallback: return minimal structure
        return {
            "score": 0,
            "matching_skills": [],
            "missing_skills": [],
            "summary": f"Failed to parse model output: {str(e)}. Raw output: {content[:200]}"
        }

    # Ensure types and keys
    return {
        "score": int(data.get("score", 0)) if isinstance(data.get("score", 0), (int, float, str)) else 0,
        "matching_skills": data.get("matching_skills", []) if isinstance(data.get("matching_skills", []), list) else [],
        "missing_skills": data.get("missing_skills", []) if isinstance(data.get("missing_skills", []), list) else [],
        "summary": data.get("summary", "") if isinstance(data.get("summary", ""), str) else ""
    }

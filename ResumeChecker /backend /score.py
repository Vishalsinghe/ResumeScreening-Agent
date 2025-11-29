from openai import OpenAI
client = OpenAI()

def score_resume(resume_text, jd):

    prompt = f"""
    Compare the following resume with the job description.

    RESUME:
    {resume_text}

    JOB DESCRIPTION:
    {jd}

    Output JSON with:
    - score (0-100)
    - matching_skills
    - missing_skills
    - summary (1 paragraph)
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return eval(response.choices[0].message["content"])

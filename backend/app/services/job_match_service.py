from .ai_service import ask_ai

MAX_CV_CHARACTERS = 12000
MAX_JOB_DESCRIPTION_CHARACTERS = 8000


def _trim_text(text: str, max_characters: int) -> str:
    if len(text) <= max_characters:
        return text

    return (
        text[:max_characters]
        + "\n\n[Text was shortened to keep the AI request within response time limits.]"
    )


async def match_job(
    cv_text: str,
    target_role: str,
    job_description: str,
    location: str | None = None,
    experience_level: str | None = "Entry-level",
) -> str:
    system_prompt = """
    You are CareerBridge UK, a UK job matching and employability assistant.
    Compare candidate CVs against job descriptions realistically.
    Do not invent experience.
    """

    user_prompt = f"""
    Compare this candidate's CV against this UK job description.

    Target role: {target_role}
    Location: {location}
    Experience level: {experience_level}

    Candidate CV:
    {_trim_text(cv_text, MAX_CV_CHARACTERS)}

    Job description:
    {_trim_text(job_description, MAX_JOB_DESCRIPTION_CHARACTERS)}

    Provide:

    1. Overall Match Score out of 100
    2. Job Fit Summary
    3. Matching Skills and Experience
    4. Missing Skills or Weak Areas
    5. Missing Keywords from CV
    6. CV Changes Needed Before Applying
    7. Suggested Cover Letter Paragraph
    8. Interview Questions Likely from this Job
    9. Apply / Improve First Recommendation
    """

    return await ask_ai(system_prompt, user_prompt)

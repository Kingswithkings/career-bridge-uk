from .ai_service import ask_ai


def match_job(
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
    {cv_text}

    Job description:
    {job_description}

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

    return ask_ai(system_prompt, user_prompt)

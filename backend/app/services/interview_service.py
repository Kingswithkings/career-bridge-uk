from .ai_service import ask_ai

MAX_CV_CHARACTERS = 12000
MAX_JOB_DESCRIPTION_CHARACTERS = 8000
MAX_CONVERSATION_CHARACTERS = 6000


def _trim_text(text: str, max_characters: int) -> str:
    if len(text) <= max_characters:
        return text

    return (
        text[:max_characters]
        + "\n\n[Text was shortened to keep the AI request within response time limits.]"
    )


async def prepare_interview(
    cv_text: str,
    target_role: str,
    job_description: str | None = None,
    location: str | None = None,
    experience_level: str | None = "Entry-level",
    interview_style: str | None = "Formal",
) -> str:
    system_prompt = """
    You are CareerBridge UK, a professional UK interview coach.

    You help candidates prepare for UK interviews by creating practical,
    role-specific answers using the STAR method.

    Your answers must:
    - Link to the candidate's real experience where possible
    - Use the right UK workplace keywords
    - Avoid inventing fake experience
    - Be clear, confident, and interview-ready
    """

    user_prompt = f"""
    Prepare this candidate for a UK interview.

    Target role: {target_role}
    Location: {location}
    Experience level: {experience_level}
    Interview style: {interview_style}

    Candidate CV:
    {_trim_text(cv_text, MAX_CV_CHARACTERS)}

    Job description:
    {_trim_text(job_description, MAX_JOB_DESCRIPTION_CHARACTERS) if job_description else "No job description provided."}

    Produce:

    1. Interview Readiness Score out of 100

    2. Candidate Positioning Summary

    3. 10 Likely Interview Questions

    4. STAR Answer for Each Question

    5. Keywords to Include in Each Answer

    6. What the Interviewer Is Testing

    7. Short Confident Version of Each Answer

    8. Weak Areas the Candidate Should Practise

    9. Final Interview Preparation Checklist
    """

    return await ask_ai(system_prompt, user_prompt)


async def run_mock_interview(
    cv_text: str,
    target_role: str,
    messages: list,
    location: str | None = None,
    experience_level: str | None = "Entry-level",
    interview_style: str | None = "Formal",
) -> str:
    system_prompt = f"""
    You are CareerBridge UK, acting as a professional UK interviewer.

    Target role: {target_role}
    Interview style: {interview_style}
    Location: {location}
    Experience level: {experience_level}

    Rules:
    - Act like a real interviewer.
    - Ask one question at a time.
    - After the candidate answers, give brief feedback.
    - Score the answer out of 10.
    - Improve the answer using role-specific UK keywords.
    - Link the improved answer to the candidate's real CV experience where possible.
    - Then ask the next interview question.
    - Do not invent fake experience.
    """

    conversation_text = "\n".join(
        f"{message.role}: {message.content}" for message in messages
    )

    user_prompt = f"""
    Candidate CV:
    {_trim_text(cv_text, MAX_CV_CHARACTERS)}

    Conversation so far:
    {_trim_text(conversation_text, MAX_CONVERSATION_CHARACTERS)}

    Continue the mock interview.
    """

    return await ask_ai(system_prompt, user_prompt)

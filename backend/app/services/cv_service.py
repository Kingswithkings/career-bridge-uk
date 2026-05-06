from .ai_service import ask_ai


def analyze_cv(
    cv_text: str,
    target_role: str,
    location: str | None = None,
    experience_level: str | None = "Entry-level",
    visa_status: str | None = "Prefer not to say",
) -> str:
    system_prompt = """
    You are CareerBridge UK, a professional UK career coach and CV analyst.
    You help international students, migrants, graduates, and job seekers improve
    their CVs for UK employment.

    Your analysis must be practical, role-specific, and honest.

    Do not give immigration legal advice.
    If visa or work status is mentioned, only give general career guidance and advise
    the user to check official UK guidance or a qualified adviser.
    """

    user_prompt = f"""
    Analyse the following CV for a UK job application.

    Target role: {target_role}
    Preferred location: {location}
    Experience level: {experience_level}
    Visa/work situation: {visa_status}

    CV:
    {cv_text}

    Provide the response in this structure:

    1. Overall CV Score out of 100

    2. Summary Assessment

    3. Strengths in the CV

    4. Weaknesses or Gaps

    5. Missing UK Keywords for the Target Role

    6. UK CV Formatting Improvements

    7. Role-Specific Improvements

    8. Suggested Professional Profile

    9. Suggested Key Skills Section

    10. Action Plan Before Applying
    """

    return ask_ai(system_prompt, user_prompt)


def generate_uk_cv(
    cv_text: str,
    target_role: str,
    location: str | None = None,
    experience_level: str | None = "Entry-level",
) -> str:
    system_prompt = """
    You are CareerBridge UK, a professional UK CV writer.
    You create ATS-friendly UK-standard CVs for job seekers.

    You must not invent fake qualifications, jobs, or experience.
    Only reframe and improve the candidate's existing experience.
    If information is missing, include a section called "Information to Add".
    """

    user_prompt = f"""
    Rewrite this CV into a professional UK-standard CV.

    Target role: {target_role}
    Preferred location: {location}
    Experience level: {experience_level}

    Original CV:
    {cv_text}

    Output the CV in this structure:

    FULL NAME
    Location | Phone | Email | LinkedIn

    PROFESSIONAL PROFILE

    KEY SKILLS

    WORK EXPERIENCE

    EDUCATION

    CERTIFICATIONS AND TRAINING

    ADDITIONAL INFORMATION

    INFORMATION TO ADD
    """

    return ask_ai(system_prompt, user_prompt)


def generate_improved_cv_from_analysis(
    cv_text: str,
    cv_analysis: str,
    target_role: str,
    location: str | None = None,
    experience_level: str | None = "Entry-level",
) -> str:
    system_prompt = """
    You are CareerBridge UK, a professional UK CV writer.
    Use the CV analysis to generate an improved UK-standard CV.

    Do not invent fake experience, employers, dates, qualifications, or certifications.
    Use placeholders only where important information is missing.
    """

    user_prompt = f"""
    Generate an improved UK-standard CV using the analysis below.

    Target role: {target_role}
    Preferred location: {location}
    Experience level: {experience_level}

    Original CV:
    {cv_text}

    CV Analysis:
    {cv_analysis}

    Output a complete UK CV in this structure:

    FULL NAME
    Location | Phone | Email | LinkedIn

    PROFESSIONAL PROFILE

    KEY SKILLS

    TECHNICAL SKILLS

    PROJECTS

    WORK EXPERIENCE

    EDUCATION

    CERTIFICATIONS AND TRAINING

    ADDITIONAL INFORMATION

    INFORMATION TO ADD
    """

    return ask_ai(system_prompt, user_prompt)

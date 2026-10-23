from backend.app.xai.schemas import CareerProfile, JobEvidence


def analyse_career_profile(
    candidate: CareerProfile,
    job: JobEvidence,
) -> dict:
    """Compare candidate skills against a job's requirements."""

    candidate_skills = {
        skill.strip().casefold()
        for skill in candidate.skills
    }

    matched_skills = [
        skill
        for skill in job.required_skills
        if skill.strip().casefold() in candidate_skills
    ]

    missing_skills = [
        skill
        for skill in job.required_skills
        if skill.strip().casefold() not in candidate_skills
    ]

    total_required = len(job.required_skills)

    match_percentage = (
        round(len(matched_skills) / total_required * 100, 2)
        if total_required
        else None
    )

    return {
        "career_goal": candidate.career_goal,
        "job_id": job.job_id,
        "job_title": job.title,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "skill_match_percentage": match_percentage,
    }

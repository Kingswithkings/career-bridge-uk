"""Deterministic evaluation of CareerBridge job-match evidence."""

from backend.app.xai.schemas import CareerProfile, JobEvidence


def evaluate_job_match(
    candidate: CareerProfile,
    job: JobEvidence,
    *,
    evidence_origin: str,
    source_type: str,
) -> dict:
    """Evaluate skill coverage and identify evidence limitations."""

    candidate_skills = {
        skill.strip().casefold()
        for skill in candidate.skills
        if skill.strip()
    }

    required_skills = list(
        dict.fromkeys(
            skill.strip()
            for skill in job.required_skills
            if skill.strip()
        )
    )

    matched = [
        skill
        for skill in required_skills
        if skill.casefold() in candidate_skills
    ]
    missing = [
        skill
        for skill in required_skills
        if skill.casefold() not in candidate_skills
    ]

    score = (
        round(100 * len(matched) / len(required_skills), 2)
        if required_skills
        else None
    )

    verified_live = (
        source_type == "live"
        and bool(job.source_url)
    )

    return {
        "job_id": job.job_id,
        "job_title": job.title,
        "company": job.company,
        "skill_match_percentage": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "evidence_origin": evidence_origin,
        "source_type": source_type,
        "source_url": job.source_url,
        "verified_live_vacancy": False,
        "evidence_warnings": (
            ["Demonstration job; not a verified live vacancy."]
            if source_type == "sample"
            else ["Live vacancy status has not been independently verified."]
        ),
    }

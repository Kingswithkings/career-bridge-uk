"""Deterministic evaluation of CareerBridge job-match evidence."""

from backend.app.xai.schemas import CareerProfile, JobEvidence


def evaluate_job_match(
    candidate: CareerProfile,
    job: JobEvidence,
    *,
    evidence_origin: str,
    source_type: str,
    skill_evidence_method: str = "source_requirements",
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

    warnings = (
        ["Demonstration job; not a verified live vacancy."]
        if source_type == "sample"
        else ["Live vacancy status has not been independently verified."]
    )
    if skill_evidence_method == "description_keyword_mentions":
        warnings.append(
            "Skills are keyword mentions in an Adzuna listing summary, "
            "not independently verified employer requirements."
        )

    return {
        "job_id": job.job_id,
        "job_title": job.title,
        "company": job.company,
        "skill_match_percentage": score,
        "metric_label": (
            "skill mention coverage" if skill_evidence_method == "description_keyword_mentions"
            else "listed required-skill coverage"
        ),
        "skill_evidence_method": skill_evidence_method,
        "matched_skills": matched,
        "missing_skills": missing,
        "evidence_origin": evidence_origin,
        "source_type": source_type,
        "source_url": job.source_url,
        "verified_live_vacancy": False,
        "evidence_warnings": warnings,
    }

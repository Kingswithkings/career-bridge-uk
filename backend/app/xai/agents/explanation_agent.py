"""Evidence-grounded explanations for CareerBridge XAI."""


def explain_job_match(evaluation: dict) -> dict:
    """Explain a deterministic skill-match evaluation."""

    job_title = evaluation["job_title"]
    company = evaluation["company"]
    score = evaluation["skill_match_percentage"]
    matched = evaluation["matched_skills"]
    missing = evaluation["missing_skills"]

    if score is None:
        summary = (
            f"The skill match for {job_title} at {company} "
            "cannot be calculated because no required skills were provided."
        )
    else:
        summary = (
            f"The candidate matches {score:g}% of the listed skills "
            f"for {job_title} at {company}."
        )

    matched_text = (
        f"Matched skills: {', '.join(matched)}."
        if matched
        else "No required skills were matched."
    )

    missing_text = (
        f"Missing skills: {', '.join(missing)}."
        if missing
        else "No missing skills were identified among the listed requirements."
    )

    warnings = evaluation.get("evidence_warnings", [])

    return {
        "job_id": evaluation["job_id"],
        "job_title": job_title,
        "summary": summary,
        "why_matched": matched_text,
        "skills_to_develop": missing,
        "missing_skills_explanation": missing_text,
        "evidence": {
            "origin": evaluation["evidence_origin"],
            "source_type": evaluation["source_type"],
            "source_url": evaluation.get("source_url"),
            "verified_live_vacancy": evaluation["verified_live_vacancy"],
        },
        "limitations": warnings + [
            "Skill coverage alone does not establish overall job suitability."
        ],
    }

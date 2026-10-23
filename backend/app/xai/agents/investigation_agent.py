"""Evidence-linked cross-vacancy investigation with a deterministic critic."""

from collections import defaultdict


def critique_sources(records: list[dict]) -> dict:
    """Identify source gaps before explaining anything; never equate a URL with verification."""
    origins = {str(r.get("evidence_origin", "unknown")) for r in records}
    live = [r for r in records if r.get("source_type") != "sample"]
    usable = [r for r in records if r.get("required_skills")]
    live_usable = [r for r in live if r.get("required_skills")]
    live_providers = {str(r.get("evidence_origin", "unknown")) for r in live_usable}
    reasons = []
    if not records:
        reasons.append("No job evidence was retrieved.")
    if len(usable) < 2:
        reasons.append("Fewer than two jobs have usable skills evidence.")
    if not live:
        reasons.append("All retrieved job records are sample data, not real vacancies.")
    if len(live_providers) < 2:
        reasons.append(
            "Fewer than two independently sourced non-sample job-data providers are represented."
        )
    if live and not all(r.get("source_url") for r in live):
        reasons.append("At least one non-sample listing has no source URL.")
    return {
        "sufficient_for_cross_source_inference": bool(len(live_usable) >= 2 and len(live_providers) >= 2),
        "needs_additional_source": len(live_providers) < 2,
        "limitations": reasons,
        "provider_count": len(origins),
        "providers": sorted(origins),
        "non_sample_providers": sorted(live_providers),
        "non_sample_count": len(live),
        "usable_non_sample_count": len(live_usable),
        "sample_count": len(records) - len(live),
    }


def investigate_career_evidence(candidate, results: list[dict], records: list[dict], *, question: str | None = None) -> dict:
    """Produce grounded, source-addressable gap hypotheses and next actions."""
    by_id = {str(record["job_id"]): record for record in records}
    skills = defaultdict(lambda: {"jobs": set(), "origins": set()})
    for result in results:
        evaluation = result["evaluation"]
        record = by_id.get(str(result["job_id"]))
        if record is None:
            continue
        for missing in evaluation["missing_skills"]:
            key = missing.casefold().strip()
            if not key:
                continue
            skills[key]["jobs"].add(str(record["job_id"]))
            skills[key]["origins"].add(str(record.get("evidence_origin", "unknown")))

    labels = {
        skill.casefold(): skill for record in records
        for skill in record.get("required_skills", [])
    }
    priorities = []
    for key, matches in skills.items():
        cited_jobs = sorted(matches["jobs"])
        refs = [
            {
                "job_id": job_id,
                "origin": by_id[job_id].get("evidence_origin", "unknown"),
                "source_type": by_id[job_id].get("source_type", "unknown"),
                "source_url": by_id[job_id].get("source_url"),
                "evidence_method": by_id[job_id].get("skill_evidence_method", "source_requirements"),
            }
            for job_id in cited_jobs
        ]
        priorities.append({
            "skill": labels.get(key, key),
            "jobs_mentioning_gap": len(cited_jobs),
            "source_providers": sorted(matches["origins"]),
            "evidence_references": refs,
            "recommended_action": "Add truthful evidence of this skill to your CV, or develop it if needed.",
        })
    priorities.sort(key=lambda p: (-p["jobs_mentioning_gap"], p["skill"].casefold()))
    review = critique_sources(records)
    if not records:
        conclusion = "Insufficient evidence to assess the target career goal."
    elif review["sufficient_for_cross_source_inference"]:
        conclusion = (
            "These skills are not listed in the candidate profile but recur in the cited job "
            "evidence. This does not establish why an employer rejected an application."
        )
    else:
        conclusion = (
            "These are preliminary gaps relative to the retrieved records. Broader, "
            "independently checked evidence is needed before drawing labor-market conclusions."
        )
    return {
        "question": question or f"Which documented skills should I demonstrate for {candidate.career_goal}?",
        "candidate_goal": candidate.career_goal,
        "candidate_source": "user_provided_profile",
        "evidence_jobs": len(records),
        "source_critique": review,
        "conclusion": conclusion,
        "priority_skill_gaps": priorities,
        "next_actions": [
            "Review each cited job description and confirm whether a skill is genuinely required.",
            "Add relevant, truthful examples of completed projects to the CV.",
            "Request employer feedback to investigate any actual rejection decision.",
        ],
        "boundaries": [
            "An unlisted candidate skill is not proof that the candidate lacks the skill.",
            "Description keyword mentions are not independently verified employer requirements.",
            "Skill overlap is not a hiring probability or an explanation of a hiring decision.",
            "Links and recency do not independently prove that a vacancy remains open.",
        ],
    }

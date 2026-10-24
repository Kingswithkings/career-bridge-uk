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



def assess_skill_gap_hypotheses(skill: str, refs: list[dict]) -> dict:
    """Separate profile evidence, vacancy claims, and unresolved assumptions."""
    live = [r for r in refs if r.get("source_type") != "sample"]
    synthetic = [r for r in refs if r.get("source_type") == "sample"]

    if not live:
        next_check = (
            f"Retrieve real job descriptions mentioning {skill}; "
            "synthetic examples cannot establish labor-market demand."
        )
    elif any(not r.get("source_url") for r in live):
        next_check = (
            "Locate the original source for each uncited listing "
            "before treating it as supporting evidence."
        )
    else:
        next_check = (
            f"Inspect the cited descriptions to establish whether {skill} "
            "is mandatory, preferred, or merely mentioned."
        )

    return {
        "hypotheses": [
            {
                "claim": f"{skill} is not documented in the submitted profile.",
                "assessment": "supported_by_profile_comparison",
                "supporting_job_ids": [
                    r["job_id"] for r in refs
                ],
            },
            {
                "claim": f"{skill} is a mandatory employer requirement.",
                "assessment": "unverified",
                "reason": (
                    "The retrieved skill evidence has not established "
                    "that each mention represents a mandatory requirement."
                ),
            },
            {
                "claim": f"The candidate cannot perform work involving {skill}.",
                "assessment": "unknown",
                "reason": (
                    "An omitted profile skill does not prove a lack "
                    "of practical ability."
                ),
            },
        ],
        "live_listing_references": len(live),
        "synthetic_references": len(synthetic),
        "next_evidence_check": next_check,
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
                "source_excerpt": by_id[job_id].get(
                    "skill_contexts", {}
                ).get(labels.get(key, key)),
            }
            for job_id in cited_jobs
        ]
        live_count = sum(
            by_id[job_id].get("source_type") != "sample"
            for job_id in cited_jobs
        )
        sample_count = len(cited_jobs) - live_count

        priorities.append({
            "skill": labels.get(key, key),
            "jobs_mentioning_gap": len(cited_jobs),
            "live_listings_mentioning_gap": live_count,
            "synthetic_examples_mentioning_gap": sample_count,
            "evidence_strength": (
                "unverified_listing_mentions"
                if live_count
                else "synthetic_only"
            ),
            "source_providers": sorted(matches["origins"]),
            "evidence_references": refs,
            "why_it_matters": (
                f"The submitted candidate profile does not document {labels.get(key, key)}. "
                f"It appears in {live_count} non-sample job record(s) and "
                f"{sample_count} synthetic demonstration record(s). "
                "Non-sample records are not automatically verified vacancies, "
                "and skill mentions do not prove mandatory requirements."
                if live_count
                else
                f"The submitted candidate profile does not document {labels.get(key, key)}, "
                f"but this finding is based only on {sample_count} synthetic "
                "demonstration record(s). It cannot establish real labor-market demand."
            ),
            "alternative_explanation": (
                "The candidate may possess this skill but have omitted it from "
                "their profile. A listing may also mention the skill as optional "
                "rather than mandatory."
            ),
            "verification_action": (
                "Inspect the cited vacancy descriptions and evidence methods, "
                "confirm whether the skill is mandatory, and add truthful project "
                "evidence or develop the skill if genuinely needed."
            ),
            "hypothesis_investigation": assess_skill_gap_hypotheses(
                labels.get(key, key), refs
            ),
            "recommended_action": "Add truthful evidence of this skill to your CV, or develop it if needed.",
        })
    priorities.sort(
        key=lambda p: (
            -p["live_listings_mentioning_gap"],
            -p["jobs_mentioning_gap"],
            p["skill"].casefold(),
        )
    )
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

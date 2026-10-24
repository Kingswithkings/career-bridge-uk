"""CareerBridge XAI source-aware multi-step agent orchestration."""

from uuid import uuid4

from backend.app.xai.schemas import CareerProfile, JobEvidence
from backend.app.xai.agents.career_planning import analyse_career_profile
from backend.app.xai.agents.evidence_agent import retrieve_job_evidence, retrieve_demo_job_evidence
from backend.app.xai.agents.evaluation_agent import evaluate_job_match
from backend.app.xai.agents.explanation_agent import explain_job_match
from backend.app.xai.agents.investigation_agent import critique_sources, investigate_career_evidence
from backend.app.xai.agents.live_job_agent import retrieve_live_job_evidence
from backend.app.xai.integrations.meterless_client import build_meterless_graph
from backend.app.xai.integrations.nightshift_runtime import request_nightshift_insight
from backend.app.xai.integrations.nvidia_nemotron import request_nvidia_insight
from backend.app.xai.tracing.audit import write_xai_audit


def run_careerbridge_xai(
    candidate: CareerProfile,
    *,
    limit: int = 3,
    include_live_jobs: bool = False,
    location: str | None = None,
    question: str | None = None,
    include_nvidia_insight: bool = False,
) -> dict:
    """Investigate job evidence, optionally enrich it, critique and explain it.

    Live source enrichment is bounded to a single attempt. Missing credentials and
    API outages never become fabricated job evidence.
    """
    run_id = str(uuid4())
    import os

    demo_mode = (
        os.getenv("CAREERBRIDGE_XAI_DEMO_MODE", "").lower()
        in {"true", "1", "yes"}
    )

    records = (
        retrieve_demo_job_evidence(limit=limit)
        if demo_mode
        else retrieve_job_evidence(limit=limit)
    )
    trace = [
        {
            "step": "retrieve_demo_evidence" if demo_mode else "retrieve_zetaris",
            "status": "completed",
            "records": len(records),
            "source_critique": critique_sources(records)["limitations"],
        }
    ]

    initial_review = critique_sources(records)
    if include_live_jobs:
        # Deliberate branching: the critic determines whether to investigate
        # another source; user opt-in permits exactly one live enrichment pass.
        reason = (
            "source_gap_identified" if initial_review["needs_additional_source"]
            else "user_requested_live_enrichment"
        )
        try:
            live_records = retrieve_live_job_evidence(
                candidate.career_goal, limit=min(limit, 10), location=location
            )
            existing = {
                (str(record.get("source_url") or ""), str(record.get("job_id") or ""))
                for record in records
            }
            added = 0
            for record in live_records:
                identity = (str(record.get("source_url") or ""), str(record.get("job_id") or ""))
                if identity not in existing:
                    records.append(record)
                    existing.add(identity)
                    added += 1
            trace.append({
                "step": "enrich_adzuna",
                "status": "completed",
                "reason": reason,
                "records_added": added,
                "max_attempts": 1,
            })
        except Exception as error:
            # Do not leak provider responses, authentication keys or private URLs.
            trace.append({
                "step": "enrich_adzuna",
                "status": "unavailable",
                "reason": reason,
                "error_type": type(error).__name__,
                "max_attempts": 1,
            })
    else:
        trace.append({
            "step": "enrich_adzuna",
            "status": "not_requested",
            "reason": "Live job lookups require explicit opt-in.",
        })

    meterless = build_meterless_graph(records)
    results = []
    for record in records:
        job = JobEvidence(
            job_id=record["job_id"],
            title=record["job_title"],
            company=record["company"],
            required_skills=record["required_skills"],
            source_url=record.get("source_url"),
        )
        career_analysis = analyse_career_profile(candidate, job)
        evaluation = evaluate_job_match(
            candidate,
            job,
            evidence_origin=record["evidence_origin"],
            source_type=record["source_type"],
            skill_evidence_method=record.get("skill_evidence_method", "source_requirements"),
        )
        explanation = explain_job_match(evaluation)
        results.append({
            "job_id": job.job_id,
            "career_analysis": career_analysis,
            "evaluation": evaluation,
            "explanation": explanation,
        })

    investigation = investigate_career_evidence(
        candidate, results, records, question=question
    )
    trace.append({
        "step": "evaluate_evidence",
        "status": "completed",
        "cross_source_supported": investigation["source_critique"][
            "sufficient_for_cross_source_inference"
        ],
        "remaining_limitations": investigation["source_critique"]["limitations"],
    })
    nightshift = request_nightshift_insight(investigation)
    trace.append({
        "step": "nightshift_inference",
        "status": nightshift["status"],
        "used": nightshift["used"],
    })
    nvidia = (
        request_nvidia_insight(investigation)
        if include_nvidia_insight
        else {"status": "not_requested", "used": False}
    )
    trace.append({
        "step": "nvidia_inference",
        "status": nvidia["status"],
        "used": nvidia["used"],
    })

    response = {
        "run_id": run_id,
        "candidate_goal": candidate.career_goal,
        "jobs_evaluated": len(results),
        "meterless": meterless,
        "evidence_graph": meterless["evidence_graph"],
        "results": results,
        "investigation": investigation,
        "agent_trace": trace,
        "nightshift": nightshift,
        "nvidia": nvidia,
    }
    write_xai_audit(response)
    return response

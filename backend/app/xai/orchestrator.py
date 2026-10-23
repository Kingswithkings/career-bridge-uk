from backend.app.xai.tracing.audit import write_xai_audit
"""CareerBridge XAI multi-agent orchestration."""

from uuid import uuid4

from backend.app.xai.schemas import CareerProfile, JobEvidence
from backend.app.xai.agents.career_planning import analyse_career_profile
from backend.app.xai.agents.evidence_agent import retrieve_job_evidence
from backend.app.xai.agents.evaluation_agent import evaluate_job_match
from backend.app.xai.agents.explanation_agent import explain_job_match
from backend.app.xai.integrations.meterless_client import build_meterless_graph


def run_careerbridge_xai(
    candidate: CareerProfile,
    *,
    limit: int = 3,
) -> dict:
    """Run evidence retrieval, matching, evaluation and explanation."""

    run_id = str(uuid4())
    records = retrieve_job_evidence(limit=limit)
    meterless = build_meterless_graph(records)
    results = []

    for record in records:
        job = JobEvidence(
            job_id=record["job_id"],
            title=record["job_title"],
            company=record["company"],
            required_skills=record["required_skills"],
            source_url=record["source_url"],
        )

        career_analysis = analyse_career_profile(candidate, job)

        evaluation = evaluate_job_match(
            candidate,
            job,
            evidence_origin=record["evidence_origin"],
            source_type=record["source_type"],
        )

        explanation = explain_job_match(evaluation)

        results.append(
            {
                "job_id": job.job_id,
                "career_analysis": career_analysis,
                "evaluation": evaluation,
                "explanation": explanation,
            }
        )

    response = {
        "run_id": run_id,
        "candidate_goal": candidate.career_goal,
        "jobs_evaluated": len(results),
        "meterless": meterless,
        "evidence_graph": meterless["evidence_graph"],
        "results": results,
    }

    write_xai_audit(response)
    return response

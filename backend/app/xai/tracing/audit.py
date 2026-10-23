"""JSONL audit logging for CareerBridge XAI."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path

def write_xai_audit(result: dict) -> None:
    path = Path(os.getenv(
        "XAI_AUDIT_PATH",
        "/tmp/careerbridge-xai-audit.jsonl"
    ))
    path.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "run_id": result["run_id"],
        "candidate_goal": result["candidate_goal"],
        "jobs_evaluated": result["jobs_evaluated"],
        "meterless": {
            "engine": result["meterless"]["engine"],
            "jobs_received": result["meterless"]["jobs_received"],
            "relationship_count": result["evidence_graph"]["relationship_count"],
            "jobs": [
                {
                    "id": job["id"],
                    "provenance": job.get("provenance"),
                }
                for job in result["evidence_graph"]["jobs"]
            ],
        },
        "agent_trace": result.get("agent_trace", []),
        "nightshift": {
            "status": result.get("nightshift", {}).get("status", "not_recorded"),
            "used": result.get("nightshift", {}).get("used", False),
            "model_reported": result.get("nightshift", {}).get("model_reported"),
        },
        "investigation": {
            "evidence_jobs": result.get("investigation", {}).get("evidence_jobs", 0),
            "source_critique": result.get("investigation", {}).get("source_critique", {}),
            "priority_skill_gaps": [
                {
                    "skill": item["skill"],
                    "jobs_mentioning_gap": item["jobs_mentioning_gap"],
                    "cited_job_ids": [ref["job_id"] for ref in item["evidence_references"]],
                }
                for item in result.get("investigation", {}).get("priority_skill_gaps", [])
            ],
        },
        "evaluations": [
            {
                "job_id": item["job_id"],
                "evaluation": item["evaluation"],
                "explanation": item["explanation"]
            }
            for item in result["results"]
        ]
    }
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, default=str) + "\n")

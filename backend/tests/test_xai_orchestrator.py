"""Tests for CareerBridge XAI orchestration."""

from backend.app.xai import orchestrator
from backend.app.xai.schemas import CareerProfile


def test_orchestrator_evaluates_and_audits(monkeypatch):
    jobs = [
        {
            "job_id": "DEMO-001",
            "job_title": "AI Engineer",
            "company": "Demo Technology Ltd",
            "required_skills": ["Python", "FastAPI", "LLMs", "Docker"],
            "source_url": None,
            "source_type": "sample",
            "evidence_origin": "zetaris",
        }
    ]

    audits = []

    meterless_result = {
        "engine": "Meterless World Model",
        "jobs_received": 1,
        "evidence_graph": {
            "jobs": [
                {
                    "id": "job:ingest:zetaris:DEMO-001",
                    "title": "AI Engineer",
                    "skills": ["Python", "FastAPI", "LLMs", "Docker"],
                    "provenance": {
                        "kind": "pipeline",
                        "by": "careerbridge-zetaris-evidence-agent",
                        "at": "2026-10-22T06:59:54.842Z",
                    },
                }
            ],
            "relationship_count": 4,
        },
    }

    monkeypatch.setattr(
        orchestrator,
        "build_meterless_graph",
        lambda records: meterless_result,
    )

    monkeypatch.setattr(
        orchestrator,
        "retrieve_job_evidence",
        lambda limit: jobs[:limit],
    )
    monkeypatch.setattr(
        orchestrator,
        "write_xai_audit",
        lambda result: audits.append(result),
    )

    candidate = CareerProfile(
        skills=["Python", "FastAPI", "LLMs"],
        experience_years=3,
        education=["MSc Applied AI"],
        career_goal="AI Engineer",
    )

    result = orchestrator.run_careerbridge_xai(
        candidate,
        limit=1,
    )

    assert result["jobs_evaluated"] == 1
    assert result["meterless"]["engine"] == "Meterless World Model"
    assert result["evidence_graph"]["relationship_count"] == 4
    assert result["results"][0]["job_id"] == "DEMO-001"
    assert result["results"][0]["evaluation"]["skill_match_percentage"] == 75.0
    assert len(audits) == 1
    assert audits[0]["run_id"] == result["run_id"]
    assert audits[0]["jobs_evaluated"] == 1

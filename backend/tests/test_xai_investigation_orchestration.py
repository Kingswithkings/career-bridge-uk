"""Offline tests for critique-driven orchestration and graceful provider fallback."""

from backend.app.xai import orchestrator
from backend.app.xai.schemas import CareerProfile


SAMPLE = {
    "job_id": "DEMO-001",
    "job_title": "AI Engineer",
    "company": "Synthetic Employer",
    "required_skills": ["Python", "Docker"],
    "source_url": None,
    "source_type": "sample",
    "evidence_origin": "zetaris",
}
LIVE = {
    "job_id": "ADZ-001",
    "job_title": "AI Engineer",
    "company": "Test Employer",
    "required_skills": ["Python", "Docker", "Azure"],
    "source_url": "https://example.org/job/1",
    "source_type": "live_listing_unverified",
    "evidence_origin": "adzuna",
    "skill_evidence_method": "description_keyword_mentions",
}


def setup_offline(monkeypatch):
    audits = []
    monkeypatch.setattr(orchestrator, "retrieve_job_evidence", lambda limit: [SAMPLE.copy()])
    monkeypatch.setattr(
        orchestrator,
        "build_meterless_graph",
        lambda records: {
            "engine": "Meterless World Model",
            "jobs_received": len(records),
            "evidence_graph": {"jobs": [], "relationship_count": 0},
        },
    )
    monkeypatch.setattr(orchestrator, "write_xai_audit", lambda response: audits.append(response))
    monkeypatch.setattr(
        orchestrator,
        "request_nightshift_insight",
        lambda investigation: {"status": "disabled", "used": False},
    )
    return audits


def test_opt_in_adds_second_source_and_preserves_uncertainty(monkeypatch):
    audits = setup_offline(monkeypatch)
    monkeypatch.setattr(
        orchestrator, "retrieve_live_job_evidence", lambda *args, **kwargs: [LIVE.copy()]
    )
    candidate = CareerProfile(skills=["Python"], career_goal="AI Engineer")
    result = orchestrator.run_careerbridge_xai(
        candidate, limit=3, include_live_jobs=True, question="Why?"
    )
    assert result["jobs_evaluated"] == 2
    assert result["agent_trace"][1]["records_added"] == 1
    assert result["investigation"]["source_critique"]["provider_count"] == 2
    assert result["investigation"]["source_critique"]["sufficient_for_cross_source_inference"] is False
    assert result["investigation"]["question"] == "Why?"
    assert result["results"][1]["evaluation"]["verified_live_vacancy"] is False
    assert result["results"][1]["evaluation"]["metric_label"] == "skill mention coverage"
    assert "keyword mentions" in " ".join(
        result["results"][1]["evaluation"]["evidence_warnings"]
    )
    assert len(audits) == 1


def test_live_source_failure_is_logged_without_fabricating_data(monkeypatch):
    setup_offline(monkeypatch)

    def fail(*args, **kwargs):
        raise RuntimeError("Simulated provider outage")

    monkeypatch.setattr(orchestrator, "retrieve_live_job_evidence", fail)
    result = orchestrator.run_careerbridge_xai(
        CareerProfile(skills=["Python"], career_goal="AI Engineer"),
        include_live_jobs=True,
    )
    assert result["jobs_evaluated"] == 1
    assert result["agent_trace"][1]["status"] == "unavailable"
    assert result["investigation"]["source_critique"][
        "sufficient_for_cross_source_inference"
    ] is False


def test_default_does_not_call_live_source(monkeypatch):
    setup_offline(monkeypatch)

    def must_not_call(*args, **kwargs):
        raise AssertionError("Live source contacted without user opt-in")

    monkeypatch.setattr(orchestrator, "retrieve_live_job_evidence", must_not_call)
    result = orchestrator.run_careerbridge_xai(
        CareerProfile(skills=["Python"], career_goal="AI Engineer")
    )
    assert result["agent_trace"][1]["status"] == "not_requested"

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
    monkeypatch.setattr(
        orchestrator, "retrieve_job_evidence", lambda limit: [SAMPLE.copy()]
    )
    monkeypatch.setattr(
        orchestrator,
        "build_meterless_graph",
        lambda records: {
            "engine": "Meterless World Model",
            "jobs_received": len(records),
            "evidence_graph": {"jobs": [], "relationship_count": 0},
        },
    )
    monkeypatch.setattr(
        orchestrator, "write_xai_audit", lambda response: audits.append(response)
    )
    monkeypatch.setattr(
        orchestrator,
        "request_nightshift_insight",
        lambda investigation: {"status": "disabled", "used": False},
    )
    return audits


def test_opt_in_adds_second_source_and_preserves_uncertainty(monkeypatch):
    audits = setup_offline(monkeypatch)
    monkeypatch.setattr(
        orchestrator,
        "retrieve_live_job_evidence",
        lambda *args, **kwargs: [LIVE.copy()],
    )
    candidate = CareerProfile(skills=["Python"], career_goal="AI Engineer")
    result = orchestrator.run_careerbridge_xai(
        candidate, limit=3, include_live_jobs=True, question="Why?"
    )
    assert result["jobs_evaluated"] == 2
    assert result["agent_trace"][1]["records_added"] == 1
    assert result["investigation"]["source_critique"]["provider_count"] == 2
    assert (
        result["investigation"]["source_critique"][
            "sufficient_for_cross_source_inference"
        ]
        is False
    )
    assert result["investigation"]["question"] == "Why?"
    assert result["results"][1]["evaluation"]["verified_live_vacancy"] is False
    assert (
        result["results"][1]["evaluation"]["metric_label"] == "skill mention coverage"
    )
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
    assert (
        result["investigation"]["source_critique"][
            "sufficient_for_cross_source_inference"
        ]
        is False
    )


def test_default_does_not_call_live_source(monkeypatch):
    setup_offline(monkeypatch)

    def must_not_call(*args, **kwargs):
        raise AssertionError("Live source contacted without user opt-in")

    monkeypatch.setattr(orchestrator, "retrieve_live_job_evidence", must_not_call)
    result = orchestrator.run_careerbridge_xai(
        CareerProfile(skills=["Python"], career_goal="AI Engineer")
    )
    assert result["agent_trace"][1]["status"] == "not_requested"


def test_nvidia_inference_requires_explicit_opt_in(monkeypatch):
    setup_offline(monkeypatch)
    monkeypatch.setenv("CAREERBRIDGE_XAI_DEMO_MODE", "false")

    calls = []

    def fake_nvidia(investigation):
        calls.append(investigation)
        return {
            "status": "success",
            "used": True,
            "model_reported": "nvidia/nemotron-3.5-lightning-30b-a3b",
            "advisory_narrative": "Evidence-grounded test explanation.",
            "independently_verified": False,
        }

    monkeypatch.setattr(orchestrator, "request_nvidia_insight", fake_nvidia)

    candidate = CareerProfile(
        skills=["Python"],
        career_goal="AI Engineer",
    )

    default = orchestrator.run_careerbridge_xai(candidate)

    assert default["nvidia"]["status"] == "not_requested"
    assert calls == []

    enabled = orchestrator.run_careerbridge_xai(
        candidate,
        include_nvidia_insight=True,
    )

    assert enabled["nvidia"]["status"] == "success"
    assert enabled["nvidia"]["used"] is True
    assert len(calls) == 1
    assert enabled["nvidia"]["independently_verified"] is False

    assert any(
        step["step"] == "nvidia_inference" and step["status"] == "success"
        for step in enabled["agent_trace"]
    )


def test_live_only_ignores_demo_records(monkeypatch):
    setup_offline(monkeypatch)
    monkeypatch.setenv("CAREERBRIDGE_XAI_DEMO_MODE", "true")

    def reject_samples(*args, **kwargs):
        raise AssertionError("Sample retrieval must not run")

    monkeypatch.setattr(orchestrator, "retrieve_demo_job_evidence", reject_samples)
    monkeypatch.setattr(orchestrator, "retrieve_job_evidence", reject_samples)
    monkeypatch.setattr(
        orchestrator, "retrieve_live_job_evidence", lambda *a, **kw: [LIVE.copy()]
    )
    result = orchestrator.run_careerbridge_xai(
        CareerProfile(skills=["Python"], career_goal="AI Engineer"),
        require_live_evidence=True,
    )
    assert result["jobs_evaluated"] == 1
    assert result["investigation"]["source_critique"]["sample_count"] == 0


def test_live_only_rejects_empty_provider_results(monkeypatch):
    import pytest

    setup_offline(monkeypatch)
    monkeypatch.setattr(orchestrator, "retrieve_live_job_evidence", lambda *a, **kw: [])
    with pytest.raises(
        orchestrator.LiveEvidenceUnavailable, match="No sample data was used"
    ):
        orchestrator.run_careerbridge_xai(
            CareerProfile(skills=["Python"], career_goal="AI Engineer"),
            require_live_evidence=True,
        )


def test_explicit_zetaris_snapshot_mode(monkeypatch):
    setup_offline(monkeypatch)

    snapshot = {
        **LIVE,
        "retrieval_channel": "zetaris",
        "evidence_freshness": "stored_snapshot",
        "collected_at": "2026-10-25T23:00:00+00:00",
    }

    calls = []

    def retrieve_snapshots(limit):
        calls.append(limit)
        return [snapshot.copy()]

    def reject_fresh(*args, **kwargs):
        raise AssertionError("Fresh Adzuna retrieval must not run")

    monkeypatch.setattr(
        orchestrator,
        "retrieve_zetaris_adzuna_evidence",
        retrieve_snapshots,
    )
    monkeypatch.setattr(
        orchestrator,
        "retrieve_live_job_evidence",
        reject_fresh,
    )

    result = orchestrator.run_careerbridge_xai(
        CareerProfile(skills=["Python"], career_goal="AI Engineer"),
        evidence_mode="zetaris_snapshot",
        limit=3,
    )

    assert calls == [3]
    assert result["jobs_evaluated"] == 1
    assert result["agent_trace"][0]["step"] == "retrieve_zetaris_snapshot"

    critique = result["investigation"]["source_critique"]
    assert critique["snapshot_count"] == 1
    assert critique["fresh_listing_count"] == 0
    assert critique["sufficient_for_cross_source_inference"] is False
    assert any("historical evidence" in item for item in critique["limitations"])

    gap = result["investigation"]["priority_skill_gaps"][0]
    reference = gap["evidence_references"][0]

    assert reference["retrieval_channel"] == "zetaris"
    assert reference["evidence_freshness"] == "stored_snapshot"
    assert reference["collected_at"] == snapshot["collected_at"]


def test_live_only_never_reads_zetaris_snapshots(monkeypatch):
    setup_offline(monkeypatch)

    def reject_snapshots(*args, **kwargs):
        raise AssertionError("Zetaris snapshots must not enter live-only mode")

    monkeypatch.setattr(
        orchestrator,
        "retrieve_zetaris_adzuna_evidence",
        reject_snapshots,
    )
    monkeypatch.setattr(
        orchestrator,
        "retrieve_live_job_evidence",
        lambda *args, **kwargs: [LIVE.copy()],
    )

    result = orchestrator.run_careerbridge_xai(
        CareerProfile(skills=["Python"], career_goal="AI Engineer"),
        require_live_evidence=True,
    )

    assert result["jobs_evaluated"] == 1
    assert result["investigation"]["source_critique"]["snapshot_count"] == 0


def test_snapshot_mode_rejects_live_retrieval(monkeypatch):
    import pytest

    setup_offline(monkeypatch)

    candidate = CareerProfile(
        skills=["Python"],
        career_goal="AI Engineer",
    )

    with pytest.raises(ValueError, match="cannot be combined"):
        orchestrator.run_careerbridge_xai(
            candidate,
            evidence_mode="zetaris_snapshot",
            require_live_evidence=True,
        )

    with pytest.raises(ValueError, match="cannot be combined"):
        orchestrator.run_careerbridge_xai(
            candidate,
            evidence_mode="zetaris_snapshot",
            include_live_jobs=True,
        )

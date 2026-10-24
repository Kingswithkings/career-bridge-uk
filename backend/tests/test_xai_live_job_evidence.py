"""Tests for Adzuna normalization and the distinction between mentions and requirements."""

import sys
from types import SimpleNamespace

from backend.app.xai.agents.live_job_agent import retrieve_live_job_evidence
from backend.app.xai.agents.evaluation_agent import evaluate_job_match
from backend.app.xai.schemas import CareerProfile, JobEvidence


def test_adzuna_adapter_preserves_provenance_and_unverified_status(monkeypatch):
    captured = {}

    def fake_search(*, query, location, results_per_page):
        captured.update(query=query, location=location, limit=results_per_page)
        return {
            "results": [
                {
                    "title": "AI Engineer",
                    "company": "Example UK Ltd",
                    "redirect_url": "https://example.org/jobs/abc",
                    "description": "<p>Build with Python and Docker.</p>",
                }
            ]
        }

    monkeypatch.setitem(
        sys.modules,
        "backend.app.services.job_search_service",
        SimpleNamespace(search_live_jobs=fake_search),
    )
    records = retrieve_live_job_evidence("AI Engineer", limit=2, location="Leeds")
    assert captured == {"query": "AI Engineer", "location": "Leeds", "limit": 2}
    assert len(records) == 1
    assert records[0]["job_id"].startswith("ADZ-")
    assert records[0]["required_skills"] == ["Python", "Docker"]
    assert records[0]["skill_evidence_method"] == "description_keyword_mentions"
    assert records[0]["verified_live_vacancy"] is False
    assert records[0]["source_url"] == "https://example.org/jobs/abc"


def test_keyword_coverage_is_not_labeled_verified_requirement_coverage():
    profile = CareerProfile(skills=["Python"], career_goal="AI Engineer")
    job = JobEvidence(
        job_id="ADZ-001",
        title="AI Engineer",
        company="Example UK Ltd",
        required_skills=["Python", "Docker"],
        source_url="https://example.org/jobs/abc",
    )
    result = evaluate_job_match(
        profile,
        job,
        evidence_origin="adzuna",
        source_type="live_listing_unverified",
        skill_evidence_method="description_keyword_mentions",
    )
    assert result["skill_match_percentage"] == 50.0
    assert result["metric_label"] == "skill mention coverage"
    assert result["verified_live_vacancy"] is False
    assert any("not independently verified employer requirements" in text for text in result["evidence_warnings"])

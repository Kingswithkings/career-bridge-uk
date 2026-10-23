"""Regression tests for evidence integrity and multi-source investigations."""

from backend.app.xai.agents.investigation_agent import (
    critique_sources,
    investigate_career_evidence,
)
from backend.app.xai.agents.live_job_agent import extract_skill_mentions
from backend.app.xai.schemas import CareerProfile


def test_extraction_reports_mentions_not_inferred_requirements():
    text = "<p>Our Python team uses FastAPI. Experience with Docker is helpful.</p>"
    assert extract_skill_mentions(text) == ["Python", "FastAPI", "Docker"]
    assert "Azure" not in extract_skill_mentions(text)


def test_sample_only_is_not_sufficient_for_cross_source_inference():
    evidence = [
        {
            "job_id": "DEMO-001",
            "evidence_origin": "zetaris",
            "source_type": "sample",
            "required_skills": ["Python"],
        }
    ]
    critique = critique_sources(evidence)
    assert critique["needs_additional_source"] is True
    assert critique["sufficient_for_cross_source_inference"] is False
    assert critique["sample_count"] == 1
    assert any("sample" in message for message in critique["limitations"])


def test_investigation_cites_each_skill_gap_and_never_infers_rejection_reason():
    profile = CareerProfile(skills=["Python"], career_goal="AI Engineer")
    records = [
        {
            "job_id": "DEMO-001",
            "evidence_origin": "zetaris",
            "source_type": "sample",
            "source_url": None,
            "required_skills": ["Python", "Docker"],
        },
        {
            "job_id": "ADZ-001",
            "evidence_origin": "adzuna",
            "source_type": "live_listing_unverified",
            "source_url": "https://example.org/job/1",
            "skill_evidence_method": "description_keyword_mentions",
            "required_skills": ["Python", "Docker", "Azure"],
        },
    ]
    results = [
        {"job_id": "DEMO-001", "evaluation": {"missing_skills": ["Docker"]}},
        {"job_id": "ADZ-001", "evaluation": {"missing_skills": ["Docker", "Azure"]}},
    ]
    finding = investigate_career_evidence(profile, results, records, question="Why?")
    assert finding["source_critique"]["provider_count"] == 2
    assert finding["source_critique"]["sufficient_for_cross_source_inference"] is True
    assert finding["priority_skill_gaps"][0]["skill"] == "Docker"
    assert finding["priority_skill_gaps"][0]["jobs_mentioning_gap"] == 2
    refs = finding["priority_skill_gaps"][0]["evidence_references"]
    assert {ref["job_id"] for ref in refs} == {"DEMO-001", "ADZ-001"}
    assert next(ref for ref in refs if ref["job_id"] == "ADZ-001")["evidence_method"] == "description_keyword_mentions"
    assert "does not establish why" in finding["conclusion"]
    assert any("not proof" in warning for warning in finding["boundaries"])


def test_no_evidence_abstains():
    profile = CareerProfile(skills=[], career_goal="AI Engineer")
    result = investigate_career_evidence(profile, [], [])
    assert result["priority_skill_gaps"] == []
    assert result["conclusion"].startswith("Insufficient evidence")

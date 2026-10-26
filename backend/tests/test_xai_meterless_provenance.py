"""Verify source provenance using the real Meterless TypeScript bridge."""

import pytest

from backend.app.xai.integrations.meterless_client import build_meterless_graph


@pytest.mark.parametrize(
    "origin,channel,freshness,expected_agent",
    [
        (
            "adzuna",
            None,
            None,
            "careerbridge-adzuna-evidence-agent",
        ),
        (
            "adzuna",
            "zetaris",
            "stored_snapshot",
            "careerbridge-adzuna-zetaris-snapshot-evidence-agent",
        ),
        (
            "demo",
            None,
            None,
            "careerbridge-demo-evidence-agent",
        ),
    ],
)
def test_meterless_preserves_source_provenance(
    origin, channel, freshness, expected_agent
):
    record = {
        "job_id": f"TEST-{origin}-{channel or 'direct'}",
        "job_title": "AI Engineer",
        "company": "Example Employer",
        "required_skills": ["Python", "FastAPI"],
        "source_type": ("sample" if origin == "demo" else "live_listing_unverified"),
        "evidence_origin": origin,
        "source_url": (None if origin == "demo" else "https://example.com/jobs/123"),
        "collected_at": "2026-10-25T23:00:00+00:00",
    }

    if channel is not None:
        record["retrieval_channel"] = channel

    if freshness is not None:
        record["evidence_freshness"] = freshness

    result = build_meterless_graph([record])

    assert result["engine"] == "Meterless World Model"
    assert result["jobs_received"] == 1

    graph = result["evidence_graph"]

    assert len(graph["jobs"]) == 1

    job = graph["jobs"][0]

    assert job["provenance"]["by"] == expected_agent
    assert job["provenance"]["kind"] == "pipeline"
    assert set(job["skills"]) == {"Python", "FastAPI"}

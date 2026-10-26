"""Tests for timestamped Adzuna evidence retrieved through Zetaris."""

from unittest.mock import MagicMock, patch

import pytest

from backend.app.xai.agents.evidence_agent import (
    retrieve_zetaris_adzuna_evidence,
)


COLUMNS = [
    ("job_id",),
    ("job_title",),
    ("company",),
    ("skills_mentioned",),
    ("source_url",),
    ("source_type",),
    ("evidence_origin",),
    ("skill_evidence_method",),
    ("collected_at",),
]


def make_cursor(
    *,
    source_type="live_listing_unverified",
    origin="adzuna",
    url="https://example.com/jobs/123",
):
    cursor = MagicMock()
    cursor.description = COLUMNS
    cursor.fetchall.return_value = [
        (
            "ADZ-test123",
            "Machine Learning Engineer",
            "Example Employer",
            "Python | Machine Learning | Docker",
            url,
            source_type,
            origin,
            "description_keyword_mentions",
            "2026-10-25T23:00:00+00:00",
        )
    ]
    return cursor


@pytest.mark.parametrize("limit", [0, -1, 101, True, "5"])
def test_invalid_limit_rejected(limit):
    with pytest.raises(ValueError):
        retrieve_zetaris_adzuna_evidence(limit=limit)


@patch("backend.app.xai.agents.evidence_agent.zetaris_connection")
def test_retrieve_adzuna_snapshot(mock_connection):
    cursor = make_cursor()
    connection = MagicMock()
    connection.cursor.return_value = cursor
    mock_connection.return_value.__enter__.return_value = connection

    records = retrieve_zetaris_adzuna_evidence(limit=10)

    assert len(records) == 1

    record = records[0]

    assert record["job_id"] == "ADZ-test123"
    assert record["required_skills"] == [
        "Python",
        "Machine Learning",
        "Docker",
    ]
    assert record["evidence_origin"] == "adzuna"
    assert record["retrieval_channel"] == "zetaris"
    assert record["evidence_freshness"] == "stored_snapshot"
    assert record["source_type"] == "live_listing_unverified"
    assert record["verified_live_vacancy"] is False
    assert record["collected_at"] == "2026-10-25T23:00:00+00:00"

    assert "CAREERBRIDGE_ADZUNA.careerbridge_adzuna_evidence" in (
        cursor.execute.call_args.args[0]
    )
    cursor.close.assert_called_once()


@pytest.mark.parametrize(
    "source_type,origin,url",
    [
        ("sample", "adzuna", "https://example.com/jobs/123"),
        ("live_listing_unverified", "demo", "https://example.com/jobs/123"),
        ("live_listing_unverified", "adzuna", "invalid-url"),
    ],
)
@patch("backend.app.xai.agents.evidence_agent.zetaris_connection")
def test_invalid_provenance_rejected(mock_connection, source_type, origin, url):
    cursor = make_cursor(
        source_type=source_type,
        origin=origin,
        url=url,
    )
    connection = MagicMock()
    connection.cursor.return_value = cursor
    mock_connection.return_value.__enter__.return_value = connection

    with pytest.raises(ValueError):
        retrieve_zetaris_adzuna_evidence(limit=10)

    cursor.close.assert_called_once()

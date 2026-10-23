from unittest.mock import MagicMock, patch

import pytest

from backend.app.xai.agents.evidence_agent import (
    parse_postgres_array,
    retrieve_job_evidence,
)


def test_parse_postgres_skills():
    result = parse_postgres_array(
        '{Python,FastAPI,"Machine Learning",LLMs}'
    )
    assert result == [
        "Python",
        "FastAPI",
        "Machine Learning",
        "LLMs",
    ]


def test_parse_empty_skills():
    assert parse_postgres_array("{}") == []
    assert parse_postgres_array(None) == []


def test_reject_invalid_limit():
    for limit in [0, 101, -1, True, "3"]:
        with pytest.raises(ValueError):
            retrieve_job_evidence(limit=limit)


@patch(
    "backend.app.xai.agents.evidence_agent.zetaris_connection"
)
def test_retrieve_evidence(mock_connection):
    cursor = MagicMock()
    cursor.description = [
        ("job_id",),
        ("job_title",),
        ("company",),
        ("required_skills",),
        ("experience_years",),
        ("source_url",),
        ("source_type",),
        ("collected_at",),
    ]
    cursor.fetchall.return_value = [
        (
            "DEMO-001",
            "AI Engineer",
            "Demo Technology Ltd",
            "{Python,FastAPI}",
            2.0,
            None,
            "sample",
            "2026-10-22",
        )
    ]

    connection = MagicMock()
    connection.cursor.return_value = cursor
    mock_connection.return_value.__enter__.return_value = connection

    result = retrieve_job_evidence(limit=3)

    assert len(result) == 1
    assert result[0]["job_id"] == "DEMO-001"
    assert result[0]["required_skills"] == ["Python", "FastAPI"]
    assert result[0]["evidence_origin"] == "zetaris"
    assert result[0]["verified_live_vacancy"] is False
    cursor.execute.assert_called_once()
    cursor.close.assert_called_once()


def test_normalize_naive_postgres_timestamp():
    from backend.app.xai.agents.evidence_agent import normalize_collected_at

    result = normalize_collected_at("2026-10-22 06:59:54.842174")
    assert result == "2026-10-22T06:59:54.842174+00:00"


def test_normalize_timezone_aware_timestamp():
    from backend.app.xai.agents.evidence_agent import normalize_collected_at

    result = normalize_collected_at("2026-10-22T07:59:54+01:00")
    assert result == "2026-10-22T06:59:54+00:00"


def test_reject_invalid_timestamp():
    from backend.app.xai.agents.evidence_agent import normalize_collected_at

    with pytest.raises(ValueError):
        normalize_collected_at("invalid-timestamp")

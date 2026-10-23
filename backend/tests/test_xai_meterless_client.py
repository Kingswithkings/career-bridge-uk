"""Tests for the Meterless World Model adapter."""

import json
from unittest.mock import MagicMock, patch

import pytest

from backend.app.xai.integrations.meterless_client import build_meterless_graph


@pytest.fixture
def sample_records():
    return [
        {
            "job_id": "DEMO-001",
            "job_title": "AI Engineer",
            "company": "Demo Technology Ltd",
            "required_skills": ["Python", "FastAPI"],
            "source_type": "sample",
            "source_url": None,
            "collected_at": "2026-10-22T06:59:54+00:00",
        }
    ]


@patch("backend.app.xai.integrations.meterless_client.subprocess.run")
def test_meterless_graph_success(mock_run, sample_records):
    payload = {
        "engine": "Meterless World Model",
        "jobs_received": 1,
        "evidence_graph": {
            "jobs": [
                {
                    "id": "job:ingest:zetaris:DEMO-001",
                    "title": "AI Engineer",
                    "skills": ["Python", "FastAPI"],
                    "provenance": {
                        "kind": "pipeline",
                        "at": "2026-10-22T06:59:54.000Z",
                    },
                }
            ],
            "relationship_count": 2,
        },
    }

    mock_run.return_value = MagicMock(stdout=json.dumps(payload))

    result = build_meterless_graph(sample_records)

    assert result["jobs_received"] == 1
    assert result["evidence_graph"]["relationship_count"] == 2
    mock_run.assert_called_once()


@patch("backend.app.xai.integrations.meterless_client.subprocess.run")
def test_meterless_rejects_invalid_json(mock_run, sample_records):
    mock_run.return_value = MagicMock(stdout="not-json")

    with pytest.raises(RuntimeError, match="invalid JSON"):
        build_meterless_graph(sample_records)


@patch("backend.app.xai.integrations.meterless_client.subprocess.run")
def test_meterless_rejects_missing_graph(mock_run, sample_records):
    mock_run.return_value = MagicMock(
        stdout=json.dumps({
            "engine": "Meterless World Model",
            "jobs_received": 1,
        })
    )

    with pytest.raises(RuntimeError, match="unexpected response"):
        build_meterless_graph(sample_records)


def test_meterless_rejects_empty_records():
    with pytest.raises(ValueError):
        build_meterless_graph([])

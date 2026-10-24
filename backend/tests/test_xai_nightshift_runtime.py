"""Nightshift tests never use real tokens, networks or provider credentials."""

import sys
from types import SimpleNamespace

from backend.app.xai.integrations.nightshift_runtime import request_nightshift_insight


INVESTIGATION = {
    "question": "Which evidence-backed skills are missing?",
    "candidate_goal": "AI Engineer",
    "conclusion": "Sample-only results are inconclusive.",
    "source_critique": {"sample_count": 1, "non_sample_count": 0},
    "priority_skill_gaps": [],
    "boundaries": ["Do not imply employment rejection causes."],
}


def test_nightshift_is_disabled_by_default(monkeypatch):
    monkeypatch.delenv("XAI_ENABLE_NIGHTSHIFT", raising=False)
    assert request_nightshift_insight(INVESTIGATION) == {
        "status": "disabled",
        "used": False,
    }


def test_nightshift_uses_only_runtime_token_and_expected_headers(monkeypatch):
    monkeypatch.setenv("XAI_ENABLE_NIGHTSHIFT", "true")
    monkeypatch.setenv("METERLESS_RUNTIME_TOKEN", "fake-runtime-token")
    options = {}

    class FakeCompletions:
        def create(self, **kwargs):
            options["request"] = kwargs
            return SimpleNamespace(
                choices=[SimpleNamespace(message=SimpleNamespace(content="Grounded summary."))],
                model="meterless/testing",
            )

    class FakeClient:
        def __init__(self, **kwargs):
            options["client"] = kwargs
            self.chat = SimpleNamespace(completions=FakeCompletions())

    monkeypatch.setitem(sys.modules, "openai", SimpleNamespace(OpenAI=FakeClient))
    response = request_nightshift_insight(INVESTIGATION)
    assert response["status"] == "success"
    assert response["used"] is True
    assert response["independently_verified"] is False
    assert options["client"]["api_key"] == "fake-runtime-token"
    assert options["client"]["default_headers"]["meterless-app"] == "careerbridge-xai"
    assert options["client"]["default_headers"]["meterless-scope"] == "user"
    assert options["request"]["model"] == "meterless/auto"
    assert "fake-runtime-token" not in str(response)


def test_runtime_401_fails_closed(monkeypatch):
    monkeypatch.setenv("XAI_ENABLE_NIGHTSHIFT", "true")
    monkeypatch.setenv("METERLESS_RUNTIME_TOKEN", "fake-runtime-token")

    class Unauthorized(Exception):
        status_code = 401

    class FakeClient:
        def __init__(self, **kwargs):
            self.chat = SimpleNamespace(
                completions=SimpleNamespace(create=lambda **kwargs: (_ for _ in ()).throw(Unauthorized()))
            )

    monkeypatch.setitem(sys.modules, "openai", SimpleNamespace(OpenAI=FakeClient))
    response = request_nightshift_insight(INVESTIGATION)
    assert response["status"] == "authentication_failed"
    assert response["used"] is False
    assert "fake-runtime-token" not in str(response)

"""Verify that NVIDIA inference cannot be requested anonymously."""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from backend.app.api.routes import xai_routes
from backend.app.limiter import limiter


def make_client():
    app = FastAPI()
    app.state.limiter = limiter
    app.include_router(xai_routes.router)
    return TestClient(app)


PAYLOAD = {
    "candidate": {
        "skills": ["Python"],
        "career_goal": "AI Engineer",
    },
    "include_nvidia_insight": True,
}


def test_nvidia_api_disabled_by_default(monkeypatch):
    monkeypatch.delenv("XAI_ENABLE_NVIDIA_API", raising=False)
    client = make_client()

    response = client.post("/api/xai/run", json=PAYLOAD)

    assert response.status_code == 403


def test_nvidia_api_requires_authentication(monkeypatch):
    monkeypatch.setenv("XAI_ENABLE_NVIDIA_API", "true")
    client = make_client()

    response = client.post("/api/xai/run", json=PAYLOAD)

    assert response.status_code == 401


def test_authenticated_nvidia_request_reaches_orchestrator(monkeypatch, tmp_path):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    from backend.app.api.dependencies import get_db
    from backend.app.database import Base
    from backend.app.models.user_model import User
    from backend.app.utils.security import create_access_token

    monkeypatch.setenv("XAI_ENABLE_NVIDIA_API", "true")

    engine = create_engine(
        f"sqlite:///{tmp_path / 'xai-auth-test.sqlite3'}",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)

    with SessionLocal() as session:
        session.add(
            User(
                email="xai-test@example.com",
                hashed_password="test-only-not-used",
            )
        )
        session.commit()

    def override_db():
        with SessionLocal() as session:
            yield session

    calls = []

    def fake_orchestrator(**kwargs):
        calls.append(kwargs)
        return {
            "nvidia": {
                "status": "mocked_success",
                "used": True,
                "advisory_narrative": "Test explanation.",
                "independently_verified": False,
            }
        }

    monkeypatch.setattr(
        xai_routes,
        "run_careerbridge_xai",
        fake_orchestrator,
    )

    app = FastAPI()
    app.state.limiter = limiter
    app.include_router(xai_routes.router)
    app.dependency_overrides[get_db] = override_db

    token = create_access_token({"sub": "xai-test@example.com"})

    try:
        with TestClient(app) as client:
            response = client.post(
                "/api/xai/run",
                json=PAYLOAD,
                headers={"Authorization": f"Bearer {token}"},
            )

        assert response.status_code == 200, response.text
        assert calls
        assert calls[0]["include_nvidia_insight"] is True
        assert response.json()["nvidia"]["status"] == "mocked_success"
    finally:
        engine.dispose()


def test_capabilities_require_both_flags_and_key(monkeypatch):
    monkeypatch.delenv("XAI_ENABLE_NVIDIA_API", raising=False)
    monkeypatch.setenv("XAI_ENABLE_NVIDIA", "true")
    monkeypatch.setenv("NVIDIA_API_KEY", "test-only-secret")
    client = make_client()
    assert client.get("/api/xai/capabilities").json() == {"nvidia_available": False}
    monkeypatch.setenv("XAI_ENABLE_NVIDIA_API", "true")
    assert client.get("/api/xai/capabilities").json() == {"nvidia_available": True}
    monkeypatch.delenv("NVIDIA_API_KEY")
    assert client.get("/api/xai/capabilities").json() == {"nvidia_available": False}


def test_live_only_api_rejects_false():
    import pytest
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        xai_routes.XAIRunRequest.model_validate(
            {
                "candidate": {
                    "skills": ["Python"],
                    "career_goal": "AI Engineer",
                },
                "include_live_jobs": False,
            }
        )

import requests
import streamlit as st

BASE_URL = "http://127.0.0.1:8000"
TIMEOUT_SECONDS = 60


def get_headers():
    token = st.session_state.get("token")

    if token:
        return {"Authorization": f"Bearer {token}"}

    return {}


def post_json(path, data):
    try:
        response = requests.post(
            f"{BASE_URL}{path}",
            json=data,
            headers=get_headers(),
            timeout=TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(
            "Backend is not running. Start it with: "
            "backend/.venv/bin/uvicorn backend.app.main:app --reload"
        ) from exc
    except requests.exceptions.HTTPError as exc:
        try:
            detail = response.json()
        except ValueError:
            detail = response.text
        raise RuntimeError(f"Backend returned {response.status_code}: {detail}") from exc
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"Request failed: {exc}") from exc


def get_json(path):
    try:
        response = requests.get(
            f"{BASE_URL}{path}",
            headers=get_headers(),
            timeout=TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(
            "Backend is not running. Start it with: "
            "backend/.venv/bin/uvicorn backend.app.main:app --reload"
        ) from exc
    except requests.exceptions.HTTPError as exc:
        try:
            detail = response.json()
        except ValueError:
            detail = response.text
        raise RuntimeError(f"Backend returned {response.status_code}: {detail}") from exc
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"Request failed: {exc}") from exc


def analyze_cv(data):
    return post_json("/api/cv/analyze", data)


def generate_cv(data):
    return post_json("/api/cv/generate", data)


def prepare_interview(data):
    return post_json("/api/interview/prepare", data)


def mock_interview(data):
    return post_json("/api/interview/mock", data)


def match_job(data):
    return post_json("/api/jobs/match", data)


def save_result(data):
    return post_json("/api/results/save", data)


def get_results():
    return get_json("/api/results/")


def register_user(data):
    try:
        return post_json("/api/auth/register", data)
    except RuntimeError as exc:
        return {"detail": str(exc)}


def login_user(data):
    try:
        return post_json("/api/auth/login", data)
    except RuntimeError as exc:
        return {"detail": str(exc)}


def search_jobs(data):
    try:
        return post_json("/api/jobs/search", data)
    except RuntimeError as exc:
        return {"detail": str(exc)}

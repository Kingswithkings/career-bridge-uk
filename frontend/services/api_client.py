import os

import requests
import streamlit as st

DEFAULT_BACKEND_URL = "https://career-bridge-uk.onrender.com"
TIMEOUT_SECONDS = 60


def get_base_url():
    backend_url = os.getenv("BACKEND_URL")
    if backend_url:
        return backend_url.rstrip("/")

    try:
        return st.secrets.get("BACKEND_URL", DEFAULT_BACKEND_URL).rstrip("/")
    except (FileNotFoundError, KeyError):
        return DEFAULT_BACKEND_URL


def get_headers():
    token = st.session_state.get("token")

    if token:
        return {"Authorization": f"Bearer {token}"}

    return {}


def post_json(path, data):
    try:
        response = requests.post(
            f"{get_base_url()}{path}",
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
            f"{get_base_url()}{path}",
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


def generate_cv_from_analysis(data):
    return post_json("/api/cv/generate-from-analysis", data)


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


def health_check():
    return get_json("/health")


def register_user(data):
    try:
        return post_json("/api/auth/register", data)
    except RuntimeError as exc:
        message = str(exc)
        if "Backend returned 400" in message and "Email already registered" in message:
            return {
                "detail": "That email is already registered. Use the Login tab with the password you created.",
                "status_code": 400,
            }
        return {"detail": message}


def login_user(data):
    try:
        return post_json("/api/auth/login", data)
    except RuntimeError as exc:
        message = str(exc)
        if "Backend returned 401" in message and "Invalid email or password" in message:
            return {
                "detail": (
                    "Invalid email or password. If this is your first time using the deployed app, "
                    "create an account in the Register tab first."
                ),
                "status_code": 401,
            }
        return {"detail": message}


def search_jobs(data):
    try:
        return post_json("/api/jobs/search", data)
    except RuntimeError as exc:
        return {"detail": str(exc)}

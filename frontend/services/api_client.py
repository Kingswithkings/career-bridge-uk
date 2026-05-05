import requests

BASE_URL = "http://127.0.0.1:8000"
TIMEOUT_SECONDS = 60


def post_json(path, data):
    try:
        response = requests.post(
            f"{BASE_URL}{path}",
            json=data,
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

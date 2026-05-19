import requests
from fastapi import HTTPException

from ..config import ADZUNA_APP_ID, ADZUNA_APP_KEY

UK_LOCATION_PARTS = {"gb", "uk", "united kingdom", "great britain", "england", "scotland", "wales"}
REMOTE_LOCATION_PARTS = {"remote", "hybrid"}


def _normalize_location(location: str | None) -> str | None:
    if not location:
        return None

    location_parts = [
        part.strip()
        for part in location.split(",")
        if part.strip() and part.strip().lower() not in UK_LOCATION_PARTS
    ]

    if not location_parts:
        return None

    normalized = location_parts[0]

    if normalized.lower() in REMOTE_LOCATION_PARTS:
        return None

    return normalized


def _request_jobs(params: dict):
    response = requests.get(
        f"https://api.adzuna.com/v1/api/jobs/gb/search/{params.pop('page')}",
        params=params,
        timeout=20,
    )

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Adzuna API error: {response.text}",
        )

    return response.json()


def search_live_jobs(
    query: str,
    location: str | None = None,
    page: int = 1,
    results_per_page: int = 10,
):
    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        raise HTTPException(
            status_code=500,
            detail=(
                "Adzuna API credentials are missing. Add ADZUNA_APP_ID and "
                "ADZUNA_APP_KEY to .env"
            ),
        )

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "page": page,
        "results_per_page": results_per_page,
        "what": query.strip(),
        "content-type": "application/json",
        "distance": 30,
    }

    normalized_location = _normalize_location(location)

    if normalized_location:
        params["where"] = normalized_location

    data = _request_jobs(params.copy())

    if data.get("count", 0) == 0 and normalized_location:
        fallback_params = params.copy()
        fallback_params.pop("where", None)
        data = _request_jobs(fallback_params)

    jobs = []

    for item in data.get("results", []):
        jobs.append(
            {
                "title": item.get("title"),
                "company": item.get("company", {}).get("display_name"),
                "location": item.get("location", {}).get("display_name"),
                "salary_min": item.get("salary_min"),
                "salary_max": item.get("salary_max"),
                "description": item.get("description"),
                "redirect_url": item.get("redirect_url"),
                "created": item.get("created"),
            }
        )

    return {
        "count": data.get("count", 0),
        "results": jobs,
    }

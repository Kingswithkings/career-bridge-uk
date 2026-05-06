import requests
from fastapi import HTTPException

from ..config import ADZUNA_APP_ID, ADZUNA_APP_KEY


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

    url = f"https://api.adzuna.com/v1/api/jobs/gb/search/{page}"

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": results_per_page,
        "what": query,
        "content-type": "application/json",
    }

    if location:
        params["where"] = location

    response = requests.get(url, params=params, timeout=20)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Adzuna API error: {response.text}",
        )

    data = response.json()
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

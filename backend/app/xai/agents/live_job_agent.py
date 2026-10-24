"""Read Adzuna listings without mistaking keyword mentions for verified requirements."""

from datetime import datetime, timezone
from hashlib import sha256
from html import unescape
import re

# Conservative, transparent vocabulary. Matches are mentions, NOT inferred requirements.
SKILL_VOCABULARY = (
    "Python", "FastAPI", "Django", "Flask", "SQL", "PostgreSQL", "Docker",
    "Kubernetes", "AWS", "Azure", "GCP", "Machine Learning", "Deep Learning",
    "NLP", "LLMs", "RAG", "PyTorch", "TensorFlow", "Git", "CI/CD",
    "JavaScript", "TypeScript", "React", "Next.js", "Java", "C++", "Spark",
    "ETL", "Data Engineering", "Computer Vision", "MLOps", "Terraform",
)


def extract_skill_mentions(description: str) -> list[str]:
    """Return explicit phrase mentions only; this is not requirement extraction."""
    plain = unescape(re.sub(r"<[^>]*>", " ", description or ""))
    return [
        skill for skill in SKILL_VOCABULARY
        if re.search(r"(?<![\w])" + re.escape(skill) + r"(?![\w])", plain, re.I)
    ]


def extract_skill_contexts(description: str) -> dict[str, str]:
    """Verify skill mentions against retrieved text and retain short excerpts.

    These excerpts are evidence of mentions, not verified job requirements.
    """
    plain = " ".join(
        unescape(re.sub(r"<[^>]*>", " ", description or "")).split()
    )
    contexts = {}

    for skill in extract_skill_mentions(description):
        match = re.search(
            r"(?<![\w])" + re.escape(skill) + r"(?![\w])",
            plain,
            re.I,
        )
        if match:
            start = max(0, match.start() - 80)
            end = min(len(plain), match.end() + 80)
            contexts[skill] = plain[start:end]

    return contexts


def retrieve_live_job_evidence(goal: str, *, limit: int = 5, location: str | None = None) -> list[dict]:
    """Read actual Adzuna search results. Does not claim vacancies are independently verified."""
    # Keep the existing application dependency isolated from deterministic/offline tests.
    from backend.app.services.job_search_service import search_live_jobs

    response = search_live_jobs(query=goal, location=location, results_per_page=limit)
    collected = datetime.now(timezone.utc).isoformat()
    records = []
    for job in response.get("results", []):
        url = (job.get("redirect_url") or "").strip()
        title = (job.get("title") or "").strip()
        if not title or not url.startswith(("https://", "http://")):
            continue
        company = (job.get("company") or "Unknown employer").strip()
        # Adzuna's search service exposes summaries, not a verified requirements schema.
        mentions = extract_skill_mentions(job.get("description") or "")
        if not mentions:
            continue  # No measurable skills; don't manufacture them.
        job_id = "ADZ-" + sha256(url.encode("utf-8")).hexdigest()[:12]
        records.append({
            "job_id": job_id,
            "job_title": title,
            "company": company,
            "required_skills": mentions,
            "source_url": url,
            "source_type": "live_listing_unverified",
            "evidence_origin": "adzuna",
            "skill_evidence_method": "description_keyword_mentions",
            "skill_contexts": extract_skill_contexts(
                job.get("description") or ""
            ),
            "collected_at": collected,
            "verified_live_vacancy": False,
        })
    return records

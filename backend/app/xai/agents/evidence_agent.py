from datetime import datetime, timezone
import re

from backend.app.xai.integrations.zetaris_client import zetaris_connection


def parse_postgres_array(value):
    """Parse simple PostgreSQL text arrays of skills."""
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return list(value)

    import csv
    import io

    text = str(value)
    if not (text.startswith("{") and text.endswith("}")):
        raise ValueError("Unexpected required_skills format")

    return next(
        csv.reader(io.StringIO(text[1:-1]), skipinitialspace=True),
        [],
    )



def normalize_collected_at(value):
    """Normalize timestamps from the verified UTC PostgreSQL source."""
    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, str):
        parsed = datetime.fromisoformat(
            value.strip().replace("Z", "+00:00")
        )
    else:
        raise ValueError("Unsupported collected_at timestamp")

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)

    return parsed.astimezone(timezone.utc).isoformat()

def retrieve_job_evidence(limit=10):
    """Retrieve sample job evidence through Zetaris JDBC."""
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= 100:
        raise ValueError("limit must be an integer between 1 and 100")

    query = (
        "SELECT job_id, job_title, company, required_skills, "
        "experience_years, source_url, source_type, collected_at "
        "FROM CAREERBRIDGE_XAI.job_evidence "
        f"LIMIT {limit}"
    )

    with zetaris_connection() as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            columns = [column[0].lower() for column in cursor.description]
            rows = cursor.fetchall()
        finally:
            cursor.close()

    evidence = []
    for row in rows:
        record = dict(zip(columns, row))
        record["required_skills"] = parse_postgres_array(
            record["required_skills"]
        )
        record["collected_at"] = normalize_collected_at(
            record["collected_at"]
        )
        record["evidence_origin"] = "zetaris"
        record["verified_live_vacancy"] = False
        evidence.append(record)

    return evidence

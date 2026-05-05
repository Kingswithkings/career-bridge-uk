from pydantic import BaseModel


class JobMatchRequest(BaseModel):
    cv_text: str
    target_role: str
    job_description: str
    location: str | None = None
    experience_level: str | None = "Entry-level"


class JobMatchResponse(BaseModel):
    match_result: str
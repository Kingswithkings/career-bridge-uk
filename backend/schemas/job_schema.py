from pydantic import BaseModel, Field


class JobMatchRequest(BaseModel):
    cv_text: str
    target_role: str
    job_description: str
    location: str | None = None
    experience_level: str | None = "Entry-level"


class MatchedJobItem(BaseModel):
    title: str | None = None
    company: str | None = None
    location: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    description: str | None = None
    redirect_url: str | None = None
    created: str | None = None


class JobMatchResponse(BaseModel):
    match_result: str
    matched_jobs: list[MatchedJobItem] = Field(default_factory=list)
    jobs_count: int = 0

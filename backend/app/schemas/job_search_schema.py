from pydantic import BaseModel


class JobSearchRequest(BaseModel):
    query: str
    location: str | None = None
    page: int = 1
    results_per_page: int = 10


class JobItem(BaseModel):
    title: str | None = None
    company: str | None = None
    location: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    description: str | None = None
    redirect_url: str | None = None
    created: str | None = None


class JobSearchResponse(BaseModel):
    count: int
    results: list[JobItem]

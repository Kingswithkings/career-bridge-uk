
from pydantic import BaseModel, Field


class CareerProfile(BaseModel):
    skills: list[str] = Field(default_factory=list)
    experience_years: float = Field(default=0, ge=0)
    education: list[str] = Field(default_factory=list)
    career_goal: str = Field(min_length=1)


class JobEvidence(BaseModel):
    job_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    company: str = Field(min_length=1)
    required_skills: list[str] = Field(default_factory=list)
    source_url: str | None = None


class XAIRequest(BaseModel):
    candidate: CareerProfile
    jobs: list[JobEvidence] = Field(min_length=1)

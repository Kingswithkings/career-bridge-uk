"""API endpoints for CareerBridge XAI."""

from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.app.xai.orchestrator import run_careerbridge_xai
from backend.app.xai.schemas import CareerProfile

router = APIRouter(prefix="/api/xai", tags=["CareerBridge XAI"])


class XAIRunRequest(BaseModel):
    candidate: CareerProfile
    limit: int = Field(default=3, ge=1, le=100)
    include_live_jobs: bool = False
    location: str | None = None
    question: str | None = Field(default=None, max_length=500)


@router.post("/run")
def run_xai(request: XAIRunRequest):
    return run_careerbridge_xai(
        candidate=request.candidate,
        limit=request.limit,
        include_live_jobs=request.include_live_jobs,
        location=request.location,
        question=request.question,
    )

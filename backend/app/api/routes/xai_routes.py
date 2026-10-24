"""API endpoints for CareerBridge XAI."""

import os

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.app.api.dependencies import get_current_user
from backend.app.database import get_db
from backend.app.limiter import limiter

from backend.app.xai.orchestrator import run_careerbridge_xai
from backend.app.xai.schemas import CareerProfile

router = APIRouter(prefix="/api/xai", tags=["CareerBridge XAI"])
optional_bearer = HTTPBearer(auto_error=False)


class XAIRunRequest(BaseModel):
    candidate: CareerProfile
    limit: int = Field(default=3, ge=1, le=100)
    include_live_jobs: bool = False
    include_nvidia_insight: bool = False
    location: str | None = None
    question: str | None = Field(default=None, max_length=500)


@router.post("/run")
@limiter.limit("5/minute")
def run_xai(
    request: Request,
    payload: XAIRunRequest,
    credentials: HTTPAuthorizationCredentials | None = Depends(optional_bearer),
    db: Session = Depends(get_db),
):
    if payload.include_nvidia_insight:
        enabled = os.getenv(
            "XAI_ENABLE_NVIDIA_API", ""
        ).lower() in {"true", "1", "yes"}

        if not enabled:
            raise HTTPException(
                status_code=403,
                detail="NVIDIA inference is disabled for API requests.",
            )

        if credentials is None:
            raise HTTPException(
                status_code=401,
                detail="Login required for NVIDIA inference.",
            )

        get_current_user(credentials=credentials, db=db)

    return run_careerbridge_xai(
        candidate=payload.candidate,
        limit=payload.limit,
        include_live_jobs=payload.include_live_jobs,
        location=payload.location,
        question=payload.question,
        include_nvidia_insight=payload.include_nvidia_insight,
    )

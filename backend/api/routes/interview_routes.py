from fastapi import APIRouter, HTTPException

from backend.schemas.interview_schema import (
    InterviewPreparationRequest,
    InterviewPreparationResponse,
)
from backend.services.interview_service import prepare_interview

router = APIRouter(prefix="/api/interview", tags=["Interview"])


@router.post("/prepare", response_model=InterviewPreparationResponse)
def prepare_candidate_interview(request: InterviewPreparationRequest):
    try:
        result = prepare_interview(
            cv_text=request.cv_text,
            target_role=request.target_role,
            job_description=request.job_description,
            location=request.location,
            experience_level=request.experience_level,
            interview_style=request.interview_style,
        )

        return InterviewPreparationResponse(preparation=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

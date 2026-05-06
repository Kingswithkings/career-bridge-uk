from fastapi import APIRouter, Depends, HTTPException

from ...api.dependencies import get_current_user
from ...services.job_match_service import match_job


try:
    from backend.schemas.job_schema import JobMatchRequest, JobMatchResponse
except ModuleNotFoundError:
    from schemas.job_schema import JobMatchRequest, JobMatchResponse

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])


@router.post("/match", response_model=JobMatchResponse)
def match_candidate_to_job(
    request: JobMatchRequest,
    _current_user=Depends(get_current_user),
):

    try:
        result = match_job(
            cv_text=request.cv_text,
            target_role=request.target_role,
            job_description=request.job_description,
            location=request.location,
            experience_level=request.experience_level,
        )
        return JobMatchResponse(match_result=result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

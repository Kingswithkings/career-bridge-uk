import asyncio

from fastapi import APIRouter, Depends, HTTPException

from ...api.dependencies import get_current_user
from ...posthog_client import posthog_client
from ...services.job_match_service import match_job
from ...services.job_search_service import search_live_jobs
from ...schemas.job_search_schema import JobSearchRequest, JobSearchResponse

try:
    from backend.schemas.job_schema import JobMatchRequest, JobMatchResponse
except ModuleNotFoundError:
    from schemas.job_schema import JobMatchRequest, JobMatchResponse

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])


@router.post("/match", response_model=JobMatchResponse)
async def match_candidate_to_job(
    request: JobMatchRequest,
    _current_user=Depends(get_current_user),
):

    try:
        result = await match_job(
            cv_text=request.cv_text,
            target_role=request.target_role,
            job_description=request.job_description,
            location=request.location,
            experience_level=request.experience_level,
        )
        posthog_client.capture(
            distinct_id=_current_user.email,
            event="job_matched",
            properties={
                "target_role": request.target_role,
                "experience_level": request.experience_level,
            },
        )
        return JobMatchResponse(match_result=result)
    except asyncio.TimeoutError as exc:
        raise HTTPException(
            status_code=504,
            detail="The AI response took too long. Please try again with a shorter CV or job description.",
        ) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/search", response_model=JobSearchResponse)
def search_jobs(
    request: JobSearchRequest,
    _current_user=Depends(get_current_user),
):
    try:
        result = search_live_jobs(
            query=request.query,
            location=request.location,
            page=request.page,
            results_per_page=request.results_per_page,
        )
        posthog_client.capture(
            distinct_id=_current_user.email,
            event="jobs_searched",
            properties={
                "results_per_page": request.results_per_page,
                "page": request.page,
            },
        )
        return result

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

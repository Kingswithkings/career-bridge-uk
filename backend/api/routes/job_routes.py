from fastapi import APIRouter, HTTPException

from backend.schemas.job_schema import JobMatchRequest, JobMatchResponse
from backend.services.job_match_service import match_job
from backend.services.job_search_service import search_live_jobs

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])


@router.post("/match", response_model=JobMatchResponse)
def match_candidate_to_job(request: JobMatchRequest):
    try:
        result = match_job(
            cv_text=request.cv_text,
            target_role=request.target_role,
            job_description=request.job_description,
            location=request.location,
            experience_level=request.experience_level,
        )
        jobs_result = search_live_jobs(
            query=request.target_role,
            location=request.location,
            results_per_page=10,
        )

        return JobMatchResponse(
            match_result=result,
            matched_jobs=jobs_result["results"],
            jobs_count=jobs_result["count"],
        )

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

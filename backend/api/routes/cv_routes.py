from fastapi import APIRouter, HTTPException

from app.services.cv_service import analyze_cv
from schemas.cv_schema import CVAnalysisRequest, CVAnalysisResponse

router = APIRouter(prefix="/api/cv", tags=["CV"])


@router.post("/analyze", response_model=CVAnalysisResponse)
def analyze_candidate_cv(request: CVAnalysisRequest):
    try:
        result = analyze_cv(
            cv_text=request.cv_text,
            target_role=request.target_role,
            location=request.location,
            experience_level=request.experience_level,
            visa_status=request.visa_status,
        )

        return CVAnalysisResponse(analysis=result)

    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

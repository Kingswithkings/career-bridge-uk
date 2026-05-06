from fastapi import APIRouter, Depends, HTTPException

from ...api.dependencies import get_current_user
from ...services.cv_service import (
    analyze_cv,
    generate_improved_cv_from_analysis,
    generate_uk_cv,
)

try:
    from backend.schemas.cv_schema import (
        CVAnalysisRequest,
        CVAnalysisResponse,
        CVGenerateRequest,
        CVGenerateResponse,
        ImprovedCVRequest,
        ImprovedCVResponse,
    )
except ModuleNotFoundError:
    from schemas.cv_schema import (
        CVAnalysisRequest,
        CVAnalysisResponse,
        CVGenerateRequest,
        CVGenerateResponse,
        ImprovedCVRequest,
        ImprovedCVResponse,
    )

router = APIRouter(prefix="/api/cv", tags=["CV"])


@router.post("/analyze", response_model=CVAnalysisResponse)
def analyze_candidate_cv(
    request: CVAnalysisRequest,
    _current_user=Depends(get_current_user),
):

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


@router.post("/generate", response_model=CVGenerateResponse)
def generate_candidate_cv(
    request: CVGenerateRequest,
    _current_user=Depends(get_current_user),
):

    try:
        result = generate_uk_cv(
            cv_text=request.cv_text,
            target_role=request.target_role,
            location=request.location,
            experience_level=request.experience_level,
        )
        return CVGenerateResponse(generated_cv=result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/generate-from-analysis", response_model=ImprovedCVResponse)
def generate_candidate_cv_from_analysis(
    request: ImprovedCVRequest,
    _current_user=Depends(get_current_user),
):

    try:
        result = generate_improved_cv_from_analysis(
            cv_text=request.cv_text,
            cv_analysis=request.cv_analysis,
            target_role=request.target_role,
            location=request.location,
            experience_level=request.experience_level,
        )
        return ImprovedCVResponse(improved_cv=result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

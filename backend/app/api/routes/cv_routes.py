import asyncio

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile

from ...api.dependencies import get_current_user
from ...limiter import limiter
from ...services.cv_service import (
    analyze_cv,
    generate_improved_cv_from_analysis,
    generate_uk_cv,
)
from ...utils.cv_file_parser import extract_cv_text

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


@router.post("/upload")
async def upload_candidate_cv(
    file: UploadFile = File(...),
    _current_user=Depends(get_current_user),
):
    text = await extract_cv_text(file)
    return {"filename": file.filename, "cv_text": text}


@router.post("/analyze", response_model=CVAnalysisResponse)
@limiter.limit("5/minute")
async def analyze_candidate_cv(
    request: Request,
    payload: CVAnalysisRequest,
    _current_user=Depends(get_current_user),
):

    try:
        result = await analyze_cv(
            cv_text=payload.cv_text,
            target_role=payload.target_role,
            location=payload.location,
            experience_level=payload.experience_level,
            visa_status=payload.visa_status,
        )
        return CVAnalysisResponse(analysis=result)
    except asyncio.TimeoutError as exc:
        raise HTTPException(
            status_code=504,
            detail="The AI response took too long. Please try again with a shorter CV or job target.",
        ) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/generate", response_model=CVGenerateResponse)
async def generate_candidate_cv(
    request: CVGenerateRequest,
    _current_user=Depends(get_current_user),
):

    try:
        result = await generate_uk_cv(
            cv_text=request.cv_text,
            target_role=request.target_role,
            location=request.location,
            experience_level=request.experience_level,
        )
        return CVGenerateResponse(generated_cv=result)
    except asyncio.TimeoutError as exc:
        raise HTTPException(
            status_code=504,
            detail="The AI response took too long. Please try again with a shorter CV.",
        ) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/generate-from-analysis", response_model=ImprovedCVResponse)
async def generate_candidate_cv_from_analysis(
    request: ImprovedCVRequest,
    _current_user=Depends(get_current_user),
):

    try:
        result = await generate_improved_cv_from_analysis(
            cv_text=request.cv_text,
            cv_analysis=request.cv_analysis,
            target_role=request.target_role,
            location=request.location,
            experience_level=request.experience_level,
        )
        return ImprovedCVResponse(improved_cv=result)
    except asyncio.TimeoutError as exc:
        raise HTTPException(
            status_code=504,
            detail="The AI response took too long. Please try again with shorter CV analysis.",
        ) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

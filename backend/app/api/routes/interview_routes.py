from typing import Any

from fastapi import APIRouter, Body, HTTPException
from pydantic import ValidationError

from ...services.interview_service import prepare_interview, run_mock_interview

try:
    from backend.schemas.interview_schema import (
        InterviewMessage,
        InterviewPreparationRequest,
        InterviewPreparationResponse,
        MockInterviewRequest,
        MockInterviewResponse,
    )
except ModuleNotFoundError:
    from schemas.interview_schema import (
        InterviewMessage,
        InterviewPreparationRequest,
        InterviewPreparationResponse,
        MockInterviewRequest,
        MockInterviewResponse,
    )

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
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/mock", response_model=MockInterviewResponse)
def mock_interview(payload: Any = Body(default_factory=dict)):
    try:
        if payload is None:
            payload = {}
        if not isinstance(payload, dict):
            raise HTTPException(
                status_code=400,
                detail="Request body must be a JSON object.",
            )

        messages = payload.get("messages", [])
        if isinstance(messages, str):
            messages = [{"role": "candidate", "content": messages}]
        elif isinstance(messages, dict):
            messages = [messages]

        request = MockInterviewRequest(
            cv_text=payload.get("cv_text") or payload.get("cv") or "",
            target_role=payload.get("target_role") or payload.get("role") or "",
            location=payload.get("location"),
            experience_level=payload.get("experience_level") or "Entry-level",
            interview_style=payload.get("interview_style") or "Formal",
            messages=[
                message
                if isinstance(message, InterviewMessage)
                else InterviewMessage(
                    role=message.get("role", "candidate"),
                    content=message.get("content", str(message)),
                )
                for message in messages
            ],
        )

        if not request.cv_text.strip() or not request.target_role.strip():
            raise HTTPException(
                status_code=400,
                detail="cv_text and target_role are required.",
            )

        result = run_mock_interview(
            cv_text=request.cv_text,
            target_role=request.target_role,
            messages=request.messages,
            location=request.location,
            experience_level=request.experience_level,
            interview_style=request.interview_style,
        )

        return MockInterviewResponse(reply=result)

    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=exc.errors()) from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

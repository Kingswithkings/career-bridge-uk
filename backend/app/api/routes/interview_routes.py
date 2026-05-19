import asyncio

from fastapi import APIRouter, Body, HTTPException
from fastapi import Depends
from pydantic import ValidationError

from ...api.dependencies import get_current_user
from ...posthog_client import posthog_client
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
async def prepare_candidate_interview(
    request: InterviewPreparationRequest,
    _current_user=Depends(get_current_user),
):

    try:
        result = await prepare_interview(
            cv_text=request.cv_text,
            target_role=request.target_role,
            job_description=request.job_description,
            location=request.location,
            experience_level=request.experience_level,
            interview_style=request.interview_style,
        )
        posthog_client.capture(
            distinct_id=_current_user.email,
            event="interview_prepared",
            properties={
                "target_role": request.target_role,
                "experience_level": request.experience_level,
                "interview_style": request.interview_style,
            },
        )
        return InterviewPreparationResponse(preparation=result)
    except asyncio.TimeoutError as exc:
        raise HTTPException(
            status_code=504,
            detail="The AI response took too long. Please try again with a shorter CV or job description.",
        ) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/mock", response_model=MockInterviewResponse)
async def mock_interview(
    payload: dict = Body(default_factory=dict),
    _current_user=Depends(get_current_user),
):

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

        result = await run_mock_interview(
            cv_text=request.cv_text,
            target_role=request.target_role,
            messages=request.messages,
            location=request.location,
            experience_level=request.experience_level,
            interview_style=request.interview_style,
        )

        posthog_client.capture(
            distinct_id=_current_user.email,
            event="mock_interview_completed",
            properties={
                "target_role": request.target_role,
                "experience_level": request.experience_level,
                "interview_style": request.interview_style,
                "message_count": len(request.messages),
            },
        )
        return MockInterviewResponse(reply=result)

    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=exc.errors()) from exc
    except HTTPException:
        raise
    except asyncio.TimeoutError as exc:
        raise HTTPException(
            status_code=504,
            detail="The AI response took too long. Please try again with a shorter conversation.",
        ) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

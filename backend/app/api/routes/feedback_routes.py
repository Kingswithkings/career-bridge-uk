from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...api.dependencies import get_current_user
from ...database import get_db
from ...posthog_client import posthog_client
from ...models.feedback_model import Feedback
from ...schemas.feedback_schema import FeedbackItem, FeedbackRequest, FeedbackResponse

router = APIRouter(prefix="/api/feedback", tags=["Feedback"])


@router.post("", response_model=FeedbackResponse)
def submit_feedback(
    request: FeedbackRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    feedback = Feedback(
        user_id=current_user.id,
        rating=request.rating,
        message=request.message,
        page=request.page,
        cv_analysis_helpful=request.cv_analysis_helpful,
        interview_preparation_useful=request.interview_preparation_useful,
        job_matching_accurate=request.job_matching_accurate,
        app_loaded_quickly=request.app_loaded_quickly,
        would_use_again=request.would_use_again,
    )

    db.add(feedback)
    db.commit()
    db.refresh(feedback)

    posthog_client.capture(
        distinct_id=current_user.email,
        event="feedback_submitted",
        properties={
            "rating": request.rating,
            "page": request.page,
            "cv_analysis_helpful": request.cv_analysis_helpful,
            "interview_preparation_useful": request.interview_preparation_useful,
            "job_matching_accurate": request.job_matching_accurate,
            "would_use_again": request.would_use_again,
        },
    )
    return FeedbackResponse(id=feedback.id, message="Feedback submitted successfully")


@router.get("", response_model=list[FeedbackItem])
def get_my_feedback(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return (
        db.query(Feedback)
        .filter(Feedback.user_id == current_user.id)
        .order_by(Feedback.created_at.desc())
        .all()
    )

from datetime import datetime

from pydantic import BaseModel, Field


class FeedbackRequest(BaseModel):
    rating: int = Field(ge=1, le=5)
    message: str | None = Field(default=None, max_length=4000)
    page: str | None = Field(default=None, max_length=120)
    cv_analysis_helpful: bool | None = None
    interview_preparation_useful: bool | None = None
    job_matching_accurate: bool | None = None
    app_loaded_quickly: bool | None = None
    would_use_again: bool | None = None


class FeedbackResponse(BaseModel):
    id: int
    message: str


class FeedbackItem(BaseModel):
    id: int
    user_id: int
    rating: int
    message: str | None
    page: str | None
    cv_analysis_helpful: bool | None
    interview_preparation_useful: bool | None
    job_matching_accurate: bool | None
    app_loaded_quickly: bool | None
    would_use_again: bool | None
    created_at: datetime

    class Config:
        from_attributes = True

from pydantic import BaseModel
from datetime import datetime


class SaveResultRequest(BaseModel):
    feature_type: str
    target_role: str | None = None
    location: str | None = None
    input_text: str | None = None
    result_text: str


class SaveResultResponse(BaseModel):
    id: int
    message: str


class SavedResultItem(BaseModel):
    id: int
    feature_type: str
    target_role: str | None
    location: str | None
    result_text: str
    created_at: datetime

    class Config:
        from_attributes = True

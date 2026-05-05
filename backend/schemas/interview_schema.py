from pydantic import BaseModel, Field


class InterviewPreparationRequest(BaseModel):
    cv_text: str
    target_role: str
    job_description: str | None = None
    location: str | None = None
    experience_level: str | None = "Entry-level"
    interview_style: str | None = "Formal"


class InterviewPreparationResponse(BaseModel):
    preparation: str


class InterviewMessage(BaseModel):
    role: str
    content: str


class MockInterviewRequest(BaseModel):
    cv_text: str
    target_role: str
    location: str | None = None
    experience_level: str | None = "Entry-level"
    interview_style: str | None = "Formal"
    messages: list[InterviewMessage] = Field(default_factory=list)


class MockInterviewResponse(BaseModel):
    reply: str

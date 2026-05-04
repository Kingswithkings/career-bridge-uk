from pydantic import BaseModel


class CVAnalysisRequest(BaseModel):
    cv_text: str
    target_role: str
    location: str | None = None
    experience_level: str | None = "Entry-level"
    visa_status: str | None = "Prefer not to say"


class CVAnalysisResponse(BaseModel):
    analysis: str
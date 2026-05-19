from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text

from ..database import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    message = Column(Text, nullable=True)
    page = Column(String, nullable=True)
    cv_analysis_helpful = Column(Boolean, nullable=True)
    interview_preparation_useful = Column(Boolean, nullable=True)
    job_matching_accurate = Column(Boolean, nullable=True)
    app_loaded_quickly = Column(Boolean, nullable=True)
    would_use_again = Column(Boolean, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from ..database import Base


class SavedResult(Base):
    __tablename__ = "saved_results"

    id = Column(Integer, primary_key=True, index=True)
    feature_type = Column(String, nullable=False)
    target_role = Column(String, nullable=True)
    location = Column(String, nullable=True)
    input_text = Column(Text, nullable=True)
    result_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

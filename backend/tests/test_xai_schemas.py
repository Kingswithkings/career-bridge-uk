import pytest
from pydantic import ValidationError

from backend.app.xai.schemas import XAIRequest


def test_valid_xai_request():
    request = XAIRequest.model_validate(
        {
            "candidate": {
                "skills": ["Python", "FastAPI", "SQL"],
                "experience_years": 3,
                "education": ["MSc Artificial Intelligence"],
                "career_goal": "AI Engineer",
            },
            "jobs": [
                {
                    "job_id": "job-001",
                    "title": "AI Engineer",
                    "company": "Example Company",
                    "required_skills": ["Python", "SQL"],
                }
            ],
        }
    )

    assert request.candidate.career_goal == "AI Engineer"
    assert len(request.jobs) == 1


def test_negative_experience_rejected():
    with pytest.raises(ValidationError):
        XAIRequest.model_validate(
            {
                "candidate": {
                    "experience_years": -2,
                    "career_goal": "AI Engineer",
                },
                "jobs": [
                    {
                        "job_id": "job-001",
                        "title": "AI Engineer",
                        "company": "Example Company",
                    }
                ],
            }
        )


def test_empty_jobs_rejected():
    with pytest.raises(ValidationError):
        XAIRequest.model_validate(
            {
                "candidate": {"career_goal": "AI Engineer"},
                "jobs": [],
            }
        )

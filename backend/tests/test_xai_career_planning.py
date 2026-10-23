from backend.app.xai.agents.career_planning import analyse_career_profile
from backend.app.xai.schemas import CareerProfile, JobEvidence


def make_candidate():
    return CareerProfile(
        skills=["Python", "FastAPI", "SQL"],
        experience_years=3,
        education=["MSc Artificial Intelligence"],
        career_goal="AI Engineer",
    )


def make_job(required_skills):
    return JobEvidence(
        job_id="job-001",
        title="AI Engineer",
        company="Example Company",
        required_skills=required_skills,
    )


def test_matching_skills():
    result = analyse_career_profile(
        make_candidate(),
        make_job(["Python", "SQL"]),
    )

    assert result["matched_skills"] == ["Python", "SQL"]
    assert result["missing_skills"] == []
    assert result["skill_match_percentage"] == 100.0


def test_missing_skills():
    result = analyse_career_profile(
        make_candidate(),
        make_job(["Python", "Docker", "Kubernetes"]),
    )

    assert result["matched_skills"] == ["Python"]
    assert result["missing_skills"] == ["Docker", "Kubernetes"]
    assert result["skill_match_percentage"] == 33.33


def test_empty_required_skills():
    result = analyse_career_profile(
        make_candidate(),
        make_job([]),
    )

    assert result["matched_skills"] == []
    assert result["missing_skills"] == []
    assert result["skill_match_percentage"] is None


def test_case_insensitive_matching():
    result = analyse_career_profile(
        make_candidate(),
        make_job(["python", "FASTAPI"]),
    )

    assert result["matched_skills"] == ["python", "FASTAPI"]
    assert result["skill_match_percentage"] == 100.0

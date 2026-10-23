from backend.app.xai.agents.evaluation_agent import evaluate_job_match
from backend.app.xai.schemas import CareerProfile, JobEvidence


def make_candidate():
    return CareerProfile(
        skills=["Python", "FastAPI", "LLMs", "RAG", "NLP"],
        experience_years=3,
        education=["MSc Applied AI"],
        career_goal="AI Engineer",
    )


def make_job(skills):
    return JobEvidence(
        job_id="DEMO-001",
        title="AI Engineer",
        company="Demo Technology Ltd",
        required_skills=skills,
        source_url=None,
    )


def evaluate(skills, source_type="sample"):
    return evaluate_job_match(
        make_candidate(),
        make_job(skills),
        evidence_origin="zetaris",
        source_type=source_type,
    )


def test_skill_match_percentage():
    result = evaluate(["Python", "FastAPI", "Machine Learning", "LLMs"])

    assert result["skill_match_percentage"] == 75.0
    assert result["matched_skills"] == ["Python", "FastAPI", "LLMs"]
    assert result["missing_skills"] == ["Machine Learning"]


def test_case_insensitive_matching():
    result = evaluate(["PYTHON", "fastapi"])

    assert result["skill_match_percentage"] == 100.0


def test_missing_skills():
    result = evaluate(["PostgreSQL", "Docker"])

    assert result["skill_match_percentage"] == 0.0
    assert result["missing_skills"] == ["PostgreSQL", "Docker"]


def test_empty_requirements():
    result = evaluate([])

    assert result["skill_match_percentage"] is None


def test_sample_jobs_not_verified():
    result = evaluate(["Python"])

    assert result["verified_live_vacancy"] is False
    assert result["source_type"] == "sample"
    assert result["evidence_warnings"]


def test_live_claim_not_automatically_verified():
    result = evaluate(["Python"], source_type="live")

    assert result["verified_live_vacancy"] is False
    assert result["evidence_warnings"]

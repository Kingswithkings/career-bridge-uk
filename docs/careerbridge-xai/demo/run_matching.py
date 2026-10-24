"""Offline matching and explanation demonstration."""

import json
from pathlib import Path

from backend.app.xai.schemas import CareerProfile, JobEvidence
from backend.app.xai.agents.evaluation_agent import evaluate_job_match
from backend.app.xai.agents.explanation_agent import explain_job_match
from backend.app.xai.agents.investigation_agent import investigate_career_evidence

root = Path(__file__).resolve().parents[3]
records = json.loads(
    (root / "docs/careerbridge-xai/sample_jobs.json").read_text()
)

candidate = CareerProfile(
    skills=["Python", "FastAPI", "LLMs", "RAG"],
    experience_years=3,
    education=["MSc Applied AI"],
    career_goal="AI Engineer",
)

print("CAREERBRIDGE XAI — MATCHING DEMONSTRATION")
results = []

for record in records:
    job = JobEvidence(
        job_id=record["job_id"],
        title=record["job_title"],
        company=record["company"],
        required_skills=record["required_skills"],
        source_url=record["source_url"],
    )

    evaluation = evaluate_job_match(
        candidate,
        job,
        evidence_origin=record["evidence_origin"],
        source_type=record["source_type"],
    )
    explanation = explain_job_match(evaluation)
    results.append({"job_id": job.job_id, "evaluation": evaluation})

    print()
    print("Job:", job.title)
    print("Skill coverage:", evaluation["skill_match_percentage"], "%")
    print("Matched:", ", ".join(evaluation["matched_skills"]) or "None")
    print("Missing:", ", ".join(evaluation["missing_skills"]) or "None")
    print("Explanation:", explanation["summary"])

print()
finding = investigate_career_evidence(candidate, results, records)
print("SOURCE-QUALITY CRITIQUE:", finding["source_critique"]["limitations"])
print("EVIDENCE-GROUNDED GAP HYPOTHESES:")
for gap in finding["priority_skill_gaps"]:
    print(" -", gap["skill"], "cited jobs:", gap["jobs_mentioning_gap"])
print("IMPORTANT:", finding["conclusion"])
assert not finding["source_critique"]["sufficient_for_cross_source_inference"]
print()
print("MATCHING DEMONSTRATION: PASSED")

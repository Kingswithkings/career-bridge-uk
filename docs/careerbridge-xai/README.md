# CareerBridge XAI
## Explainable Career Intelligence Agent

CareerBridge XAI extends CareerBridge UK with an evidence-grounded
career investigation workflow. It retrieves job listings, constructs
an evidence graph, evaluates skill mentions, critiques source quality,
and produces transparent recommendations.

Developed for Open Agent Hackathon 2026, Track 2:
Agent That Can Explain Why.

## Architecture

Next.js dashboard
    |
    v
FastAPI /api/xai/run
    |
    v
Live Adzuna Job Evidence Agent
    |
    v
Meterless World Model
(job-to-skill relationships and source provenance)
    |
    v
Career Planning and Evaluation Agents
    |
    v
Investigation and Source Critique Agent
    |
    +--> Evidence references and alternative explanations
    |
    +--> Optional NVIDIA Nemotron advisory explanation
    |
    v
Dashboard response, execution trace and JSONL audit

## Technology

- Next.js and React frontend
- Python 3.11 and FastAPI backend
- Adzuna job search API
- Meterless World Model (TypeScript)
- NVIDIA Nemotron through NVIDIA hosted inference API
- SQLite or PostgreSQL application database
- Pydantic and pytest

## Live Evidence Policy

The public XAI investigation endpoint requires live job evidence.

- The API retrieves Adzuna job-search records.
- Listings must provide usable source URLs and skill mentions.
- No synthetic records are substituted if live retrieval fails.
- Missing usable live evidence produces HTTP 503.
- Job-description keyword mentions are not verified requirements.
- A skill missing from the submitted candidate profile does not
  establish that the candidate lacks the skill.
- Cross-provider corroboration is not claimed when only Adzuna
  evidence is represented.

The Zetaris adapter and synthetic demonstration remain separate
development and testing capabilities; they are not the source of
records in the demonstrated live-only API workflow.

## API

POST /api/xai/run

Key request fields:

- candidate.career_goal
- candidate.skills
- candidate.education
- candidate.experience_years
- limit
- include_live_jobs: true
- location (optional)
- question (optional)
- include_nvidia_insight: false by default

The response includes:

- Investigation ID
- Evaluated job records
- Meterless evidence graph
- Skill-gap hypotheses and source references
- Alternative explanations and verification actions
- Source-quality critique
- Agent execution trace
- Optional NVIDIA advisory narrative

GET /api/xai/capabilities returns whether optional NVIDIA
inference is configured and enabled, without returning credentials.

## NVIDIA Nemotron

The verified hosted model is:

nvidia/nemotron-3.5-lightning-30b-a3b

NVIDIA explanations are optional, not independent verification.
Model output does not change the underlying evidence records.

NVIDIA API requests require a valid application login and
XAI_ENABLE_NVIDIA_API=true. The inference adapter additionally
requires XAI_ENABLE_NVIDIA=true and NVIDIA_API_KEY.

Do not enable hosted paid inference publicly without suitable
usage quotas, abuse protection and monitoring.

Never commit API keys, tokens or .env files.

## Local Development

Run the FastAPI backend from the repository root with its Python
dependencies installed and application database configured:

    python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8001

Run the frontend separately:

    cd frontend/careerbridge-frontend
    npm ci
    npm run dev -- --webpack --port 3000

For local development, configure the frontend API base URL as:

    NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8001

Set Adzuna credentials in the backend's private configuration:

- ADZUNA_APP_ID
- ADZUNA_APP_KEY

The browser demonstration is at /dashboard/xai.

## Offline Reproducible Demonstration

The repository also contains synthetic sample job records at:

docs/careerbridge-xai/sample_jobs.json

These records are examples, not live or verified vacancies.

From the repository root:

    cd backend/app/xai/integrations/meterless
    npm ci
    cd ../../../../..
    ./docs/careerbridge-xai/demo/run_all.sh

The offline demonstration exercises Meterless graph ingestion and
explainable matching without depending on live Adzuna retrieval.

The Meterless bridge distinguishes source origins including
Adzuna, Zetaris and synthetic demo records.

## Testing

From the repository root, with the Python environment active:

    python -m pytest backend/tests/test_xai_*.py -q
    git diff --check

Latest reported validation: 50 Python tests passed.

A separate local Meterless provenance check also passed with:
- 2 input records
- 3 job-to-skill relationships
- Correct Adzuna and demo source labels

## Demonstrated Results

A successful local browser investigation evaluated:

- 8 live Adzuna job records
- 12 evidence relationships
- 0 synthetic records
- 3 preliminary skill-gap hypotheses
- Successful optional NVIDIA Nemotron inference

These figures describe one observed run, not a fixed system output.
Live search results can change.

Independent cross-provider corroboration was not established.

## Audit and Evidence Limitations

The system records execution metadata, evaluations and evidence
provenance in a JSONL audit log.

Match scores reflect the implemented skill-coverage logic. They
are not hiring probabilities, confirmed employer decisions or
guarantees of candidate suitability.

Adzuna listing excerpts are unverified third-party source content.
NVIDIA output is an advisory interpretation of supplied evidence.

A fresh public deployment of the full XAI workflow has not yet
been validated as part of this local demonstration.

## Prior Work and Licensing

CareerBridge UK predates this hackathon.

The Meterless World Model reference source is vendored under its
declared Apache-2.0 license. See:

backend/app/xai/integrations/meterless/vendor/LICENSE
backend/app/xai/integrations/meterless/vendor/UPSTREAM.md

CareerBridge XAI adds evidence-source integrations, investigation
orchestration, explainability, provenance and the dashboard.

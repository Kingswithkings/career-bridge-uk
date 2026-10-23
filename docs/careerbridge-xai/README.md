# CareerBridge XAI

## Explainable Career Intelligence Agent

CareerBridge XAI extends CareerBridge UK with an
explainable, multi-agent career intelligence workflow.

It evaluates required-skill coverage, identifies skill
gaps, explains matching results, and records evidence
provenance for auditing.

## Architecture

FastAPI
  -> Zetaris Evidence Agent
  -> Meterless World Model
  -> Career Planning Agent
  -> Evaluation Agent
  -> Explanation Agent
  -> API Response and JSONL Audit

## Technology

- Python 3.11 and FastAPI
- PostgreSQL and Zetaris JDBC
- Meterless World Model (TypeScript)
- Node.js and tsx
- Pydantic and pytest

## API

Endpoint: POST /api/xai/run

Request fields:
- candidate.skills
- candidate.experience_years
- candidate.education
- candidate.career_goal
- limit (default: 3)

The response contains:
- A unique run ID
- Career analysis
- Job matching evaluations
- Human-readable explanations
- Meterless evidence graph

Match percentages represent required-skill coverage,
not hiring probabilities.

## Reproducible demonstration

Three synthetic job records are included in
docs/careerbridge-xai/sample_jobs.json.

From the repository root, install dependencies:

cd backend/app/xai/integrations/meterless
npm ci

Return to the repository root:

cd ../../../../..

Run the Meterless demonstration:

backend/app/xai/integrations/meterless/node_modules/.bin/tsx backend/app/xai/integrations/meterless/bridge.ts docs/careerbridge-xai/sample_jobs.json

Expected:
- 3 jobs processed
- 12 job-to-skill relationships
- 3 unchanged records skipped on second ingestion

## Zetaris configuration

The full API requires a running Zetaris JDBC service
connected to the CAREERBRIDGE_XAI.job_evidence table.

Required environment variables:

- ZETARIS_JDBC_URL
- ZETARIS_USERNAME
- ZETARIS_PASSWORD
- ZETARIS_JDBC_DRIVER_PATH

Never commit credentials or local .env files.

The existing CareerBridge application also requires
its database configuration.

## Automated testing

Activate the Python environment and run:

python -m pytest backend/tests/test_xai_*.py -q

Latest verified result: 25 tests passed.

## Evidence and limitations

The DEMO-* job records are synthetic examples,
not verified live employment opportunities.

Matching scores measure required-skill coverage.
They do not predict hiring decisions or overall
candidate suitability.

Meterless records job-to-skill relationships and
source provenance. JSONL audit entries capture
run IDs, evaluations and evidence metadata.

The offline Meterless demonstration is reproducible
from the included sample data.

The complete API was verified locally using Zetaris,
but a fresh-environment Zetaris installation and
hosted deployment have not yet been validated.

## Licensing and prior work

CareerBridge UK existed before this hackathon.

The Meterless World Model reference source is
vendored under its declared Apache-2.0 licence.

See:
backend/app/xai/integrations/meterless/vendor/LICENSE
backend/app/xai/integrations/meterless/vendor/UPSTREAM.md

CareerBridge XAI adds the integration adapters,
career agents, orchestration and explanations.

## Combined offline hackathon demonstration

Install Meterless dependencies as documented above.

From the repository root, with Python dependencies installed:

    ./docs/careerbridge-xai/demo/run_all.sh

The demonstration shows:
- Meterless job-to-skill evidence graph and provenance
- Idempotent ingestion of three synthetic job records
- Required-skill coverage calculations
- Matched and missing skills
- Human-readable explanations

The offline demonstration does not require Zetaris.
The full FastAPI endpoint uses Zetaris separately.
All sample job records are synthetic.

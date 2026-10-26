# CareerBridge XAI — Track 2 investigation increment

This change extends the existing CareerBridge XAI (which predates the hackathon).
It is an **implementation increment**, not a claim that every sponsor integration
has been live-verified on a clean machine.

## New behavior

`POST /api/xai/run` now accepts the optional fields:

- `question`: career investigation question (up to 500 characters).
- `include_live_jobs`: opt-in to a bounded Adzuna enrichment attempt (default `false`).
- `location`: UK place passed to the existing Adzuna search service.

The workflow:

1. Reads the existing Zetaris job evidence records.
2. Evaluates evidence sufficiency, origin diversity and sample-only limitations.
3. If explicitly requested, retrieves UK Adzuna job listings once via the
   **existing** `job_search_service.search_live_jobs` and retains their URLs.
4. Uses a conservative, explicitly disclosed dictionary to identify skills
   *mentioned* in listing summaries. These are **not verified requirements**.
5. Builds the existing Meterless World Model evidence graph.
6. Evaluates per-job candidate skill coverage and cross-vacancy recurring gaps.
7. Runs a second evidence critique. It abstains from employer rejection claims
   and attaches individual source references to each gap hypothesis.
8. Optionally sends a **supplemental**, clearly marked narrative request to
   Meterless Nightshift. It never substitutes model output for cited findings.
9. Emits a branch/decision trace and appends a sanitized audit record.

The second provider is queried directly and is **not yet persisted into
Zetaris**. Full source unification through Zetaris and independent vacancy
verification remain production follow-ups.

## Example request

Ensure your existing Zetaris setup and backend are running. For live
enrichment, also configure `ADZUNA_APP_ID` and `ADZUNA_APP_KEY` as used by
the existing CareerBridge app. Do not commit keys or tokens.

```bash
curl --fail-with-body -sS -X POST http://127.0.0.1:8000/api/xai/run \
  -H 'Content-Type: application/json' \
  -d '{
    "candidate": {
      "skills": ["Python", "FastAPI", "LLMs", "RAG"],
      "experience_years": 3,
      "education": ["MSc Applied AI"],
      "career_goal": "AI Engineer"
    },
    "question": "Which evidenced gaps might reduce my fit for UK AI Engineer roles?",
    "location": "Doncaster",
    "limit": 3,
    "include_live_jobs": true
  }'
```

Response additions: `investigation`, `agent_trace`, `nightshift`.

- `investigation.priority_skill_gaps[*].evidence_references` references each
  record with `job_id`, provider, source type, method and any job URL.
- `investigation.source_critique` explicitly indicates whether comparisons
  across distinct providers are possible.
- `nightshift.used` is `false` unless an actual model response was received.
- Scores are skill *coverage*, **never hiring probabilities**.
- Sample records, stale postings, CV omissions and inferred employer decisions
  must not be mislabeled as verified observations.

## Optional Nightshift inference

The existing API continues to work deterministically while Nightshift access
is unresolved. To opt into real Nightshift inference:

```bash
export XAI_ENABLE_NIGHTSHIFT=true
export METERLESS_BASE_URL=http://127.0.0.1:8088/v1
export METERLESS_MODEL=meterless/auto
# Export the genuine token privately; NEVER add it to a public README.
```

`METERLESS_RUNTIME_TOKEN` must be supplied privately in the process
environment. The client sends `Authorization: Bearer`, `meterless-app:
careerbridge-xai`, and `meterless-scope: user` on an OpenAI-compatible chat
request. On authentication failure it returns
`{"status":"authentication_failed","used":false}` and preserves
deterministic findings; it never invents a response.

The model is asked to summarize only the supplied structured evidence.
The returned text is labeled *advisory* and *not independently verified*.
Review Nightshift's real model receipt before claiming NVIDIA Nemotron usage.
`meterless/auto` does not itself prove a Nemotron model handled the request.

## Tests

```bash
python -m pytest backend/tests/test_xai_*.py -q
python -m black --check backend/app/xai backend/app/api/routes/xai_routes.py backend/tests/test_xai_*.py
```

Existing demo: `./docs/careerbridge-xai/demo/run_all.sh`. It remains an
offline synthetic-data demonstration and does not prove live-provider access.

## Remaining acceptance gates

- [ ] Real Adzuna enrichment works with credentials and references accessible URLs.
- [ ] Authentic Zetaris queries and the Meterless World Model both execute on the demonstration machine.
- [ ] Nightshift runtime token authenticates (currently HTTP 401 on the user's Mac).
- [ ] Live Nightshift chat call and underlying NVIDIA model receipt verified.
- [ ] Independent job availability verification and skill requirement review.
- [ ] CI passes and the existing application does not regress.
- [ ] Production auth, privacy, tracing retention, rate limiting and user consent reviewed.

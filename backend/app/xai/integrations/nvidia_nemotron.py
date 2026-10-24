"""Hosted NVIDIA Nemotron explanations grounded in CareerBridge XAI evidence."""

import json
import os
from pathlib import Path

from dotenv import load_dotenv


def request_nvidia_insight(investigation: dict) -> dict:
    """Generate an optional advisory narrative without modifying evidence."""
    load_dotenv(Path(__file__).resolve().parents[3] / ".env")

    if os.getenv("XAI_ENABLE_NVIDIA", "").lower() not in {"true", "1", "yes"}:
        return {"status": "disabled", "used": False}

    key = os.getenv("NVIDIA_API_KEY")
    if not key:
        return {"status": "not_configured", "used": False}

    from openai import OpenAI

    model = os.getenv(
        "NVIDIA_MODEL",
        "nvidia/nemotron-3.5-lightning-30b-a3b",
    )

    findings = []
    for gap in investigation.get("priority_skill_gaps", [])[:3]:
        refs = gap.get("evidence_references", [])[:3]
        findings.append({
            "skill": gap.get("skill"),
            "why_it_matters": gap.get("why_it_matters"),
            "live_references": gap.get("live_listings_mentioning_gap", 0),
            "synthetic_references": gap.get("synthetic_examples_mentioning_gap", 0),
            "references": [
                {
                    "job_id": ref.get("job_id"),
                    "source_type": ref.get("source_type"),
                    "excerpt": (ref.get("source_excerpt") or "")[:200],
                }
                for ref in refs
            ],
        })

    evidence = {
        "question": investigation.get("question"),
        "candidate_goal": investigation.get("candidate_goal"),
        "conclusion": investigation.get("conclusion"),
        "source_critique": investigation.get("source_critique"),
        "findings": findings,
        "boundaries": investigation.get("boundaries", []),
    }

    try:
        client = OpenAI(
            api_key=key,
            base_url="https://integrate.api.nvidia.com/v1",
            timeout=60.0,
            max_retries=0,
        )

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are CareerBridge XAI's evidence-grounded "
                        "career investigation narrator. Explain the supplied "
                        "findings clearly and briefly. Cite job IDs when "
                        "referring to listing evidence. Distinguish synthetic "
                        "records from unverified live listings. Do not invent "
                        "jobs, requirements, statistics, candidate abilities, "
                        "or employer rejection reasons. State uncertainty."
                    ),
                },
                {
                    "role": "user",
                    "content": json.dumps(evidence),
                },
            ],
            temperature=1,
            max_tokens=512,
            extra_body={
                "chat_template_kwargs": {
                    "enable_thinking": False,
                },
            },
        )

        answer = response.choices[0].message.content or ""

        if not answer.strip():
            return {"status": "empty_response", "used": False}

        return {
            "status": "success",
            "used": True,
            "model_requested": model,
            "model_reported": response.model,
            "advisory_narrative": answer.strip(),
            "independently_verified": False,
        }

    except Exception as error:
        status_code = getattr(error, "status_code", None)

        return {
            "status": "inference_failed",
            "used": False,
            "error_type": type(error).__name__,
            "http_status": status_code,
        }

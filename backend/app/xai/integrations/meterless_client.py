"""Python adapter for the Meterless World Model."""

import json
import os
import subprocess
import tempfile
from pathlib import Path


BRIDGE_PATH = Path(__file__).resolve().parent / "meterless" / "bridge.ts"


def build_meterless_graph(records: list[dict]) -> dict:
    """Build a Meterless evidence graph from Zetaris job records."""
    if not records:
        raise ValueError("Meterless requires at least one evidence record")

    local_runner = BRIDGE_PATH.parent / "node_modules" / ".bin" / "tsx"
    runner = os.getenv("METERLESS_TSX_PATH") or str(local_runner)

    with tempfile.TemporaryDirectory(prefix="careerbridge-meterless-") as directory:
        input_path = Path(directory) / "jobs.json"
        input_path.write_text(
            json.dumps(records, default=str),
            encoding="utf-8",
        )

        try:
            completed = subprocess.run(
                [runner, str(BRIDGE_PATH), str(input_path)],
                capture_output=True,
                text=True,
                timeout=30,
                check=True,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            raise RuntimeError(
                "Meterless World Model execution failed"
            ) from exc

    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Meterless returned invalid JSON") from exc

    if (
        not isinstance(result, dict)
        or result.get("engine") != "Meterless World Model"
        or result.get("jobs_received") != len(records)
        or not isinstance(result.get("evidence_graph"), dict)
        or not isinstance(result["evidence_graph"].get("jobs"), list)
        or not isinstance(result["evidence_graph"].get("relationship_count"), int)
        or len(result["evidence_graph"]["jobs"]) != len(records)
    ):
        raise RuntimeError("Meterless returned an unexpected response")

    return result

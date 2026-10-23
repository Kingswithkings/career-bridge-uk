#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
BRIDGE="$ROOT/backend/app/xai/integrations/meterless"
SAMPLE="$ROOT/docs/careerbridge-xai/sample_jobs.json"

if [ ! -x "$BRIDGE/node_modules/.bin/tsx" ]; then
    echo "Meterless dependencies missing."
    echo "Run: cd $BRIDGE && npm ci"
    exit 1
fi

OUTPUT="$(mktemp)"
trap 'rm -f "$OUTPUT"' EXIT

"$BRIDGE/node_modules/.bin/tsx" \
    "$BRIDGE/bridge.ts" "$SAMPLE" > "$OUTPUT"

node - "$OUTPUT" <<'JS'
const fs = require("node:fs");
const result = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));

const jobs = result.evidence_graph.jobs;
const relationships = result.evidence_graph.relationship_count;

if (jobs.length !== 3 || relationships !== 12) {
    throw new Error("Unexpected Meterless evidence graph");
}

console.log("CAREERBRIDGE XAI — METERLESS DEMONSTRATION");
console.log("Engine:", result.engine);
console.log("Jobs:", jobs.length);
console.log("Skill relationships:", relationships);

for (const job of jobs) {
    console.log("-", job.title);
    console.log("  Skills:", job.skills.join(", "));
    console.log("  Provenance:", job.provenance.at);
}

console.log(
    "Unchanged records skipped:",
    result.second_ingest.skipped_unchanged
);
console.log("DEMONSTRATION: PASSED");
JS

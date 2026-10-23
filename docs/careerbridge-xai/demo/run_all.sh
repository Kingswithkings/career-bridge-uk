#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "$ROOT"

echo "========================================"
echo "CAREERBRIDGE XAI — HACKATHON DEMONSTRATION"
echo "========================================"

echo
echo "PART 1 — METERLESS EVIDENCE GRAPH"
bash docs/careerbridge-xai/demo/run_demo.sh

echo
echo "PART 2 — EXPLAINABLE JOB MATCHING"
PYTHONPATH=. python docs/careerbridge-xai/demo/run_matching.py

echo
echo "========================================"
echo "CAREERBRIDGE XAI DEMONSTRATION: PASSED"
echo "========================================"

# GitHub Copilot Instructions

This repository is an academic capstone project for fixed-CCTV traffic incident detection and flood road warning.

## Core Rules:
1. Always reference AGENTS.md for architectural rules and module ownership.
2. Event format between components must strictly use PipelineEvent in src/pipeline/event_schema.py.
3. Never hardcode thresholds or magic numbers; read them from configs/*.yaml.
4. Stage 1 is heuristic/rule-based (no ML training required). Stage 2 is an image classifier. Keep them decoupled.
5. Shared metrics live in evaluation/metrics.py.

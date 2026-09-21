# Claude Code Project Guidelines

Please read AGENTS.md before making changes. It defines the core project architecture, scope boundaries, and role assignments.

## Quick Commands
- Run tests: pytest
- Run smoke test: pytest tests/test_smoke.py
- Run pipeline: python src/pipeline/end_to_end.py --config configs/pipeline.yaml --source <video>
- Check evaluation: python -m evaluation.metrics --help

## Key Boundaries & Rules
- Do NOT hardcode thresholds (put them into configs/*.yaml).
- All events passed between stages MUST strictly use PipelineEvent from src/pipeline/event_schema.py.
- Keep Stage 1 (rule-based) and Stage 2 (classifier) cleanly decoupled.
- Follow module ownership defined in AGENTS.md.

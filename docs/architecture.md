# Kiến trúc hệ thống chi tiết

## Data flow

```
                      ┌──────────────────────────────────┐
   Video CCTV/file ──►│  detection_tracking/detector.py  │  YOLOv26m
                      │  (+ tracker — TBD)               │
                      └──────────────┬───────────────────┘
                                     │ List[Detection] per frame
                      ┌──────────────▼───────────────────┐
                      │  stage1_rule_engine/              │  Rule-based (no training)
                      │  flags: sudden_stop, lane_deviate │
                      └──────────────┬───────────────────┘
                                     │ CandidateEvent (track_id, frames)
                      ┌──────────────▼───────────────────┐
                      │  stage2_classifier/               │  Image classifier
                      │  → incident_score: float          │
                      └──────────────┬───────────────────┘
                                     │
                      ┌──────────────▼───────────────────┐
   Flood model ──────►│  event_engine/                    │  threshold/smooth/dedup
                      │  → PipelineEvent                  │
                      └──────────────┬───────────────────┘
                                     │
                      ┌──────────────▼───────────────────┐
                      │  database/db_client.py            │  SQLite
                      └──────────────┬───────────────────┘
                                     │
                      ┌──────────────▼───────────────────┐
                      │  FastAPI backend                  │
                      │  → WebSocket / REST               │
                      │  → React Dashboard (Khang)        │
                      └──────────────────────────────────┘
```

## Event JSON Schema

Defined in `src/pipeline/event_schema.py` — `PipelineEvent` dataclass.
All stages must use this schema. Do NOT create alternative schemas.

## Stage 1 ↔ Stage 2 boundary

- Stage 1 outputs: `track_id`, `flagged_frames`, `flag_reason`
- Stage 2 receives: cropped image frames (pre-extracted from video)
- Stage 2 trains independently on static clips — does NOT depend on live tracking

## Config override hierarchy

1. `configs/<module>.yaml` — default values
2. CLI args `--config` override at pipeline level
3. Never hardcode thresholds in `.py` files

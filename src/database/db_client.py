"""
SQLite database client.
Responsible: Lãnh
"""
import sqlite3
from pathlib import Path
from typing import List, Optional
from loguru import logger

from src.pipeline.event_schema import PipelineEvent


class DBClient:
    """Simple synchronous SQLite client."""

    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        schema = (Path(__file__).parent / "schema.sql").read_text()
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(schema)
        logger.info(f"DB initialised at {self.db_path}")

    def insert_event(self, event: PipelineEvent) -> int:
        """Insert a PipelineEvent and return its row id."""
        d = event.to_dict()
        bbox = d.pop("bbox") or {}
        sql = """
            INSERT INTO events (
                event_type, source_id, timestamp_start, timestamp_end,
                frame_start, frame_end, track_id,
                stage1_flagged, stage2_score, flood_level, incident_score,
                bbox_x1, bbox_y1, bbox_x2, bbox_y2,
                evidence_clip_path, thumbnail_path, location_tag
            ) VALUES (
                :event_type, :source_id, :timestamp_start, :timestamp_end,
                :frame_start, :frame_end, :track_id,
                :stage1_flagged, :stage2_score, :flood_level, :incident_score,
                :bbox_x1, :bbox_y1, :bbox_x2, :bbox_y2,
                :evidence_clip_path, :thumbnail_path, :location_tag
            )
        """
        params = {**d, **{f"bbox_{k}": v for k, v in bbox.items()}}
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.execute(sql, params)
            return cur.lastrowid

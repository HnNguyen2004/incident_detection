"""
Canonical JSON schema for events passed between pipeline stages.
All stages MUST produce/consume this format.
"""
from dataclasses import dataclass, field
from typing import Literal, Optional
import time


EventType = Literal["traffic_incident", "flood"]
FloodLevel = Literal["Normal", "PossibleFlood", "SevereFlood"]


@dataclass
class BoundingBox:
    x1: float
    y1: float
    x2: float
    y2: float


@dataclass
class PipelineEvent:
    """Single event emitted by the event engine to the database."""

    # Identity
    event_type: EventType

    # Timing
    timestamp_start: float = field(default_factory=time.time)
    timestamp_end: Optional[float] = None
    frame_start: int = 0
    frame_end: Optional[int] = None

    # Source
    source_id: str = ""           # camera id / video filename
    track_id: Optional[int] = None  # vehicle track id (traffic only)

    # Scores
    stage1_flagged: bool = False
    stage2_score: Optional[float] = None   # None for flood events
    flood_level: Optional[FloodLevel] = None  # None for traffic events
    incident_score: float = 0.0            # final unified score

    # Evidence
    bbox: Optional[BoundingBox] = None
    evidence_clip_path: Optional[str] = None
    thumbnail_path: Optional[str] = None

    # Metadata
    location_tag: Optional[str] = None    # e.g. "Camera 01 — Ngã tư Bình Thạnh"

    def to_dict(self) -> dict:
        import dataclasses
        return dataclasses.asdict(self)

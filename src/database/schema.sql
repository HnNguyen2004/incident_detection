-- Incident Detection Database Schema
-- Engine: SQLite

CREATE TABLE IF NOT EXISTS events (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type          TEXT NOT NULL,          -- 'traffic_incident' | 'flood'
    source_id           TEXT NOT NULL,          -- camera id / video filename
    timestamp_start     REAL NOT NULL,          -- Unix timestamp
    timestamp_end       REAL,
    frame_start         INTEGER,
    frame_end           INTEGER,
    track_id            INTEGER,                -- vehicle track (traffic only)
    stage1_flagged      INTEGER DEFAULT 0,      -- boolean
    stage2_score        REAL,
    flood_level         TEXT,                   -- 'Normal'|'PossibleFlood'|'SevereFlood'
    incident_score      REAL NOT NULL,
    bbox_x1             REAL,
    bbox_y1             REAL,
    bbox_x2             REAL,
    bbox_y2             REAL,
    evidence_clip_path  TEXT,
    thumbnail_path      TEXT,
    location_tag        TEXT,
    created_at          TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_events_type       ON events(event_type);
CREATE INDEX IF NOT EXISTS idx_events_source     ON events(source_id);
CREATE INDEX IF NOT EXISTS idx_events_timestamp  ON events(timestamp_start);

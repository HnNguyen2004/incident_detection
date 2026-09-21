"""
Smoke tests — verify module imports and basic instantiation.
Run: pytest tests/test_smoke.py
"""
import pytest


def test_event_schema_import():
    from src.pipeline.event_schema import PipelineEvent, BoundingBox
    e = PipelineEvent(event_type="traffic_incident", source_id="cam01", incident_score=0.9)
    assert e.event_type == "traffic_incident"
    d = e.to_dict()
    assert "incident_score" in d


def test_config_utils():
    from src.utils.config import load_config
    cfg = load_config("configs/pipeline.yaml")
    assert "source" in cfg
    assert "event_engine" in cfg


def test_metrics_functions():
    from evaluation.metrics import compute_frame_metrics, compute_event_recall
    metrics = compute_frame_metrics([1, 0, 1, 0], [1, 0, 0, 0])
    assert "precision" in metrics
    recall = compute_event_recall([(0, 10)], [(2, 8)])
    assert recall == 1.0

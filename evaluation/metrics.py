"""
Shared evaluation harness.
Use this for BOTH traffic incident model and flood model.
Do NOT write separate evaluation scripts.

Metrics computed:
- Precision, Recall, F1, PR-AUC (frame-level)
- Event-level recall
- False alarms per hour
- Detection delay (seconds)
"""
from __future__ import annotations
import argparse
from pathlib import Path
from typing import List, Tuple
import numpy as np


def compute_frame_metrics(
    y_true: List[int],
    y_pred: List[int],
    y_score: Optional[List[float]] = None,
) -> dict:
    """Precision / Recall / F1 at frame level."""
    from sklearn.metrics import precision_recall_fscore_support, average_precision_score
    prec, rec, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average="binary", zero_division=0
    )
    result = {"precision": prec, "recall": rec, "f1": f1}
    if y_score is not None:
        result["pr_auc"] = average_precision_score(y_true, y_score)
    return result


def compute_event_recall(
    gt_events: List[Tuple[float, float]],   # list of (start_sec, end_sec)
    pred_events: List[Tuple[float, float]],
    iou_threshold: float = 0.1,
) -> float:
    """
    Event-level recall: fraction of GT events that overlap with at least one prediction.
    """
    if not gt_events:
        return 1.0
    hits = 0
    for gt_s, gt_e in gt_events:
        gt_dur = gt_e - gt_s
        for pd_s, pd_e in pred_events:
            inter = max(0, min(gt_e, pd_e) - max(gt_s, pd_s))
            union = max(gt_e, pd_e) - min(gt_s, pd_s)
            if union > 0 and (inter / union) >= iou_threshold:
                hits += 1
                break
    return hits / len(gt_events)


def compute_false_alarms_per_hour(
    pred_events: List[Tuple[float, float]],
    gt_events: List[Tuple[float, float]],
    video_duration_sec: float,
    iou_threshold: float = 0.1,
) -> float:
    """False alarm rate = FP events / video hours."""
    fp = 0
    for pd_s, pd_e in pred_events:
        matched = False
        for gt_s, gt_e in gt_events:
            inter = max(0, min(pd_e, gt_e) - max(pd_s, gt_s))
            union = max(pd_e, gt_e) - min(pd_s, gt_s)
            if union > 0 and (inter / union) >= iou_threshold:
                matched = True
                break
        if not matched:
            fp += 1
    hours = video_duration_sec / 3600.0
    return fp / hours if hours > 0 else float("inf")


def main():
    parser = argparse.ArgumentParser(description="Shared Evaluation Harness")
    parser.add_argument("--predictions", type=str, required=True,
                        help="Path to predictions CSV")
    parser.add_argument("--ground-truth", type=str, required=True,
                        help="Path to ground truth CSV")
    parser.add_argument("--video-duration", type=float, default=None,
                        help="Video duration in seconds (for false-alarms/hour)")
    args = parser.parse_args()

    # TODO: load CSVs and call compute_* functions
    print("Evaluation harness — TODO: implement CSV loading")


if __name__ == "__main__":
    main()

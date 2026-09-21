"""
YOLO detector wrapper.
Owns model loading and per-frame inference.
Tracking integration is a separate concern (tracker.py).
"""
from __future__ import annotations
from pathlib import Path
from typing import List, NamedTuple, Optional
import numpy as np


class Detection(NamedTuple):
    """Single object detection result."""
    class_id: int
    confidence: float
    x1: float
    y1: float
    x2: float
    y2: float


class YOLODetector:
    """
    Thin wrapper around Ultralytics YOLO (yolo26m).

    Usage::
        detector = YOLODetector.from_config(cfg)
        detections = detector.detect(frame)
    """

    def __init__(self, model_name: str, weights: Optional[str], device: str,
                 conf: float, iou: float, classes: List[int]):
        from ultralytics import YOLO
        weight_path = weights or model_name
        self.model = YOLO(weight_path)
        self.device = device
        self.conf = conf
        self.iou = iou
        self.classes = classes

    @classmethod
    def from_config(cls, cfg) -> "YOLODetector":
        """Instantiate from OmegaConf detection config node."""
        return cls(
            model_name=cfg.model.name,
            weights=cfg.model.weights,
            device=cfg.model.device,
            conf=cfg.model.conf_threshold,
            iou=cfg.model.iou_threshold,
            classes=list(cfg.model.classes),
        )

    def detect(self, frame: np.ndarray) -> List[Detection]:
        """Run inference on a single BGR frame."""
        results = self.model.predict(
            frame,
            device=self.device,
            conf=self.conf,
            iou=self.iou,
            classes=self.classes,
            verbose=False,
        )
        detections = []
        for r in results:
            for box in r.boxes:
                detections.append(Detection(
                    class_id=int(box.cls[0]),
                    confidence=float(box.conf[0]),
                    x1=float(box.xyxy[0][0]),
                    y1=float(box.xyxy[0][1]),
                    x2=float(box.xyxy[0][2]),
                    y2=float(box.xyxy[0][3]),
                ))
        return detections

"""Video inference with trained YOLOv8 model."""

from pathlib import Path
from typing import List, Dict, Optional
import cv2
import numpy as np


class VideoInference:
    """Run YOLOv8 inference on surgical videos for anomalous bleeding detection."""

    def __init__(self, model_path: str, confidence_threshold: float = 0.5):
        self.model_path = Path(model_path)
        self.confidence_threshold = confidence_threshold
        self._model = None

    def _load_model(self):
        """Lazy-load the YOLO model."""
        if self._model is None:
            try:
                from ultralytics import YOLO
                self._model = YOLO(str(self.model_path))
            except ImportError:
                raise ImportError("ultralytics not installed")
        return self._model

    def process_frame(self, frame: np.ndarray) -> List[Dict]:
        """Run inference on a single frame.

        Returns:
            List of detections with class, confidence, and bounding box.
        """
        model = self._load_model()
        results = model(frame, conf=self.confidence_threshold, verbose=False)
        detections = []

        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    detections.append({
                        "class_id": int(box.cls[0]),
                        "class_name": model.names[int(box.cls[0])],
                        "confidence": float(box.conf[0]),
                        "bbox": box.xyxy[0].tolist(),
                    })

        return detections

    def process_video(self, video_path: str, output_path: Optional[str] = None,
                      frame_interval: int = 10) -> List[Dict]:
        """Process entire video and return all detections.

        Args:
            video_path: Path to input video.
            output_path: Optional path to save annotated output video.
            frame_interval: Process every Nth frame.

        Returns:
            List of frame detections with timestamps.
        """
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        all_detections = []
        frame_idx = 0
        writer = None

        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            writer = cv2.VideoWriter(output_path, fourcc, fps / frame_interval, (width, height))

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_idx % frame_interval == 0:
                detections = self.process_frame(frame)
                timestamp = frame_idx / fps if fps > 0 else 0
                all_detections.append({
                    "frame_idx": frame_idx,
                    "timestamp_seconds": round(timestamp, 2),
                    "detections": detections,
                })

                if writer and detections:
                    annotated = self._draw_boxes(frame, detections)
                    writer.write(annotated)

            frame_idx += 1

        cap.release()
        if writer:
            writer.release()

        return all_detections

    def _draw_boxes(self, frame: np.ndarray, detections: List[Dict]) -> np.ndarray:
        """Draw bounding boxes and labels on frame."""
        colors = {0: (0, 255, 0), 1: (0, 0, 255), 2: (255, 255, 0)}
        for det in detections:
            x1, y1, x2, y2 = map(int, det["bbox"])
            color = colors.get(det["class_id"], (255, 255, 255))
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            label = f"{det['class_name']}: {det['confidence']:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        return frame

    def detect_anomaly_in_video(self, video_path: str,
                                 anomaly_threshold: float = 0.3) -> Dict:
        """Analyze video and determine if anomalies are present.

        Returns:
            Summary with anomaly score and alert level.
        """
        detections = self.process_video(video_path)
        total_frames = len(detections)
        if total_frames == 0:
            return {"anomaly_detected": False, "score": 0.0, "level": "normal"}

        anomaly_frames = sum(
            1 for d in detections
            if any(det["class_name"] == "anomalous_bleeding" and det["confidence"] > 0.5
                   for det in d["detections"])
        )
        anomaly_ratio = anomaly_frames / total_frames

        if anomaly_ratio > anomaly_threshold:
            level = "critical" if anomaly_ratio > 0.5 else "high"
        elif anomaly_ratio > anomaly_threshold / 2:
            level = "medium"
        else:
            level = "low"

        return {
            "anomaly_detected": anomaly_ratio > 0,
            "score": round(anomaly_ratio * 100, 2),
            "level": level,
            "total_frames": total_frames,
            "anomalous_frames": anomaly_frames,
        }

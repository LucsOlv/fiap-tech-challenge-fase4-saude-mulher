"""Dataset loading and preprocessing for surgical video analysis."""

import os
from pathlib import Path
from typing import List, Tuple, Optional
import cv2
import numpy as np


class VideoDataset:
    """Dataset class for surgical and clinical videos.

    Handles loading videos, extracting frames, and managing labels
    for YOLOv8 training on anomalous bleeding detection.
    """

    def __init__(self, data_dir: str = "data/raw", annotation_dir: str = "data/processed"):
        self.data_dir = Path(data_dir)
        self.annotation_dir = Path(annotation_dir)
        self.classes = ["normal", "anomalous_bleeding", "surgical_instrument",
                        "critical_area", "discomfort_signal"]

    def list_videos(self) -> List[Path]:
        """List all video files in the data directory."""
        video_extensions = {".mp4", ".avi", ".mov", ".mkv"}
        videos = []
        for ext in video_extensions:
            videos.extend(self.data_dir.glob(f"*{ext}"))
        return sorted(videos)

    def extract_frames(self, video_path: Path, output_dir: Path,
                       frame_interval: int = 30) -> List[Path]:
        """Extract frames from a video at specified intervals.

        Args:
            video_path: Path to the video file.
            output_dir: Directory to save extracted frames.
            frame_interval: Extract every Nth frame.

        Returns:
            List of paths to extracted frames.
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        cap = cv2.VideoCapture(str(video_path))
        frames = []
        frame_count = 0
        saved_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_count % frame_interval == 0:
                frame_path = output_dir / f"{video_path.stem}_f{saved_count:06d}.jpg"
                cv2.imwrite(str(frame_path), frame)
                frames.append(frame_path)
                saved_count += 1
            frame_count += 1

        cap.release()
        return frames

    def load_frame(self, frame_path: Path, target_size: Tuple[int, int] = (640, 640)) -> np.ndarray:
        """Load and resize a single frame."""
        frame = cv2.imread(str(frame_path))
        if frame is None:
            raise FileNotFoundError(f"Cannot read frame: {frame_path}")
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, target_size)
        return frame

    def get_video_metadata(self, video_path: Path) -> dict:
        """Extract video metadata."""
        cap = cv2.VideoCapture(str(video_path))
        metadata = {
            "path": str(video_path),
            "fps": cap.get(cv2.CAP_PROP_FPS),
            "frame_count": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            "duration_seconds": 0,
        }
        if metadata["fps"] > 0:
            metadata["duration_seconds"] = metadata["frame_count"] / metadata["fps"]
        cap.release()
        return metadata

    def validate_frame(self, frame: np.ndarray) -> bool:
        """Validate that a frame is suitable for processing."""
        if frame is None or frame.size == 0:
            return False
        if frame.shape[0] < 100 or frame.shape[1] < 100:
            return False
        # Check if frame is too dark (mean pixel value < 10)
        if np.mean(frame) < 10:
            return False
        return True

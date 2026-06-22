"""Video preprocessing pipeline for surgical video analysis."""

from pathlib import Path
from typing import Tuple
import cv2
import numpy as np


class VideoPreprocessor:
    """Preprocessing pipeline for surgical and clinical videos.

    Handles frame normalization, contrast enhancement, and artifact
    removal specific to medical imaging contexts.
    """

    def __init__(self, target_size: Tuple[int, int] = (640, 640)):
        self.target_size = target_size

    def normalize(self, frame: np.ndarray) -> np.ndarray:
        """Normalize frame pixel values to [0, 1] range."""
        return frame.astype(np.float32) / 255.0

    def denormalize(self, frame: np.ndarray) -> np.ndarray:
        """Convert normalized frame back to uint8."""
        return (np.clip(frame, 0, 1) * 255).astype(np.uint8)

    def enhance_contrast(self, frame: np.ndarray) -> np.ndarray:
        """Apply CLAHE contrast enhancement for better feature visibility."""
        lab = cv2.cvtColor(frame, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        lab = cv2.merge([l, a, b])
        return cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)

    def remove_specular_reflections(self, frame: np.ndarray,
                                     threshold: int = 240) -> np.ndarray:
        """Reduce specular reflections common in surgical lighting."""
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        mask = gray > threshold
        frame = frame.copy()
        frame[mask] = cv2.inpaint(frame, mask.astype(np.uint8), 3, cv2.INPAINT_TELEA)[mask]
        return frame

    def resize(self, frame: np.ndarray) -> np.ndarray:
        """Resize frame to target dimensions."""
        return cv2.resize(frame, self.target_size)

    def preprocess(self, frame: np.ndarray) -> np.ndarray:
        """Full preprocessing pipeline."""
        frame = self.resize(frame)
        frame = self.remove_specular_reflections(frame)
        frame = self.enhance_contrast(frame)
        frame = self.normalize(frame)
        return frame

    def preprocess_batch(self, frames: np.ndarray) -> np.ndarray:
        """Preprocess a batch of frames."""
        processed = []
        for frame in frames:
            processed.append(self.preprocess(frame))
        return np.stack(processed)

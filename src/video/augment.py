"""Data augmentation for surgical video frames."""

import random
import cv2
import numpy as np


class VideoAugmenter:
    """Data augmentation strategies for surgical video analysis.

    Implements augmentations suitable for medical imaging:
    rotation, flipping, brightness/contrast shifts, and
    simulated lighting variations.
    """

    def __init__(self, seed: int = 42):
        random.seed(seed)
        np.random.seed(seed)

    def random_rotation(self, frame: np.ndarray, max_angle: float = 15.0) -> np.ndarray:
        """Apply random rotation within max_angle degrees."""
        angle = random.uniform(-max_angle, max_angle)
        h, w = frame.shape[:2]
        matrix = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
        return cv2.warpAffine(frame, matrix, (w, h), borderMode=cv2.BORDER_REFLECT)

    def random_flip(self, frame: np.ndarray, prob: float = 0.5) -> np.ndarray:
        """Random horizontal flip."""
        if random.random() < prob:
            return cv2.flip(frame, 1)
        return frame

    def random_brightness_contrast(self, frame: np.ndarray,
                                    brightness_range: float = 0.2,
                                    contrast_range: float = 0.2) -> np.ndarray:
        """Adjust brightness and contrast randomly."""
        alpha = 1.0 + random.uniform(-contrast_range, contrast_range)
        beta = random.uniform(-brightness_range, brightness_range) * 255
        return cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

    def random_blur(self, frame: np.ndarray, prob: float = 0.3,
                    max_kernel: int = 5) -> np.ndarray:
        """Apply random Gaussian blur to simulate motion."""
        if random.random() < prob:
            ksize = random.choice([3, 5])
            if ksize > max_kernel:
                ksize = max_kernel
            if ksize % 2 == 0:
                ksize += 1
            return cv2.GaussianBlur(frame, (ksize, ksize), 0)
        return frame

    def random_noise(self, frame: np.ndarray, sigma: float = 10.0,
                     prob: float = 0.3) -> np.ndarray:
        """Add random Gaussian noise."""
        if random.random() < prob:
            noise = np.random.normal(0, sigma, frame.shape).astype(np.float32)
            frame = frame.astype(np.float32) + noise
            frame = np.clip(frame, 0, 255).astype(np.uint8)
        return frame

    def augment(self, frame: np.ndarray) -> np.ndarray:
        """Apply a random augmentation pipeline."""
        frame = self.random_flip(frame)
        frame = self.random_rotation(frame)
        frame = self.random_brightness_contrast(frame)
        frame = self.random_blur(frame)
        frame = self.random_noise(frame)
        return frame

    def augment_batch(self, frames: np.ndarray) -> np.ndarray:
        """Augment a batch of frames."""
        return np.stack([self.augment(f) for f in frames])

"""Tests for video augmentation module."""

import numpy as np
from src.video.augment import VideoAugmenter


class TestVideoAugmenter:
    """Test VideoAugmenter class."""

    def test_init(self):
        aug = VideoAugmenter(seed=42)
        assert aug is not None

    def test_random_flip(self, sample_frame):
        aug = VideoAugmenter(seed=42)
        flipped = aug.random_flip(sample_frame, prob=1.0)
        assert flipped.shape == sample_frame.shape

    def test_random_rotation(self, sample_frame):
        aug = VideoAugmenter(seed=42)
        rotated = aug.random_rotation(sample_frame, max_angle=15.0)
        assert rotated.shape == sample_frame.shape

    def test_random_brightness_contrast(self, sample_frame):
        aug = VideoAugmenter(seed=42)
        adjusted = aug.random_brightness_contrast(sample_frame, 0.2, 0.2)
        assert adjusted.shape == sample_frame.shape

    def test_random_blur(self, sample_frame):
        aug = VideoAugmenter(seed=42)
        blurred = aug.random_blur(sample_frame, prob=1.0)
        assert blurred.shape == sample_frame.shape

    def test_random_noise(self, sample_frame):
        aug = VideoAugmenter(seed=42)
        noisy = aug.random_noise(sample_frame, sigma=10.0, prob=1.0)
        assert noisy.shape == sample_frame.shape

    def test_augment_pipeline(self, sample_frame):
        aug = VideoAugmenter(seed=42)
        result = aug.augment(sample_frame)
        assert result.shape == sample_frame.shape

    def test_augment_batch(self, sample_frame):
        aug = VideoAugmenter(seed=42)
        batch = np.stack([sample_frame] * 4)
        result = aug.augment_batch(batch)
        assert result.shape == batch.shape

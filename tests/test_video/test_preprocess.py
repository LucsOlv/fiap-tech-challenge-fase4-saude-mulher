"""Tests for video preprocessing module."""

import numpy as np
from src.video.preprocess import VideoPreprocessor


class TestVideoPreprocessor:
    """Test VideoPreprocessor class."""

    def test_init(self):
        pp = VideoPreprocessor(target_size=(320, 320))
        assert pp.target_size == (320, 320)

    def test_normalize(self, sample_frame):
        pp = VideoPreprocessor()
        norm = pp.normalize(sample_frame)
        assert norm.dtype == np.float32
        assert norm.min() >= 0.0
        assert norm.max() <= 1.0

    def test_denormalize(self, sample_frame):
        pp = VideoPreprocessor()
        norm = pp.normalize(sample_frame)
        denorm = pp.denormalize(norm)
        assert denorm.dtype == np.uint8
        assert denorm.shape == sample_frame.shape

    def test_resize(self, sample_frame):
        pp = VideoPreprocessor(target_size=(320, 320))
        resized = pp.resize(sample_frame)
        assert resized.shape == (320, 320, 3)

    def test_enhance_contrast(self, sample_frame):
        pp = VideoPreprocessor()
        enhanced = pp.enhance_contrast(sample_frame)
        assert enhanced.shape == sample_frame.shape
        assert enhanced.dtype == np.uint8

    def test_preprocess_pipeline(self, sample_frame):
        pp = VideoPreprocessor()
        processed = pp.preprocess(sample_frame)
        assert processed.shape == (640, 640, 3)
        assert processed.dtype == np.float32

    def test_preprocess_batch(self, sample_frame):
        pp = VideoPreprocessor()
        batch = np.stack([sample_frame] * 4)
        processed = pp.preprocess_batch(batch)
        assert processed.shape == (4, 640, 640, 3)

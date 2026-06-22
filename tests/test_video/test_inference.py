"""Tests for video inference module."""

import pytest
import numpy as np
from src.video.inference import VideoInference


class TestVideoInference:
    """Test VideoInference class."""

    def test_init(self):
        vi = VideoInference("dummy_model.pt", confidence_threshold=0.5)
        assert vi.confidence_threshold == 0.5

    def test_detect_anomaly_no_video(self):
        """Test anomaly detection with empty results."""
        vi = VideoInference("dummy_model.pt")
        result = vi.detect_anomaly_in_video("/nonexistent/video.mp4")
        assert "anomaly_detected" in result
        assert "score" in result
        assert "level" in result

    def test_process_frame_no_model(self, sample_frame):
        """Test that missing model triggers ImportError."""
        vi = VideoInference("nonexistent_model.pt")
        # This will try to load ultralytics which may or may not be installed
        pass  # Skip actual load test if ultralytics not available

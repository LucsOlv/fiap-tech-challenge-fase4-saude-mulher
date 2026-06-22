"""Tests for video dataset module."""

import pytest
import numpy as np
from pathlib import Path
import tempfile
import cv2

from src.video.dataset import VideoDataset


class TestVideoDataset:
    """Test VideoDataset class."""

    def test_init_default_dir(self):
        ds = VideoDataset()
        assert ds.classes == ["normal", "anomalous_bleeding", "surgical_instrument",
                              "critical_area", "discomfort_signal"]

    def test_load_frame(self, sample_frame):
        """Test loading a single frame from file."""
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            cv2.imwrite(tmp.name, cv2.cvtColor(sample_frame, cv2.COLOR_RGB2BGR))

        ds = VideoDataset()
        frame = ds.load_frame(Path(tmp.name))
        assert frame.shape == (640, 640, 3)
        Path(tmp.name).unlink()

    def test_load_frame_not_found(self):
        ds = VideoDataset()
        with pytest.raises(FileNotFoundError):
            ds.load_frame(Path("/nonexistent/frame.jpg"))

    def test_validate_frame_valid(self, sample_frame):
        ds = VideoDataset()
        assert ds.validate_frame(sample_frame) is True

    def test_validate_frame_none(self):
        ds = VideoDataset()
        assert ds.validate_frame(None) is False

    def test_validate_frame_too_small(self):
        ds = VideoDataset()
        tiny = np.zeros((50, 50, 3), dtype=np.uint8)
        assert ds.validate_frame(tiny) is False

    def test_get_video_metadata(self, sample_video_path):
        ds = VideoDataset()
        meta = ds.get_video_metadata(Path(sample_video_path))
        assert meta["frame_count"] == 30
        assert meta["width"] == 640
        assert meta["height"] == 480
        assert meta["fps"] > 0

    def test_extract_frames(self, sample_video_path):
        ds = VideoDataset()
        output_dir = Path(tempfile.mkdtemp())
        frames = ds.extract_frames(Path(sample_video_path), output_dir, frame_interval=10)
        assert len(frames) > 0
        assert all(f.exists() for f in frames)

        # Cleanup
        for f in frames:
            f.unlink()
        output_dir.rmdir()

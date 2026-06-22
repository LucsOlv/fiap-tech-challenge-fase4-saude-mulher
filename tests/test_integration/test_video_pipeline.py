"""Integration tests for video analysis pipeline."""

import pytest
from pathlib import Path
from src.video.dataset import VideoDataset
from src.video.preprocess import VideoPreprocessor
from src.video.augment import VideoAugmenter
from src.video.report_generator import ReportGenerator
from src.video.alert_manager import AlertManager


class TestVideoPipeline:
    """End-to-end video pipeline tests."""

    def test_full_pipeline_no_model(self, sample_video_path):
        """Test pipeline from loading to report generation (no GPU needed)."""
        # Dataset
        ds = VideoDataset()
        meta = ds.get_video_metadata(Path(sample_video_path))
        assert meta["frame_count"] > 0

        # Preprocessor
        pp = VideoPreprocessor()
        assert pp is not None

        # Augmenter
        aug = VideoAugmenter()
        assert aug is not None

        # Report Generator
        rg = ReportGenerator()
        detections = [
            {"frame_idx": 0, "timestamp_seconds": 0.0,
             "detections": [{"class_name": "anomalous_bleeding", "confidence": 0.9,
                             "class_id": 1, "bbox": [0, 0, 100, 100]}]},
        ]
        report = rg.generate_report(str(sample_video_path), detections)
        assert len(report["alerts"]) > 0

        # Alert Manager
        am = AlertManager()
        alert = am.create_alert("bleeding", "critical", "Test pipeline alert")
        assert alert is not None

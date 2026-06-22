"""Tests for anomaly detector module."""

from src.fusion.anomaly_detector import AnomalyDetector


class TestAnomalyDetector:
    """Test AnomalyDetector class."""

    def test_init(self):
        ad = AnomalyDetector(window_size=30)
        assert ad.window_size == 30

    def test_add_reading_insufficient_data(self):
        ad = AnomalyDetector()
        result = ad.add_reading("systolic", 120, "2026-01-01T00:00:00")
        assert result["status"] == "insufficient_data"
        assert result["anomaly"] is False

    def test_add_readings_and_detect_anomaly(self):
        ad = AnomalyDetector(window_size=30)
        # Add normal readings
        for i in range(20):
            ad.add_reading("systolic", 120 + i * 0.5, f"t{i}")
        # Add anomalous reading
        result = ad.add_reading("systolic", 180, "t20")
        assert "z_score" in result

    def test_clinical_thresholds_high(self):
        ad = AnomalyDetector()
        # Pre-fill with normal data
        for i in range(15):
            ad.add_reading("systolic", 120, f"t{i}")
        result = ad.add_reading("systolic", 160, "t15")
        assert bool(result["anomaly"]) is True

    def test_fetal_hr_range(self):
        ad = AnomalyDetector()
        result = ad._check_clinical_thresholds("fetal_hr", 180)
        assert result["alert"] is True

    def test_unknown_measurement(self):
        ad = AnomalyDetector()
        result = ad.add_reading("unknown_type", 100, "t0")
        assert "error" in result

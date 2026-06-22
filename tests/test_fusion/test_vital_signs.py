"""Tests for vital signs monitor module."""

from src.fusion.vital_signs import VitalSignsMonitor


class TestVitalSignsMonitor:
    """Test VitalSignsMonitor class."""

    def test_record_normal_bp(self):
        vsm = VitalSignsMonitor()
        result = vsm.record("blood_pressure_systolic", 120)
        assert result["in_range"] is True
        assert result["alert"] is None

    def test_record_high_bp(self):
        vsm = VitalSignsMonitor()
        result = vsm.record("blood_pressure_systolic", 155)
        assert result["in_range"] is False
        assert result["alert"] == "high"

    def test_record_low_fetal_hr(self):
        vsm = VitalSignsMonitor()
        result = vsm.record("fetal_heart_rate", 90)
        assert result["in_range"] is False
        assert result["alert"] == "low"

    def test_get_status(self):
        vsm = VitalSignsMonitor()
        vsm.record("blood_pressure_systolic", 120)
        vsm.record("fetal_heart_rate", 145)
        status = vsm.get_status()
        assert status["total_measurements"] == 2
        assert status["abnormal"] == 0

    def test_preeclampsia_risk_high(self):
        vsm = VitalSignsMonitor()
        result = vsm.check_preeclampsia_risk(160, 105, True)
        assert result["risk_level"] == "critical"

    def test_preeclampsia_risk_normal(self):
        vsm = VitalSignsMonitor()
        result = vsm.check_preeclampsia_risk(115, 75, False)
        assert result["risk_level"] == "low"

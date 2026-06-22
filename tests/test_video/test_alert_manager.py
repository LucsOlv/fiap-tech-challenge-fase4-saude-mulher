"""Tests for alert manager module."""

from src.video.alert_manager import AlertManager


class TestAlertManager:
    """Test AlertManager class."""

    def test_create_alert(self):
        am = AlertManager()
        alert = am.create_alert("bleeding", "critical", "Test alert")
        assert alert["id"].startswith("ALT-")
        assert alert["severity"] == "critical"
        assert not alert["acknowledged"]

    def test_create_alert_invalid_severity(self):
        import pytest
        am = AlertManager()
        with pytest.raises(ValueError):
            am.create_alert("test", "invalid", "msg")

    def test_get_active_alerts(self):
        am = AlertManager()
        am.create_alert("t1", "low", "Low priority")
        am.create_alert("t2", "critical", "Critical alert")
        am.create_alert("t3", "high", "High priority")

        active = am.get_active_alerts(min_severity="high")
        assert len(active) >= 2  # high and critical

    def test_acknowledge_alert(self):
        am = AlertManager()
        alert = am.create_alert("test", "medium", "Test")
        assert am.acknowledge_alert(alert["id"]) is True
        assert am.acknowledge_alert("nonexistent") is False

    def test_get_alert_summary(self):
        am = AlertManager()
        am.create_alert("t1", "low", "msg")
        am.create_alert("t2", "critical", "msg")

        summary = am.get_alert_summary()
        assert summary["total_alerts"] == 2
        assert summary["active_alerts"] == 2
        assert "critical" in summary["by_severity"]

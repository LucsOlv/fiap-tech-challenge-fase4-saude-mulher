"""Tests for realtime alerts module."""

from src.fusion.realtime_alerts import RealtimeAlertSystem


class TestRealtimeAlertSystem:
    """Test RealtimeAlertSystem class."""

    def test_create_and_send(self):
        ras = RealtimeAlertSystem()
        alert = ras.create_and_send("PAC-001", "bleeding", "critical",
                                     "Sangramento detectado")
        assert alert["patient_id"] == "PAC-001"
        assert alert["severity"] == "critical"

    def test_subscribe_and_receive(self):
        ras = RealtimeAlertSystem()
        received = []

        def callback(alert):
            received.append(alert)

        ras.subscribe(callback)
        ras.create_and_send("PAC-001", "test", "high", "Test message")
        assert len(received) == 1
        assert received[0]["type"] == "test"

    def test_unsubscribe(self):
        ras = RealtimeAlertSystem()
        received = []

        def callback(alert):
            received.append(alert)

        ras.subscribe(callback)
        ras.unsubscribe(callback)
        ras.create_and_send("PAC-001", "test", "low", "msg")
        assert len(received) == 0

    def test_get_history(self):
        ras = RealtimeAlertSystem()
        ras.create_and_send("PAC-001", "t1", "low", "msg1")
        ras.create_and_send("PAC-002", "t2", "critical", "msg2")

        history = ras.get_history(limit=10)
        assert len(history) == 2

        history_high = ras.get_history(min_severity="high")
        assert len(history_high) == 1

    def test_to_sse_event(self):
        ras = RealtimeAlertSystem()
        alert = ras.create_and_send("PAC-001", "test", "medium", "msg")
        sse = ras.to_sse_event(alert)
        assert sse.startswith("data: ")

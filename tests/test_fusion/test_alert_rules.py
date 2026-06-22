"""Tests for alert rules module."""

from src.fusion.alert_rules import AlertRules


class TestAlertRules:
    """Test AlertRules class."""

    def test_critical_bleeding_rule(self):
        ar = AlertRules()
        context = {"video": {"level": "critical"}}
        triggered = ar.evaluate(context)
        assert any(r["rule_id"] == "CRITICAL_BLEEDING" for r in triggered)

    def test_no_violence_no_trigger(self):
        ar = AlertRules()
        context = {"audio": {"trauma_indicators": {"score": 0.1}}}
        triggered = ar.evaluate(context)
        assert not any(r["rule_id"] == "VIOLENCE_DISCLOSURE" for r in triggered)

    def test_violence_trigger(self):
        ar = AlertRules()
        context = {"audio": {"trauma_indicators": {"score": 0.85}}}
        triggered = ar.evaluate(context)
        assert any(r["rule_id"] == "VIOLENCE_DISCLOSURE" for r in triggered)

    def test_empty_context(self):
        ar = AlertRules()
        triggered = ar.evaluate({})
        assert len(triggered) == 0

    def test_medication_conflict_rule(self):
        ar = AlertRules()
        context = {"text": {"risk_level": "critical"}}
        triggered = ar.evaluate(context)
        assert any(r["rule_id"] == "MEDICATION_CONFLICT" for r in triggered)

"""Clinical alert rules engine for multimodal fusion."""

from typing import Dict, List


class AlertRules:
    """Define and evaluate clinical alert rules."""

    def __init__(self):
        self.rules = self._define_rules()

    def _define_rules(self) -> List[Dict]:
        """Define clinical alert rules."""
        return [
            {
                "id": "CRITICAL_BLEEDING",
                "condition": lambda ctx: ctx.get("video", {}).get("level") == "critical",
                "severity": "critical",
                "message": "Sangramento crítico detectado. Intervenção imediata necessária.",
                "action": "ALERT_SURGICAL_TEAM",
            },
            {
                "id": "VIOLENCE_DISCLOSURE",
                "condition": lambda ctx: ctx.get("audio", {}).get("trauma_indicators", {}).get("score", 0) > 0.7,
                "severity": "critical",
                "message": "Possível relato de violência doméstica detectado na análise de voz.",
                "action": "ALERT_SOCIAL_SERVICES",
            },
            {
                "id": "DEPRESSION_RISK",
                "condition": lambda ctx: ctx.get("audio", {}).get("postpartum_depression_risk", {}).get("score", 0) > 0.6,
                "severity": "high",
                "message": "Risco elevado de depressão pós-parto detectado.",
                "action": "REFER_PSYCHIATRY",
            },
            {
                "id": "MEDICATION_CONFLICT",
                "condition": lambda ctx: ctx.get("text", {}).get("risk_level") == "critical",
                "severity": "high",
                "message": "Conflito medicamentoso ou contraindicação detectada na prescrição.",
                "action": "REVIEW_PRESCRIPTION",
            },
            {
                "id": "VITAL_SIGNS_ANOMALY",
                "condition": lambda ctx: ctx.get("vitals", {}).get("anomaly_detected", False),
                "severity": "high",
                "message": "Anomalia em sinais vitais detectada.",
                "action": "CHECK_VITALS",
            },
        ]

    def evaluate(self, context: Dict) -> List[Dict]:
        """Evaluate all rules against the given context.

        Args:
            context: Dict with video, audio, text, and vitals results.

        Returns:
            List of triggered alerts.
        """
        triggered = []
        for rule in self.rules:
            try:
                if rule["condition"](context):
                    triggered.append({
                        "rule_id": rule["id"],
                        "severity": rule["severity"],
                        "message": rule["message"],
                        "recommended_action": rule["action"],
                    })
            except Exception:
                continue
        return triggered

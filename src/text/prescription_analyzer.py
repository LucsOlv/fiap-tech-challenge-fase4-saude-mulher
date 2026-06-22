"""Analyze medical prescriptions for anomalies and risks."""

from typing import Dict, List
import re


class PrescriptionAnalyzer:
    """Analyze obstetrics and gynecology prescriptions for anomalies."""

    # Drug interactions to flag (OB/GYN context)
    INTERACTIONS = {
        ("ocitocina", "misoprostol"): "HIGH: Combined uterotonic effect risk",
        ("metildopa", "nifedipina"): "MEDIUM: Additive hypotensive effect",
        ("sulfato de magnésio", "nifedipina"): "HIGH: Neuromuscular blockade risk",
        ("sertralina", "fluoxetina"): "HIGH: Serotonin syndrome risk",
    }

    # Pregnancy category D/X drugs (contraindicated)
    PREGNANCY_CONTRAINDICATED = [
        "misoprostol", "metotrexato", "isotretinoína", "warfarina",
        "valsartana", "losartana", "enalapril", "captopril",
    ]

    def analyze(self, prescription_text: str) -> Dict:
        """Analyze prescription for anomalies and risks.

        Returns:
            Dict with risk score, alerts, and recommendations.
        """
        text_lower = prescription_text.lower()
        alerts = []
        risk_score = 0.0

        # Check for pregnancy-contraindicated drugs
        contraindicated = [d for d in self.PREGNANCY_CONTRAINDICATED if d in text_lower]
        if contraindicated:
            alerts.append({
                "type": "contraindicated_medication",
                "severity": "critical",
                "medications": contraindicated,
                "message": f"Medicação contraindicada na gestação: {', '.join(contraindicated)}",
            })
            risk_score += 0.4

        # Check for drug interactions
        for (drug1, drug2), risk in self.INTERACTIONS.items():
            if drug1 in text_lower and drug2 in text_lower:
                alerts.append({
                    "type": "drug_interaction",
                    "severity": "high" if "HIGH" in risk else "medium",
                    "drugs": [drug1, drug2],
                    "message": risk,
                })
                risk_score += 0.3

        # Check dosage anomalies
        dosage_issues = self._check_dosages(prescription_text)
        if dosage_issues:
            alerts.extend(dosage_issues)
            risk_score += 0.15 * len(dosage_issues)

        # Check for missing information
        if "dose" not in text_lower and "mg" not in text_lower:
            alerts.append({
                "type": "missing_info",
                "severity": "medium",
                "message": "Prescrição sem informação de dosagem",
            })

        return {
            "risk_score": round(min(risk_score, 1.0), 2),
            "risk_level": "critical" if risk_score > 0.7 else "high" if risk_score > 0.4 else "medium" if risk_score > 0.2 else "low",
            "alerts": alerts,
            "safe_for_pregnancy": len(contraindicated) == 0 if 'contraindicated' in dir() else True,
        }

    def _check_dosages(self, text: str) -> List[Dict]:
        """Check for dosage anomalies."""
        issues = []
        # Check for suspiciously high doses
        high_doses = re.findall(r"(\d{3,})\s*(mg|mcg|g)", text, re.IGNORECASE)
        if high_doses:
            issues.append({
                "type": "high_dosage",
                "severity": "medium",
                "message": f"Dosagem potencialmente elevada: {high_doses}",
            })
        return issues

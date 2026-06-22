"""Vital signs processing and monitoring for pregnant patients."""

from typing import Dict, List, Optional
from datetime import datetime


class VitalSignsMonitor:
    """Monitor and process vital signs specifically for maternal health."""

    # Clinical reference ranges for pregnancy
    REFERENCE_RANGES = {
        "blood_pressure_systolic": {"low": 90, "high": 140, "unit": "mmHg"},
        "blood_pressure_diastolic": {"low": 60, "high": 90, "unit": "mmHg"},
        "fetal_heart_rate": {"low": 110, "high": 160, "unit": "bpm"},
        "maternal_heart_rate": {"low": 60, "high": 100, "unit": "bpm"},
        "temperature": {"low": 36.0, "high": 37.8, "unit": "°C"},
        "oxygen_saturation": {"low": 95, "high": 100, "unit": "%"},
    }

    def __init__(self):
        self.current_readings: Dict[str, Dict] = {}

    def record(self, measurement_type: str, value: float) -> Dict:
        """Record a vital sign measurement and assess it.

        Returns:
            Assessment with status and alerts.
        """
        ref = self.REFERENCE_RANGES.get(measurement_type)
        reading = {
            "type": measurement_type,
            "value": value,
            "timestamp": datetime.now().isoformat(),
        }

        if ref:
            in_range = ref["low"] <= value <= ref["high"]
            reading["in_range"] = in_range
            reading["reference_range"] = f"{ref['low']}-{ref['high']} {ref['unit']}"

            if not in_range:
                reading["alert"] = "high" if value > ref["high"] else "low"
                reading["alert_message"] = (
                    f"{measurement_type}: {value} {ref['unit']} "
                    f"(ref: {ref['low']}-{ref['high']})"
                )
            else:
                reading["alert"] = None

        self.current_readings[measurement_type] = reading
        return reading

    def get_status(self) -> Dict:
        """Get current vital signs status summary."""
        alerts = []
        normal_count = 0
        total = len(self.current_readings)

        for mtype, reading in self.current_readings.items():
            if reading.get("alert"):
                alerts.append(reading)
            else:
                normal_count += 1

        return {
            "total_measurements": total,
            "normal": normal_count,
            "abnormal": len(alerts),
            "alerts": alerts,
            "readings": self.current_readings,
        }

    def check_preeclampsia_risk(self, systolic: float, diastolic: float,
                                  proteinuria: bool = False) -> Dict:
        """Assess preeclampsia risk based on blood pressure and proteinuria."""
        risk_score = 0.0
        factors = []

        if systolic >= 140 or diastolic >= 90:
            risk_score += 0.4
            factors.append("Hipertensão detectada")

        if systolic >= 160 or diastolic >= 110:
            risk_score += 0.3
            factors.append("Hipertensão severa")

        if proteinuria:
            risk_score += 0.3
            factors.append("Proteinúria presente")

        risk_level = "critical" if risk_score >= 0.7 else "high" if risk_score >= 0.5 else "medium" if risk_score >= 0.3 else "low"

        return {
            "preeclampsia_risk_score": round(risk_score, 2),
            "risk_level": risk_level,
            "factors": factors,
            "recommendation": "Avaliação médica urgente" if risk_score >= 0.5 else "Monitoramento contínuo",
        }

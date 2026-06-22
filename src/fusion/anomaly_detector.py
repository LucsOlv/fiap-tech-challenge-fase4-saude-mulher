"""Real-time anomaly detection for vital signs and clinical data."""

from typing import Dict, List, Optional
import numpy as np
from collections import deque


class AnomalyDetector:
    """Detect anomalies in time-series clinical data.

    Monitors: blood pressure, fetal heart rate, hormonal prescriptions,
    and clinical evolution trends.
    """

    def __init__(self, window_size: int = 60, threshold_sigma: float = 3.0):
        self.window_size = window_size
        self.threshold_sigma = threshold_sigma
        self.history = {"systolic": deque(maxlen=window_size),
                        "diastolic": deque(maxlen=window_size),
                        "fetal_hr": deque(maxlen=window_size),
                        "maternal_hr": deque(maxlen=window_size),
                        "temperature": deque(maxlen=window_size)}

    def add_reading(self, measurement_type: str, value: float, timestamp: str) -> Dict:
        """Add a new measurement and check for anomalies.

        Returns:
            Dict with anomaly status, z-score, and alert info.
        """
        if measurement_type not in self.history:
            return {"error": f"Unknown measurement type: {measurement_type}"}

        hist = self.history[measurement_type]
        hist.append(value)

        # Need enough data for statistical comparison
        if len(hist) < 10:
            return {"anomaly": False, "value": value, "status": "insufficient_data"}

        mean = np.mean(hist)
        std = np.std(hist)

        if std < 0.001:
            return {"anomaly": False, "value": value, "z_score": 0.0}

        z_score = abs((value - mean) / std)
        is_anomaly = z_score > self.threshold_sigma

        # Clinical thresholds
        clinical_alert = self._check_clinical_thresholds(measurement_type, value)

        return {
            "anomaly": is_anomaly or clinical_alert["alert"],
            "value": value,
            "z_score": round(z_score, 2),
            "mean": round(mean, 2),
            "std": round(std, 2),
            "clinical_alert": clinical_alert,
            "timestamp": timestamp,
        }

    def _check_clinical_thresholds(self, mtype: str, value: float) -> Dict:
        """Check against clinical reference ranges for pregnancy."""
        thresholds = {
            "systolic": (90, 140),       # mmHg - pre-eclampsia if > 140
            "diastolic": (60, 90),        # mmHg
            "fetal_hr": (110, 160),       # bpm - fetal distress if outside
            "maternal_hr": (60, 100),     # bpm
            "temperature": (36.0, 37.8),  # Celsius
        }

        if mtype in thresholds:
            low, high = thresholds[mtype]
            if value < low or value > high:
                return {"alert": True,
                        "message": f"{mtype} fora do range clínico ({low}-{high}): {value}",
                        "range": [low, high]}
        return {"alert": False, "message": "Dentro dos parâmetros normais"}

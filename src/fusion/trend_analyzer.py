"""Analyze clinical trends over time."""

from typing import Dict, List
from collections import deque
import numpy as np


class TrendAnalyzer:
    """Analyze clinical data trends for early warning signs."""

    def __init__(self, max_history: int = 100):
        self.max_history = max_history
        self.history: Dict[str, deque] = {}

    def add_data_point(self, metric: str, value: float, timestamp: str) -> Dict:
        """Add data point and analyze trend."""
        if metric not in self.history:
            self.history[metric] = deque(maxlen=self.max_history)

        self.history[metric].append({"value": value, "timestamp": timestamp})
        return self.analyze_trend(metric)

    def analyze_trend(self, metric: str) -> Dict:
        """Analyze trend for a specific metric."""
        hist = list(self.history.get(metric, []))
        if len(hist) < 3:
            return {"metric": metric, "trend": "insufficient_data", "values": hist}

        values = [h["value"] for h in hist[-10:]]  # Last 10 points
        mean = np.mean(values)
        std = np.std(values)

        # Simple linear trend
        x = np.arange(len(values))
        if len(values) > 1:
            slope = np.polyfit(x, values, 1)[0]
        else:
            slope = 0

        # Determine trend direction
        if abs(slope) < 0.01 * abs(mean) if mean != 0 else abs(slope) < 0.01:
            direction = "stable"
        elif slope > 0:
            direction = "increasing"
        else:
            direction = "decreasing"

        # Check for concerning trends
        alert = False
        if direction != "stable":
            change_pct = abs(slope * len(values) / abs(mean)) * 100 if mean != 0 else 0
            if change_pct > 20:
                alert = True

        return {
            "metric": metric,
            "trend": direction,
            "slope": round(float(slope), 4),
            "mean": round(float(mean), 2),
            "std": round(float(std), 2),
            "latest_value": values[-1],
            "change_percent": round(float(slope * len(values) / abs(mean) * 100) if mean != 0 else 0, 1),
            "alert": alert,
            "data_points": len(values),
        }

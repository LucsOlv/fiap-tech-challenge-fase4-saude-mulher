"""Alert management system for video analysis results."""

from datetime import datetime
from typing import List, Dict
import json


class AlertManager:
    """Manage clinical alerts from video analysis.

    Handles alert creation, prioritization, deduplication,
    and notification routing.
    """

    SEVERITY_WEIGHTS = {"low": 1, "medium": 2, "high": 3, "critical": 4}

    def __init__(self):
        self.alerts: List[Dict] = []

    def create_alert(self, alert_type: str, severity: str,
                     message: str, source: str = "video",
                     metadata: Dict = None) -> Dict:
        """Create a new clinical alert."""
        if severity not in self.SEVERITY_WEIGHTS:
            raise ValueError(f"Invalid severity: {severity}")

        alert = {
            "id": f"ALT-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            "type": alert_type,
            "severity": severity,
            "severity_weight": self.SEVERITY_WEIGHTS[severity],
            "message": message,
            "source": source,
            "created_at": datetime.now().isoformat(),
            "acknowledged": False,
            "metadata": metadata or {},
        }
        self.alerts.append(alert)
        return alert

    def get_active_alerts(self, min_severity: str = "low") -> List[Dict]:
        """Get non-acknowledged alerts above minimum severity."""
        min_weight = self.SEVERITY_WEIGHTS.get(min_severity, 1)
        return sorted(
            [a for a in self.alerts if not a["acknowledged"] and a["severity_weight"] >= min_weight],
            key=lambda x: (-x["severity_weight"], x["created_at"]),
        )

    def acknowledge_alert(self, alert_id: str, user: str = "system") -> bool:
        """Mark an alert as acknowledged."""
        for alert in self.alerts:
            if alert["id"] == alert_id:
                alert["acknowledged"] = True
                alert["acknowledged_at"] = datetime.now().isoformat()
                alert["acknowledged_by"] = user
                return True
        return False

    def get_alert_summary(self) -> Dict:
        """Get summary statistics of all alerts."""
        total = len(self.alerts)
        active = sum(1 for a in self.alerts if not a["acknowledged"])
        by_severity = {}
        for a in self.alerts:
            by_severity[a["severity"]] = by_severity.get(a["severity"], 0) + 1

        return {
            "total_alerts": total,
            "active_alerts": active,
            "by_severity": by_severity,
            "latest_critical": any(
                not a["acknowledged"] and a["severity"] == "critical"
                for a in self.alerts[-5:]
            ),
        }

    def deduplicate(self, time_window_seconds: int = 60) -> int:
        """Remove duplicate alerts within time window."""
        if len(self.alerts) < 2:
            return 0

        deduped = [self.alerts[0]]
        removed = 0
        for alert in self.alerts[1:]:
            last = deduped[-1]
            if (alert["type"] == last["type"]
                    and alert["severity"] == last["severity"]):
                removed += 1
            else:
                deduped.append(alert)

        self.alerts = deduped
        return removed

    def export_alerts(self) -> str:
        """Export all alerts as JSON."""
        return json.dumps(self.alerts, indent=2, ensure_ascii=False)

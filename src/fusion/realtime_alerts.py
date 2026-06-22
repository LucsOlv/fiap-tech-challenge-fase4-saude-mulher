"""Real-time alert delivery system."""

from typing import Dict, List, Callable, Optional
from datetime import datetime
import json
import threading


class RealtimeAlertSystem:
    """Real-time clinical alert delivery system.

    Supports WebSocket/SSE for live dashboard updates and
    callback-based notification routing.
    """

    def __init__(self):
        self.subscribers: List[Callable] = []
        self.alert_history: List[Dict] = []
        self._lock = threading.Lock()

    def subscribe(self, callback: Callable[[Dict], None]):
        """Subscribe to real-time alerts."""
        self.subscribers.append(callback)

    def unsubscribe(self, callback: Callable[[Dict], None]):
        """Unsubscribe from alerts."""
        if callback in self.subscribers:
            self.subscribers.remove(callback)

    def send_alert(self, alert: Dict):
        """Send alert to all subscribers immediately."""
        alert["delivered_at"] = datetime.now().isoformat()

        with self._lock:
            self.alert_history.append(alert)

        for callback in self.subscribers:
            try:
                callback(alert)
            except Exception:
                pass

    def create_and_send(self, patient_id: str, alert_type: str,
                        severity: str, message: str,
                        source: str = "system",
                        metadata: Dict = None) -> Dict:
        """Create and broadcast a new alert."""
        severity_weights = {"low": 1, "medium": 2, "high": 3, "critical": 4}

        alert = {
            "id": f"ALT-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            "patient_id": patient_id,
            "type": alert_type,
            "severity": severity,
            "severity_weight": severity_weights.get(severity, 1),
            "message": message,
            "source": source,
            "created_at": datetime.now().isoformat(),
            "metadata": metadata or {},
        }

        self.send_alert(alert)
        return alert

    def get_history(self, limit: int = 50, min_severity: str = "low") -> List[Dict]:
        """Get recent alert history."""
        severity_weights = {"low": 1, "medium": 2, "high": 3, "critical": 4}
        min_weight = severity_weights.get(min_severity, 1)

        with self._lock:
            filtered = [a for a in self.alert_history
                        if severity_weights.get(a["severity"], 1) >= min_weight]
            return sorted(filtered, key=lambda x: x["created_at"], reverse=True)[:limit]

    def to_sse_event(self, alert: Dict) -> str:
        """Format alert as Server-Sent Event."""
        data = json.dumps(alert, ensure_ascii=False)
        return f"data: {data}\n\n"

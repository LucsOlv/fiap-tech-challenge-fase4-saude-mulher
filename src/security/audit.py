"""Audit logging for security and compliance."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional


class AuditLogger:
    """Track all data access and modifications for LGPD compliance."""

    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "audit.jsonl"

    def log_event(self, event_type: str, user: str, target: str,
                  action: str, details: Dict = None, success: bool = True):
        """Log an auditable event."""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "user": user,
            "target": target,
            "action": action,
            "success": success,
            "details": details or {},
        }

        with open(self.log_file, "a") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")

    def log_access(self, user: str, resource: str, resource_type: str):
        """Log data access event."""
        self.log_event("ACCESS", user, resource, "read",
                        {"resource_type": resource_type})

    def log_modification(self, user: str, resource: str,
                          change_description: str):
        """Log data modification event."""
        self.log_event("MODIFICATION", user, resource, "write",
                        {"change": change_description})

    def log_security_event(self, user: str, event: str, success: bool):
        """Log security-related event."""
        self.log_event("SECURITY", user, "system", event, success=success)

    def get_logs(self, event_type: str = None, user: str = None,
                 limit: int = 100) -> list:
        """Query audit logs."""
        if not self.log_file.exists():
            return []

        logs = []
        with open(self.log_file, "r") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if event_type and entry.get("event_type") != event_type:
                        continue
                    if user and entry.get("user") != user:
                        continue
                    logs.append(entry)
                except json.JSONDecodeError:
                    continue

        return logs[-limit:]

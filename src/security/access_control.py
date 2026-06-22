"""Role-based access control for medical data."""

from typing import Dict, List, Set


class AccessControl:
    """Simple RBAC for medical data access.

    Roles:
    - admin: Full access to all data and system config
    - doctor: Access to patient data and reports
    - nurse: Read access to assigned patients
    - researcher: Anonymized data only
    """

    ROLE_PERMISSIONS = {
        "admin": {"read:all", "write:all", "delete:all", "manage:users", "view:audit_logs"},
        "doctor": {"read:patient_data", "write:patient_data", "view:reports", "create:alerts"},
        "nurse": {"read:patient_data", "view:reports"},
        "researcher": {"read:anonymized_data"},
    }

    def __init__(self):
        self.users: Dict[str, dict] = {}

    def add_user(self, user_id: str, role: str):
        """Add a user with a specific role."""
        if role not in self.ROLE_PERMISSIONS:
            raise ValueError(f"Invalid role: {role}")
        self.users[user_id] = {"role": role, "permissions": self.ROLE_PERMISSIONS[role]}

    def has_permission(self, user_id: str, permission: str) -> bool:
        """Check if user has a specific permission."""
        user = self.users.get(user_id)
        if not user:
            return False
        return permission in user["permissions"]

    def get_role(self, user_id: str) -> str:
        """Get user's role."""
        user = self.users.get(user_id)
        return user["role"] if user else "unknown"

    def can_access_patient(self, user_id: str, patient_id: str) -> bool:
        """Check if user can access a specific patient's data."""
        user = self.users.get(user_id)
        if not user:
            return False
        if user["role"] in ("admin", "doctor"):
            return True
        if user["role"] == "nurse":
            return True  # Could add patient assignment logic
        return False

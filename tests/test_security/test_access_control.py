"""Tests for access control module."""

from src.security.access_control import AccessControl


class TestAccessControl:
    """Test AccessControl class."""

    def test_add_user(self):
        ac = AccessControl()
        ac.add_user("doctor1", "doctor")
        assert ac.get_role("doctor1") == "doctor"

    def test_add_invalid_role(self):
        import pytest
        ac = AccessControl()
        with pytest.raises(ValueError):
            ac.add_user("u1", "invalid_role")

    def test_has_permission(self):
        ac = AccessControl()
        ac.add_user("doc1", "doctor")
        assert ac.has_permission("doc1", "read:patient_data") is True
        assert ac.has_permission("doc1", "manage:users") is False

    def test_admin_permissions(self):
        ac = AccessControl()
        ac.add_user("admin1", "admin")
        assert ac.has_permission("admin1", "view:audit_logs") is True
        assert ac.has_permission("admin1", "delete:all") is True

    def test_unknown_user(self):
        ac = AccessControl()
        assert ac.has_permission("unknown", "read:patient_data") is False
        assert ac.get_role("unknown") == "unknown"

    def test_can_access_patient(self):
        ac = AccessControl()
        ac.add_user("doc1", "doctor")
        ac.add_user("nurse1", "nurse")
        assert ac.can_access_patient("doc1", "PAC-001") is True
        assert ac.can_access_patient("nurse1", "PAC-001") is True
        assert ac.can_access_patient("unknown", "PAC-001") is False

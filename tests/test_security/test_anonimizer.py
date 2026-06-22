"""Tests for data anonymizer module."""

from src.security.anonimizer import DataAnonimizer


class TestDataAnonimizer:
    """Test DataAnonimizer class."""

    def test_anonymize_text_cpf(self):
        da = DataAnonimizer()
        text = "CPF do paciente: 123.456.789-00"
        result = da.anonymize_text(text)
        assert "123.456.789-00" not in result
        assert "[CPF]" in result

    def test_anonymize_text_cns(self):
        da = DataAnonimizer()
        text = "CNS 123 4567 8901 2345"
        result = da.anonymize_text(text)
        assert "123 4567 8901 2345" not in result

    def test_anonymize_text_phone(self):
        da = DataAnonimizer()
        text = "Tel: (11) 99999-9999"
        result = da.anonymize_text(text)
        assert "99999-9999" not in result

    def test_anonymize_dict(self):
        da = DataAnonimizer()
        data = {"nome": "Maria", "documento": "CPF 123.456.789-00"}
        result = da.anonymize_dict(data)
        assert "123.456.789-00" not in result["documento"]

    def test_create_patient_hash(self):
        da = DataAnonimizer()
        h1 = da.create_patient_hash("PAC-001")
        h2 = da.create_patient_hash("PAC-001")
        assert h1 == h2
        assert len(h1) == 32

"""Tests for text anonymizer module."""

from src.text.anonimizer import TextAnonimizer


class TestTextAnonimizer:
    """Test TextAnonimizer class."""

    def test_anonymize_cpf(self):
        ta = TextAnonimizer()
        text = "Paciente com CPF 123.456.789-00"
        anonymized = ta.anonymize(text)
        assert "123.456.789-00" not in anonymized
        assert "CPF_REMOVIDO" in anonymized

    def test_anonymize_cns(self):
        ta = TextAnonimizer()
        text = "CNS 123 4567 8901 2345 do paciente"
        anonymized = ta.anonymize(text)
        assert "123 4567 8901 2345" not in anonymized
        assert "CNS_REMOVIDO" in anonymized

    def test_anonymize_phone(self):
        ta = TextAnonimizer()
        text = "Telefone: (11) 99999-9999"
        anonymized = ta.anonymize(text)
        assert "99999-9999" not in anonymized

    def test_anonymize_email(self):
        ta = TextAnonimizer()
        text = "Email: paciente@hospital.com.br"
        anonymized = ta.anonymize(text)
        assert "paciente@hospital.com.br" not in anonymized

    def test_hash_id(self):
        ta = TextAnonimizer(salt="test")
        h1 = ta.hash_id("PAC-001")
        h2 = ta.hash_id("PAC-001")
        assert h1 == h2
        assert len(h1) == 12

"""Tests for entity extractor module."""

from src.text.entity_extractor import EntityExtractor


class TestEntityExtractor:
    """Test EntityExtractor class."""

    def test_extract_cpf(self):
        ee = EntityExtractor()
        text = "Paciente CPF 123.456.789-00"
        result = ee.extract(text)
        assert "cpf" in result

    def test_extract_cns(self):
        ee = EntityExtractor()
        text = "CNS: 123 4567 8901 2345"
        result = ee.extract(text)
        assert "cns" in result

    def test_extract_blood_pressure(self):
        ee = EntityExtractor()
        text = "PA: 150/95 mmHg"
        result = ee.extract(text)
        assert "blood_pressure" in result

    def test_extract_medications(self, sample_medical_text):
        ee = EntityExtractor()
        meds = ee.extract_medications(sample_medical_text)
        assert "metildopa" in meds

    def test_extract_diagnoses(self, sample_medical_text):
        ee = EntityExtractor()
        diagnoses = ee.extract_diagnoses(sample_medical_text)
        assert len(diagnoses) > 0

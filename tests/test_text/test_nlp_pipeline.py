"""Tests for NLP pipeline module."""

from src.text.nlp_pipeline import NLPPipeline


class TestNLPPipeline:
    """Test NLPPipeline class."""

    def test_init(self):
        nlp = NLPPipeline(language="pt")
        assert nlp.language == "pt"

    def test_process_basic_text(self):
        nlp = NLPPipeline()
        result = nlp.process("Paciente com hipertensão gestacional.")
        assert "tokens" in result
        assert "sentences" in result
        assert result["word_count"] > 0

    def test_process_medical_text(self, sample_medical_text):
        nlp = NLPPipeline()
        result = nlp.process(sample_medical_text)
        assert result["word_count"] > 10
        assert "clinical_entities" in result

    def test_extract_clinical_entities(self, sample_medical_text):
        nlp = NLPPipeline()
        entities = nlp._extract_clinical_entities(sample_medical_text)
        assert "conditions" in entities
        assert "vital_signs" in entities
        # Should detect pré-eclâmpsia
        assert any("pré-eclâmpsia" in c.lower() or "preeclampsia" in c.lower()
                   for c in entities["conditions"])

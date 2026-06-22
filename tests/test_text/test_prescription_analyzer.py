"""Tests for prescription analyzer module."""

from src.text.prescription_analyzer import PrescriptionAnalyzer


class TestPrescriptionAnalyzer:
    """Test PrescriptionAnalyzer class."""

    def test_analyze_normal_prescription(self):
        pa = PrescriptionAnalyzer()
        text = "Metildopa 500mg VO 8/8h. Ácido fólico 5mg 1x/dia."
        result = pa.analyze(text)
        assert result["risk_level"] in ("low", "medium")

    def test_detect_drug_interaction(self):
        pa = PrescriptionAnalyzer()
        text = "Prescrito ocitocina 5UI e misoprostol 200mcg."
        result = pa.analyze(text)
        assert result["risk_score"] > 0.2
        assert len(result["alerts"]) > 0

    def test_detect_contraindicated_pregnancy(self):
        pa = PrescriptionAnalyzer()
        text = "Paciente gestante. Prescrito misoprostol e enalapril."
        result = pa.analyze(text)
        assert result["risk_score"] > 0.3

    def test_missing_dosage_info(self):
        pa = PrescriptionAnalyzer()
        text = "Prescrito paracetamol, tomar conforme necessário."
        result = pa.analyze(text)
        alerts = [a for a in result["alerts"] if a["type"] == "missing_info"]
        assert len(alerts) > 0

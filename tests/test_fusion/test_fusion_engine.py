"""Tests for fusion engine module."""

from src.fusion.fusion_engine import FusionEngine


class TestFusionEngine:
    """Test FusionEngine class."""

    def test_fuse_empty(self):
        fe = FusionEngine()
        result = fe.fuse()
        assert result["unified_risk_score"] == 0.0
        assert result["risk_level"] == "low"

    def test_fuse_with_video_critical(self):
        fe = FusionEngine()
        video = {"level": "critical", "score": 90.0, "anomalous_frames": 15, "total_frames": 20}
        result = fe.fuse(video_result=video)
        assert result["unified_risk_score"] > 30
        assert len(result["alerts"]) > 0

    def test_fuse_with_audio_high_risk(self):
        fe = FusionEngine()
        audio = {
            "overall_risk_score": 0.85,
            "postpartum_depression_risk": {"score": 0.9, "indicators": ["monotone"]},
            "alerts": [{"condition": "depression", "level": "high",
                        "message": "Elevated depression risk"}],
        }
        result = fe.fuse(audio_result=audio)
        assert result["modality_scores"]["audio"] > 0.7

    def test_fuse_with_text_risk(self):
        fe = FusionEngine()
        text = {"risk_score": 0.8, "risk_level": "high", "alerts": [
            {"type": "contraindicated_medication", "severity": "critical",
             "message": "Medication contraindicated"}
        ]}
        result = fe.fuse(text_result=text)
        assert "text" in result["modality_scores"]

    def test_fuse_multimodal(self):
        fe = FusionEngine()
        video = {"level": "high", "score": 60.0, "anomalous_frames": 5, "total_frames": 20}
        audio = {"overall_risk_score": 0.7, "alerts": []}
        text = {"risk_score": 0.5, "risk_level": "medium", "alerts": []}

        result = fe.fuse(video_result=video, audio_result=audio,
                         text_result=text, patient_id="TEST-001")
        assert result["patient_id"] == "TEST-001"
        assert "unified_risk_score" in result
        assert result["risk_level"] in ("low", "medium", "high", "critical")

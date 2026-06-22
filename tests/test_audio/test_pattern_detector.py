"""Tests for pattern detector module."""

from src.audio.pattern_detector import PatternDetector


class TestPatternDetector:
    """Test PatternDetector class."""

    def test_init(self):
        pd = PatternDetector()
        assert "monotone_threshold" in pd.thresholds

    def test_detect_depression(self):
        pd = PatternDetector()
        features = {"pitch_std": 5.0, "energy_mean": 0.005, "voiced_ratio": 0.3}
        result = pd._detect_depression(features)
        assert result["score"] > 0.5
        assert "monotone_speech" in result["indicators"]

    def test_detect_anxiety(self):
        pd = PatternDetector()
        features = {"zcr_mean": 0.2, "pitch_mean": 350, "pitch_std": 70}
        result = pd._detect_anxiety(features)
        assert result["score"] > 0.5

    def test_detect_trauma(self):
        pd = PatternDetector()
        features = {"pitch_std": 90}
        transcription = {"hesitation": {"has_excessive_pauses": True}}
        result = pd._detect_trauma(features, transcription)
        assert result["score"] > 0.5
        assert "excessive_pauses" in result["indicators"]

    def test_analyze_full(self):
        pd = PatternDetector()
        features = {"pitch_std": 5.0, "energy_mean": 0.005, "voiced_ratio": 0.3,
                     "zcr_mean": 0.05, "pitch_mean": 200}
        result = pd.analyze(features)
        assert "postpartum_depression_risk" in result
        assert "overall_risk_score" in result
        assert isinstance(result["alerts"], list)

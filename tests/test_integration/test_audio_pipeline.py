"""Integration tests for audio analysis pipeline."""

import numpy as np
from src.audio.dataset import AudioDataset
from src.audio.preprocess import AudioPreprocessor
from src.audio.pattern_detector import PatternDetector
from src.audio.sentiment import SentimentAnalyzer


class TestAudioPipeline:
    """End-to-end audio pipeline tests."""

    def test_pipeline_from_features_to_analysis(self, sample_audio):
        """Test audio analysis pipeline without requiring model downloads."""
        audio, sr = sample_audio

        # Dataset
        ds = AudioDataset()
        features = ds.extract_features(audio, sr)
        assert "mfcc_mean" in features

        # Preprocessor
        pp = AudioPreprocessor()
        processed = pp.preprocess(audio)
        assert processed.ndim == 1

        # Pattern Detector
        pd = PatternDetector()
        result = pd.analyze(features)
        assert "overall_risk_score" in result

        # Sentiment
        sa = SentimentAnalyzer()
        sentiment = sa.analyze("Paciente relata estar bem e tranquila.")
        assert sentiment["sentiment_label"] in ("positive", "negative", "neutral")

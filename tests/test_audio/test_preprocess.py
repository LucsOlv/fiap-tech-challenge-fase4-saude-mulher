"""Tests for audio preprocessing module."""

import numpy as np
from src.audio.preprocess import AudioPreprocessor


class TestAudioPreprocessor:
    """Test AudioPreprocessor class."""

    def test_init(self):
        pp = AudioPreprocessor(sample_rate=16000)
        assert pp.sample_rate == 16000

    def test_normalize(self, sample_audio):
        audio, sr = sample_audio
        pp = AudioPreprocessor()
        norm = pp.normalize(audio)
        assert norm.max() <= 1.0
        assert norm.min() >= -1.0

    def test_trim_silence(self):
        pp = AudioPreprocessor()
        # Create audio with silence at edges
        audio = np.concatenate([
            np.zeros(1000),
            np.sin(np.linspace(0, 100, 5000)),
            np.zeros(1000),
        ]).astype(np.float32)
        trimmed = pp.trim_silence(audio)
        assert len(trimmed) < len(audio)

    def test_pad_or_truncate(self):
        pp = AudioPreprocessor(sample_rate=16000, duration_ms=1000)
        # Create 0.5 second audio (8000 samples) - target is 16000
        audio = np.random.randn(8000).astype(np.float32)
        result = pp.pad_or_truncate(audio)
        assert len(result) == 16000

        # Create 2 second audio (32000 samples) - target is 16000
        audio = np.random.randn(32000).astype(np.float32)
        result = pp.pad_or_truncate(audio)
        assert len(result) == 16000

    def test_preprocess(self, sample_audio):
        audio, sr = sample_audio
        pp = AudioPreprocessor()
        processed = pp.preprocess(audio)
        assert processed.ndim == 1
        assert processed.max() <= 1.0

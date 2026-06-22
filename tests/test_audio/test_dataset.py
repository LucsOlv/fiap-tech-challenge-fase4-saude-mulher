"""Tests for audio dataset module."""

import pytest
import numpy as np
from src.audio.dataset import AudioDataset
from pathlib import Path


class TestAudioDataset:
    """Test AudioDataset class."""

    def test_init(self):
        ds = AudioDataset(sample_rate=16000)
        assert ds.sample_rate == 16000

    def test_load_audio(self, sample_audio_path):
        ds = AudioDataset()
        audio, sr = ds.load_audio(Path(sample_audio_path))
        assert sr == 16000
        assert len(audio) > 0

    def test_get_duration(self, sample_audio):
        audio, sr = sample_audio
        ds = AudioDataset()
        duration = ds.get_duration(audio, sr)
        assert duration == pytest.approx(3.0, rel=0.1)

    def test_extract_features(self, sample_audio):
        audio, sr = sample_audio
        ds = AudioDataset()
        features = ds.extract_features(audio, sr)
        assert "mfcc_mean" in features
        assert "energy_mean" in features
        assert "pitch_mean" in features or "pitch_mean" in features

    def test_detect_silence(self, sample_audio):
        audio, sr = sample_audio
        ds = AudioDataset()
        silences = ds.detect_silence(audio, sr, threshold_db=-20)
        assert isinstance(silences, list)

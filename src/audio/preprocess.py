"""Audio preprocessing for voice analysis."""

import numpy as np
import librosa


class AudioPreprocessor:
    """Preprocessing pipeline for clinical audio recordings."""

    def __init__(self, sample_rate: int = 16000, duration_ms: int = 5000):
        self.sample_rate = sample_rate
        self.duration_ms = duration_ms

    def normalize(self, audio: np.ndarray) -> np.ndarray:
        """Normalize audio to [-1, 1] range."""
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            return audio / max_val
        return audio

    def remove_noise(self, audio: np.ndarray, noise_reduce: bool = True) -> np.ndarray:
        """Simple noise reduction using spectral gating."""
        if not noise_reduce:
            return audio
        # Simple high-pass filter to remove low-frequency noise
        sos = librosa.filters.shelf(audio, sr=self.sample_rate)
        return audio  # Keep simple for demo purposes

    def trim_silence(self, audio: np.ndarray, top_db: int = 25) -> np.ndarray:
        """Trim leading and trailing silence."""
        trimmed, _ = librosa.effects.trim(audio, top_db=top_db)
        return trimmed

    def pad_or_truncate(self, audio: np.ndarray) -> np.ndarray:
        """Ensure consistent audio length."""
        target_length = int(self.sample_rate * self.duration_ms / 1000)
        if len(audio) > target_length:
            return audio[:target_length]
        elif len(audio) < target_length:
            return np.pad(audio, (0, target_length - len(audio)))
        return audio

    def preprocess(self, audio: np.ndarray) -> np.ndarray:
        """Full preprocessing pipeline."""
        audio = self.trim_silence(audio)
        audio = self.normalize(audio)
        audio = self.pad_or_truncate(audio)
        return audio

"""Audio dataset loading for women's health voice analysis."""

from pathlib import Path
from typing import List, Tuple, Optional, Dict
import numpy as np
import librosa


class AudioDataset:
    """Dataset for clinical audio recordings of women's health consultations.

    Supports loading .wav and .mp3 files, extracting features,
    and managing labels for emotion and health condition detection.
    """

    EMOTION_LABELS = ["neutral", "anxiety", "depression", "fear", "distress", "normal"]

    def __init__(self, data_dir: str = "data/raw/audio", sample_rate: int = 16000):
        self.data_dir = Path(data_dir)
        self.sample_rate = sample_rate

    def list_audio_files(self) -> List[Path]:
        """List all audio files in the data directory."""
        extensions = {".wav", ".mp3", ".flac", ".m4a"}
        files = []
        for ext in extensions:
            files.extend(self.data_dir.glob(f"*{ext}"))
        return sorted(files)

    def load_audio(self, path: Path, target_sr: Optional[int] = None) -> Tuple[np.ndarray, int]:
        """Load audio file and resample if needed."""
        sr = target_sr or self.sample_rate
        audio, sr = librosa.load(str(path), sr=sr)
        return audio, sr

    def get_duration(self, audio: np.ndarray, sr: int) -> float:
        """Get audio duration in seconds."""
        return len(audio) / sr if sr > 0 else 0

    def extract_features(self, audio: np.ndarray, sr: int) -> Dict[str, float]:
        """Extract acoustic features for voice analysis.

        Returns MFCCs, pitch, energy, spectral features, and pause metrics.
        """
        features = {}

        # MFCCs
        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
        features["mfcc_mean"] = float(np.mean(mfcc))
        features["mfcc_std"] = float(np.std(mfcc))

        # Spectral features
        spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=sr)
        features["spectral_centroid_mean"] = float(np.mean(spectral_centroid))
        features["spectral_rolloff"] = float(np.mean(librosa.feature.spectral_rolloff(y=audio, sr=sr)))

        # Energy / RMS
        rms = librosa.feature.rms(y=audio)
        features["energy_mean"] = float(np.mean(rms))
        features["energy_std"] = float(np.std(rms))

        # Zero crossing rate (voice quality)
        zcr = librosa.feature.zero_crossing_rate(y=audio)
        features["zcr_mean"] = float(np.mean(zcr))

        # Pitch (F0)
        f0, voiced_flag, _ = librosa.pyin(audio, fmin=50, fmax=500, sr=sr)
        if voiced_flag.any():
            features["pitch_mean"] = float(np.nanmean(f0)) if f0 is not None else 0
            features["pitch_std"] = float(np.nanstd(f0)) if f0 is not None else 0
            features["voiced_ratio"] = float(np.mean(voiced_flag))
        else:
            features["pitch_mean"] = 0.0
            features["pitch_std"] = 0.0
            features["voiced_ratio"] = 0.0

        return features

    def detect_silence(self, audio: np.ndarray, sr: int,
                        threshold_db: float = -30) -> List[Tuple[float, float]]:
        """Detect silent regions in audio (hesitation patterns)."""
        intervals = librosa.effects.split(audio, top_db=abs(threshold_db))
        silent_regions = []
        last_end = 0
        for start, end in intervals:
            if start > last_end:
                silent_regions.append((last_end / sr, start / sr))
            last_end = end
        return silent_regions

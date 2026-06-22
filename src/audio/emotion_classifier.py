"""Emotion classification from voice features."""

from typing import Dict, List
import numpy as np
import pickle
from pathlib import Path


class EmotionClassifier:
    """Classify emotions and psychological states from voice features.

    Detects: anxiety, depression, distress, and normal emotional states
    relevant to women's health contexts.
    """

    EMOTIONS = ["neutral", "anxiety", "depression", "distress", "fear"]

    def __init__(self, model_path: str = None):
        self.model_path = model_path
        self._model = None
        self._scaler = None

    def _get_model(self):
        """Load or create classifier model."""
        if self._model is None:
            if self.model_path and Path(self.model_path).exists():
                with open(self.model_path, "rb") as f:
                    data = pickle.load(f)
                    self._model = data["model"]
                    self._scaler = data.get("scaler")
            else:
                from sklearn.ensemble import RandomForestClassifier
                from sklearn.preprocessing import StandardScaler
                self._model = RandomForestClassifier(n_estimators=100, random_state=42)
                self._scaler = StandardScaler()
        return self._model, self._scaler

    def extract_features(self, audio: np.ndarray, sr: int) -> np.ndarray:
        """Extract emotion-relevant features."""
        import librosa

        features = []
        # MFCCs
        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
        features.extend(np.mean(mfcc, axis=1))
        features.extend(np.std(mfcc, axis=1))

        # Pitch
        f0, voiced, _ = librosa.pyin(audio, fmin=50, fmax=500, sr=sr)
        features.append(np.nanmean(f0) if f0 is not None else 0)
        features.append(np.nanstd(f0) if f0 is not None else 0)

        # Energy
        rms = librosa.feature.rms(y=audio)
        features.append(np.mean(rms))
        features.append(np.std(rms))

        # Zero crossing rate
        zcr = librosa.feature.zero_crossing_rate(y=audio)
        features.append(np.mean(zcr))

        # Spectral centroid
        centroid = librosa.feature.spectral_centroid(y=audio, sr=sr)
        features.append(np.mean(centroid))

        return np.array(features)

    def predict(self, features: np.ndarray) -> Dict:
        """Predict emotion from features.

        Uses heuristics when no trained model is available.
        """
        model, _ = self._get_model()

        # When using untrained RandomForest, use heuristics with feature analysis
        if not hasattr(model, "classes_") or model.classes_ is None:
            return self._heuristic_predict(features)

        features = features.reshape(1, -1)
        proba = model.predict_proba(features)[0]
        pred_idx = np.argmax(proba)
        return {
            "emotion": self.EMOTIONS[pred_idx] if pred_idx < len(self.EMOTIONS) else "neutral",
            "confidence": float(proba[pred_idx]),
            "probabilities": {self.EMOTIONS[i]: float(p) for i, p in enumerate(proba)},
        }

    def _heuristic_predict(self, features: np.ndarray) -> Dict:
        """Rule-based emotion prediction from features."""
        pitch_mean = features[26] if len(features) > 26 else 0
        energy_mean = features[28] if len(features) > 28 else 0
        pitch_std = features[27] if len(features) > 27 else 0
        zcr = features[30] if len(features) > 30 else 0

        # Heuristic rules
        if energy_mean < 0.01:
            emotion, conf = "depression", 0.7
        elif pitch_std > 50:
            emotion, conf = "anxiety", 0.7
        elif zcr > 0.1:
            emotion, conf = "distress", 0.65
        elif pitch_mean < 100:
            emotion, conf = "depression", 0.55
        else:
            emotion, conf = "neutral", 0.5

        probs = {e: 0.1 for e in self.EMOTIONS}
        probs[emotion] = conf
        return {"emotion": emotion, "confidence": conf, "probabilities": probs}

    def train(self, X: np.ndarray, y: np.ndarray):
        """Train the classifier with labeled data."""
        from sklearn.preprocessing import StandardScaler

        model, _ = self._get_model()
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        model.fit(X_scaled, y)
        self._scaler = scaler

    def save(self, path: str):
        """Save model to disk."""
        with open(path, "wb") as f:
            pickle.dump({"model": self._model, "scaler": self._scaler}, f)

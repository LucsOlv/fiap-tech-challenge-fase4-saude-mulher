"""Specialized pattern detection for women's health voice analysis."""

from typing import Dict, List
import numpy as np


class PatternDetector:
    """Detect specific voice patterns indicating health conditions.

    Focuses on:
    - Postpartum depression indicators
    - Gestational anxiety markers
    - Domestic violence trauma voice patterns
    - Voice tone alterations in gynecological consultations
    """

    def __init__(self):
        self.thresholds = {
            "monotone_threshold": 10.0,    # Pitch std below this = monotone (depression)
            "tremor_threshold": 0.15,       # High ZCR variation = tremor (anxiety)
            "pause_threshold": 3.0,         # Seconds of pause = hesitation (trauma)
            "low_energy_threshold": 0.01,   # RMS below = low energy (depression)
        }

    def analyze(self, features: Dict, transcription: Dict = None) -> Dict:
        """Analyze voice features for health-relevant patterns.

        Args:
            features: Dict of acoustic features.
            transcription: Optional transcription data with segments.

        Returns:
            Dict with risk scores for each condition.
        """
        results = {
            "postpartum_depression_risk": self._detect_depression(features),
            "gestational_anxiety_risk": self._detect_anxiety(features),
            "trauma_indicators": self._detect_trauma(features, transcription),
            "consultation_discomfort": self._detect_discomfort(features),
            "overall_risk_score": 0.0,
            "alerts": [],
        }

        # Calculate overall risk score
        scores = [
            results["postpartum_depression_risk"]["score"],
            results["gestational_anxiety_risk"]["score"],
            results["trauma_indicators"]["score"],
            results["consultation_discomfort"]["score"],
        ]
        results["overall_risk_score"] = round(sum(scores) / len(scores), 2)

        # Generate alerts for high-risk findings
        for condition, data in results.items():
            if isinstance(data, dict) and data.get("score", 0) > 0.6:
                results["alerts"].append({
                    "condition": condition,
                    "level": "high" if data["score"] > 0.8 else "medium",
                    "message": f"Elevated {condition.replace('_', ' ')} score: {data['score']:.2f}",
                })

        return results

    def _detect_depression(self, features: Dict) -> Dict:
        """Detect postpartum depression indicators."""
        score = 0.0
        indicators = []

        pitch_std = features.get("pitch_std", 0)
        energy_mean = features.get("energy_mean", 0)

        if pitch_std < self.thresholds["monotone_threshold"]:
            score += 0.4
            indicators.append("monotone_speech")
        if energy_mean < self.thresholds["low_energy_threshold"]:
            score += 0.3
            indicators.append("low_vocal_energy")
        if features.get("voiced_ratio", 1) < 0.5:
            score += 0.3
            indicators.append("reduced_voicing")

        return {"score": round(min(score, 1.0), 2), "indicators": indicators}

    def _detect_anxiety(self, features: Dict) -> Dict:
        """Detect gestational anxiety markers."""
        score = 0.0
        indicators = []

        zcr_mean = features.get("zcr_mean", 0)
        pitch_mean = features.get("pitch_mean", 0)
        pitch_std = features.get("pitch_std", 0)

        if zcr_mean > self.thresholds["tremor_threshold"]:
            score += 0.4
            indicators.append("vocal_tremor")
        if pitch_std > 60:
            score += 0.3
            indicators.append("high_pitch_variability")
        if pitch_mean > 300:
            score += 0.3
            indicators.append("elevated_pitch")

        return {"score": round(min(score, 1.0), 2), "indicators": indicators}

    def _detect_trauma(self, features: Dict, transcription: Dict = None) -> Dict:
        """Detect trauma voice patterns (domestic violence indicators)."""
        score = 0.0
        indicators = []

        if transcription:
            pauses = transcription.get("hesitation", {})
            if pauses.get("has_excessive_pauses"):
                score += 0.5
                indicators.append("excessive_pauses")

        pitch_std = features.get("pitch_std", 0)
        if pitch_std > 80:
            score += 0.3
            indicators.append("extreme_pitch_variation")

        return {"score": round(min(score, 1.0), 2), "indicators": indicators}

    def _detect_discomfort(self, features: Dict) -> Dict:
        """Detect signs of discomfort in consultation."""
        score = 0.0
        indicators = []

        energy_std = features.get("energy_std", 0)
        zcr_mean = features.get("zcr_mean", 0)

        if energy_std > 0.05:
            score += 0.35
            indicators.append("unstable_voice_energy")
        if zcr_mean > 0.08:
            score += 0.35
            indicators.append("voice_roughness")

        return {"score": round(min(score, 1.0), 2), "indicators": indicators}

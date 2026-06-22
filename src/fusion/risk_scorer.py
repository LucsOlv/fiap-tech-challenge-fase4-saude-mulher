"""Risk scoring engine for patient health assessment."""

from typing import Dict, List


class RiskScorer:
    """Calculate unified risk scores from multimodal inputs."""

    def __init__(self):
        self.thresholds = {
            "critical": 70,
            "high": 50,
            "medium": 30,
            "low": 0,
        }

    def compute_score(self, video_score: float = 0, audio_score: float = 0,
                      text_score: float = 0, vitals_score: float = 0) -> Dict:
        """Compute weighted composite risk score.

        Args:
            video_score: 0-100 score from video analysis.
            audio_score: 0-100 score from audio analysis.
            text_score: 0-100 score from text analysis.
            vitals_score: 0-100 score from vital signs monitoring.

        Returns:
            Dict with composite score and component breakdown.
        """
        weights = {"video": 0.35, "audio": 0.30, "text": 0.20, "vitals": 0.15}

        composite = (
            video_score * weights["video"]
            + audio_score * weights["audio"]
            + text_score * weights["text"]
            + vitals_score * weights["vitals"]
        )

        risk_level = "low"
        for level in ["critical", "high", "medium", "low"]:
            if composite >= self.thresholds[level]:
                risk_level = level
                break

        return {
            "composite_score": round(composite, 2),
            "risk_level": risk_level,
            "components": {
                "video": round(video_score, 2),
                "audio": round(audio_score, 2),
                "text": round(text_score, 2),
                "vital_signs": round(vitals_score, 2),
            },
            "weights": weights,
        }

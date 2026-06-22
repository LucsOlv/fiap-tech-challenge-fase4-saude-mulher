"""Multimodal fusion engine for unified risk assessment."""

from typing import Dict, List, Optional
from datetime import datetime


class FusionEngine:
    """Central engine that combines video, audio, and text analysis results
    into a unified risk assessment for each patient.

    Architecture:
        Video (YOLOv8) ──┐
        Audio (Whisper) ─┼── FusionEngine ──► Unified Risk Score ──► Alert
        Text (NLP) ──────┘
    """

    MODALITY_WEIGHTS = {
        "video": 0.40,
        "audio": 0.35,
        "text": 0.25,
    }

    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.weights = self.config.get("modality_weights", self.MODALITY_WEIGHTS)

    def fuse(self, video_result: Dict = None, audio_result: Dict = None,
             text_result: Dict = None, patient_id: str = "anonymous") -> Dict:
        """Fuse multimodal analysis results into a unified risk assessment.

        Args:
            video_result: Output from VideoInference.detect_anomaly_in_video().
            audio_result: Output from PatternDetector.analyze().
            text_result: Output from PrescriptionAnalyzer.analyze().
            patient_id: Anonymized patient identifier.

        Returns:
            Unified risk assessment with scores and alerts.
        """
        scores = {}
        alerts = []
        evidence = {}

        # Process each modality
        if video_result:
            v_score, v_alerts = self._process_video(video_result)
            scores["video"] = v_score
            alerts.extend(v_alerts)
            evidence["video"] = video_result

        if audio_result:
            a_score, a_alerts = self._process_audio(audio_result)
            scores["audio"] = a_score
            alerts.extend(a_alerts)
            evidence["audio"] = audio_result

        if text_result:
            t_score, t_alerts = self._process_text(text_result)
            scores["text"] = t_score
            alerts.extend(t_alerts)
            evidence["text"] = text_result

        # Weighted fusion
        unified_score = self._compute_unified_score(scores)

        # Determine risk level
        risk_level = self._determine_risk_level(unified_score)

        # Sort alerts by severity
        alerts = sorted(alerts, key=lambda a: a.get("severity_weight", 0), reverse=True)

        return {
            "patient_id": patient_id,
            "timestamp": datetime.now().isoformat(),
            "unified_risk_score": round(unified_score, 2),
            "risk_level": risk_level,
            "modality_scores": scores,
            "alerts": alerts,
            "evidence_summary": self._summarize_evidence(evidence),
        }

    def _process_video(self, result: Dict) -> tuple:
        """Process video analysis result."""
        score = result.get("score", 0) / 100.0
        alerts = []
        if result.get("level") in ("high", "critical"):
            alerts.append({
                "source": "video",
                "type": "anomalous_bleeding",
                "severity": result["level"],
                "severity_weight": 4 if result["level"] == "critical" else 3,
                "message": f"Video: {result.get('anomalous_frames', 0)} frames with bleeding detected.",
            })
        return score, alerts

    def _process_audio(self, result: Dict) -> tuple:
        """Process audio analysis result."""
        score = result.get("overall_risk_score", 0)
        alerts = []
        for alert in result.get("alerts", []):
            alerts.append({
                "source": "audio",
                "type": alert["condition"],
                "severity": alert["level"],
                "severity_weight": 3 if alert["level"] == "high" else 2,
                "message": alert["message"],
            })
        return score, alerts

    def _process_text(self, result: Dict) -> tuple:
        """Process text analysis result."""
        score = result.get("risk_score", 0)
        alerts = []
        for alert in result.get("alerts", []):
            alerts.append({
                "source": "text",
                "type": alert.get("type", "text_anomaly"),
                "severity": alert.get("severity", "medium"),
                "severity_weight": 3 if alert.get("severity") == "critical" else 2,
                "message": alert["message"],
            })
        return score, alerts

    def _compute_unified_score(self, scores: Dict) -> float:
        """Compute weighted unified risk score."""
        if not scores:
            return 0.0

        weighted_sum = 0.0
        total_weight = 0.0
        for modality, score in scores.items():
            weight = self.weights.get(modality, 0.33)
            weighted_sum += score * weight
            total_weight += weight

        if total_weight == 0:
            return 0.0
        return (weighted_sum / total_weight) * 100  # Scale to 0-100

    def _determine_risk_level(self, score: float) -> str:
        """Determine risk level from unified score."""
        if score >= 70:
            return "critical"
        elif score >= 50:
            return "high"
        elif score >= 30:
            return "medium"
        else:
            return "low"

    def _summarize_evidence(self, evidence: Dict) -> Dict:
        """Create human-readable evidence summary."""
        summary = {}
        for modality, data in evidence.items():
            if modality == "video":
                summary["video"] = f"{data.get('anomalous_frames', 0)} frames anômalos em {data.get('total_frames', 0)} frames analisados"
            elif modality == "audio":
                summary["audio"] = f"Score de risco vocal: {data.get('overall_risk_score', 0)}"
            elif modality == "text":
                summary["text"] = f"Nível de risco: {data.get('risk_level', 'N/A')}"
        return summary

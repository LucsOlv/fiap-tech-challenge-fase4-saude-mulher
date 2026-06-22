"""Integration tests for multimodal fusion pipeline."""

from src.fusion.fusion_engine import FusionEngine
from src.fusion.alert_rules import AlertRules
from src.fusion.risk_scorer import RiskScorer
from src.fusion.realtime_alerts import RealtimeAlertSystem
from src.fusion.vital_signs import VitalSignsMonitor
from src.fusion.anomaly_detector import AnomalyDetector


class TestMultimodalFusion:
    """End-to-end fusion pipeline tests."""

    def test_full_fusion_flow(self):
        """Test complete fusion pipeline with all modalities."""
        # Simulate inputs from each modality
        video_result = {"level": "critical", "score": 85.0,
                        "anomalous_frames": 12, "total_frames": 20}
        audio_result = {"overall_risk_score": 0.65,
                        "postpartum_depression_risk": {"score": 0.8, "indicators": ["monotone"]},
                        "alerts": [{"condition": "depression", "level": "high",
                                    "message": "Depression risk"}]}
        text_result = {"risk_score": 0.45, "risk_level": "medium",
                       "alerts": [{"type": "high_dosage", "severity": "medium",
                                   "message": "High dosage"}]}

        # Fusion Engine
        fe = FusionEngine()
        fusion_result = fe.fuse(video_result=video_result, audio_result=audio_result,
                                text_result=text_result, patient_id="INT-001")
        assert fusion_result["patient_id"] == "INT-001"
        assert fusion_result["unified_risk_score"] > 0
        assert fusion_result["risk_level"] in ("low", "medium", "high", "critical")

        # Alert Rules
        ar = AlertRules()
        context = {"video": video_result, "audio": {"trauma_indicators": {"score": 0.85}}}
        triggered = ar.evaluate(context)
        assert len(triggered) > 0

    def test_vital_signs_and_anomaly_flow(self):
        """Test vital signs monitoring and anomaly detection together."""
        vsm = VitalSignsMonitor()
        ad = AnomalyDetector()

        # Record vitals
        vsm.record("blood_pressure_systolic", 120)
        vsm.record("fetal_heart_rate", 145)

        # Inject normal data for anomaly detector baseline
        for i in range(15):
            ad.add_reading("systolic", 120 + i * 0.3, f"t{i}")

        # Add anomalous reading
        result = ad.add_reading("systolic", 165, "t15")
        assert "z_score" in result

        # Check preeclampsia
        risk = vsm.check_preeclampsia_risk(165, 100, True)
        assert risk["risk_level"] in ("high", "critical")

    def test_realtime_alert_broadcast(self):
        """Test alert system with subscriber pattern."""
        ras = RealtimeAlertSystem()
        received = []

        def handler(alert):
            received.append(alert)

        ras.subscribe(handler)
        ras.create_and_send("PAC-001", "preeclampsia", "critical",
                            "PA: 160/100, proteinúria positiva")

        assert len(received) == 1
        assert received[0]["severity"] == "critical"
        assert "preeclampsia" in received[0]["type"]

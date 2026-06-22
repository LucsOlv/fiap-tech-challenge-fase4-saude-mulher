"""Automatic report generation from video analysis results."""

from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import json


class ReportGenerator:
    """Generate clinical reports from video analysis detections.

    Produces automated reports for four categories:
    1. Obstetric procedure deviations
    2. Surgical complication signs
    3. Psychological discomfort indicators
    4. Domestic violence alerts
    """

    SEVERITY_LEVELS = ["low", "medium", "high", "critical"]

    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_report(self, video_path: str, detections: List[Dict],
                        patient_id: str = "anonymous",
                        exam_type: str = "surgery") -> Dict:
        """Generate a comprehensive report from video detections.

        Args:
            video_path: Path to the analyzed video.
            detections: List of frame-level detection results.
            patient_id: Patient identifier (anonymized).
            exam_type: Type of exam (surgery, consultation, physiotherapy, triage).

        Returns:
            Report dictionary with all findings.
        """
        report = {
            "report_id": f"VID-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "generated_at": datetime.now().isoformat(),
            "patient_id": patient_id,
            "exam_type": exam_type,
            "video_path": str(video_path),
            "summary": self._generate_summary(detections, exam_type),
            "timeline": self._generate_timeline(detections),
            "alerts": self._generate_alerts(detections, exam_type),
            "recommendations": self._generate_recommendations(detections, exam_type),
        }
        return report

    def _generate_summary(self, detections: List[Dict], exam_type: str) -> Dict:
        """Generate summary statistics."""
        total_frames = len(detections)
        frames_with_detections = sum(1 for d in detections if d["detections"])

        class_counts = {}
        for d in detections:
            for det in d["detections"]:
                name = det["class_name"]
                class_counts[name] = class_counts.get(name, 0) + 1

        return {
            "total_frames_processed": total_frames,
            "frames_with_detections": frames_with_detections,
            "detection_rate": round(frames_with_detections / max(total_frames, 1) * 100, 1),
            "class_distribution": class_counts,
            "exam_type": exam_type,
        }

    def _generate_timeline(self, detections: List[Dict]) -> List[Dict]:
        """Generate chronological timeline of significant events."""
        events = []
        for d in detections:
            if d["detections"]:
                for det in d["detections"]:
                    if det["confidence"] > 0.6:
                        events.append({
                            "timestamp": d["timestamp_seconds"],
                            "event": f"Detected {det['class_name']}",
                            "confidence": round(det["confidence"], 3),
                        })
        return sorted(events, key=lambda x: x["timestamp"])

    def _generate_alerts(self, detections: List[Dict], exam_type: str) -> List[Dict]:
        """Generate clinical alerts based on detection patterns."""
        alerts = []
        bleeding_events = []

        for d in detections:
            for det in d["detections"]:
                if det["class_name"] == "anomalous_bleeding":
                    bleeding_events.append({
                        "timestamp": d["timestamp_seconds"],
                        "confidence": det["confidence"],
                    })

        if bleeding_events:
            severity = "critical" if len(bleeding_events) > 10 else "high" if len(bleeding_events) > 5 else "medium"
            alerts.append({
                "type": "anomalous_bleeding",
                "severity": severity,
                "count": len(bleeding_events),
                "message": f"Anomalous bleeding detected in {exam_type} at {len(bleeding_events)} moments.",
                "timestamps": [e["timestamp"] for e in bleeding_events[:5]],
            })

        return alerts

    def _generate_recommendations(self, detections: List[Dict],
                                   exam_type: str) -> List[str]:
        """Generate clinical recommendations."""
        recs = []
        has_bleeding = any(
            any(det["class_name"] == "anomalous_bleeding" for det in d["detections"])
            for d in detections
        )

        if has_bleeding:
            recs.append("IMMEDIATE: Review surgical site for active bleeding.")
            recs.append("Consider coagulation panel and hematocrit check.")
            recs.append("Alert surgical team lead immediately.")

        if exam_type == "surgery" and has_bleeding:
            recs.append("Document bleeding volume and location for surgical record.")

        if not recs:
            recs.append("No immediate concerns detected. Continue standard monitoring.")

        return recs

    def save_report(self, report: Dict, filename: Optional[str] = None) -> str:
        """Save report to JSON file."""
        if filename is None:
            filename = f"{report['report_id']}.json"
        path = self.output_dir / filename
        with open(path, "w") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        return str(path)

    def report_to_html(self, report: Dict) -> str:
        """Convert report to HTML format for dashboard display."""
        html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head><meta charset="UTF-8"><title>Relatório {report['report_id']}</title>
<style>body{{font-family:Arial;margin:20px}}.alert-critical{{color:red;font-weight:bold}}
.alert-high{{color:orange}}.alert-medium{{color:goldenrod}}.alert-low{{color:green}}
</style></head>
<body>
<h1>Relatório de Análise de Vídeo</h1>
<p><strong>ID:</strong> {report['report_id']} | <strong>Data:</strong> {report['generated_at']}</p>
<p><strong>Paciente:</strong> {report['patient_id']} | <strong>Exame:</strong> {report['exam_type']}</p>
<h2>Sumário</h2>
<p>Frames processados: {report['summary']['total_frames_processed']} |
Detecções: {report['summary']['frames_with_detections']} |
Taxa: {report['summary']['detection_rate']}%</p>
<h2>Alertas</h2>"""
        for alert in report["alerts"]:
            html += f'<p class="alert-{alert["severity"]}">[{alert["severity"].upper()}] {alert["message"]}</p>'
        html += "<h2>Recomendações</h2><ul>"
        for rec in report["recommendations"]:
            html += f"<li>{rec}</li>"
        html += "</ul></body></html>"
        return html

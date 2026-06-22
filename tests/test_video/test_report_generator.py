"""Tests for report generator module."""

from src.video.report_generator import ReportGenerator


class TestReportGenerator:
    """Test ReportGenerator class."""

    def test_generate_report_empty(self):
        rg = ReportGenerator()
        report = rg.generate_report("test.mp4", [], exam_type="surgery")
        assert report["report_id"].startswith("VID-")
        assert report["exam_type"] == "surgery"
        assert report["summary"]["total_frames_processed"] == 0

    def test_generate_report_with_detections(self, sample_detections):
        rg = ReportGenerator()
        report = rg.generate_report("test.mp4", sample_detections, exam_type="surgery")
        assert report["summary"]["total_frames_processed"] == 2
        assert report["summary"]["frames_with_detections"] == 2
        assert len(report["alerts"]) > 0

    def test_report_to_html(self, sample_detections):
        rg = ReportGenerator()
        report = rg.generate_report("test.mp4", sample_detections)
        html = rg.report_to_html(report)
        assert "<html" in html
        assert "Relatório" in html
        assert "bleeding" in html.lower()

    def test_save_report(self, sample_detections):
        import tempfile
        from pathlib import Path

        rg = ReportGenerator(output_dir=tempfile.mkdtemp())
        report = rg.generate_report("test.mp4", sample_detections)
        path = rg.save_report(report)
        assert Path(path).exists()
        Path(path).unlink()

    def test_summary_class_distribution(self, sample_detections):
        rg = ReportGenerator()
        report = rg.generate_report("test.mp4", sample_detections)
        dist = report["summary"]["class_distribution"]
        assert "normal_tissue" in dist
        assert "anomalous_bleeding" in dist

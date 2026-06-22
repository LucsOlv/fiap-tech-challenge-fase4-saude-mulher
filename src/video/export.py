"""Export YOLOv8 model to various formats for deployment."""

from pathlib import Path
from typing import Optional


def export_to_onnx(model_path: str, output_path: Optional[str] = None,
                   imgsz: int = 640, opset: int = 12) -> str:
    """Export YOLOv8 model to ONNX format for Azure compatibility.

    Args:
        model_path: Path to .pt model file.
        output_path: Output path for ONNX file.
        imgsz: Image size for export.
        opset: ONNX opset version.

    Returns:
        Path to exported ONNX model.
    """
    from ultralytics import YOLO

    model = YOLO(model_path)
    if output_path is None:
        output_path = str(Path(model_path).with_suffix(".onnx"))

    model.export(format="onnx", imgsz=imgsz, opset=opset)
    return output_path


def export_to_torchscript(model_path: str,
                           output_path: Optional[str] = None) -> str:
    """Export to TorchScript format."""
    from ultralytics import YOLO

    model = YOLO(model_path)
    if output_path is None:
        output_path = str(Path(model_path).with_suffix(".torchscript"))

    model.export(format="torchscript")
    return output_path


def get_model_info(model_path: str) -> dict:
    """Get model metadata and architecture info."""
    from ultralytics import YOLO

    model = YOLO(model_path)
    return {
        "model_path": model_path,
        "task": model.task,
        "model_name": model.model_name,
        "parameters": sum(p.numel() for p in model.model.parameters()),
        "classes": model.names,
    }

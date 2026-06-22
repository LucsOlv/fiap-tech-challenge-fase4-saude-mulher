"""YOLOv8 training script for anomalous bleeding detection."""

import os
from pathlib import Path
from typing import Optional
import yaml


def create_dataset_config(data_dir: str = "data/processed",
                          output_path: str = "src/video/config/dataset.yaml") -> str:
    """Create YOLOv8 dataset configuration YAML file.

    Args:
        data_dir: Root directory containing train/val/test subdirectories.
        output_path: Path to save the YAML config.

    Returns:
        Path to the created config file.
    """
    config = {
        "path": str(Path(data_dir).absolute()),
        "train": "train/images",
        "val": "val/images",
        "test": "test/images",
        "nc": 3,  # number of classes
        "names": {
            0: "normal_tissue",
            1: "anomalous_bleeding",
            2: "surgical_instrument"
        }
    }

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    with open(output, "w") as f:
        yaml.dump(config, f, default_flow_style=False)

    return str(output)


def train_yolo(data_config: str, model_name: str = "yolov8n.pt",
               epochs: int = 100, imgsz: int = 640, batch: int = 16,
               device: Optional[str] = None, project: str = "models",
               name: str = "yolov8_saude_mulher") -> str:
    """Train YOLOv8 model for anomalous bleeding detection.

    Args:
        data_config: Path to dataset YAML config.
        model_name: Pretrained model to start from.
        epochs: Number of training epochs.
        imgsz: Image size for training.
        batch: Batch size.
        device: Device to train on (cuda/cpu).
        project: Output project directory.
        name: Experiment name.

    Returns:
        Path to the trained model weights.
    """
    try:
        from ultralytics import YOLO

        model = YOLO(model_name)
        results = model.train(
            data=data_config,
            epochs=epochs,
            imgsz=imgsz,
            batch=batch,
            device=device or ("cuda" if os.environ.get("CUDA_VISIBLE_DEVICES") else "cpu"),
            project=project,
            name=name,
            patience=20,
            save=True,
            save_period=10,
            val=True,
            plots=True,
        )

        best_model = Path(project) / name / "weights" / "best.pt"
        return str(best_model)

    except ImportError:
        raise ImportError("ultralytics not installed. Run: pip install ultralytics")


def validate_model(model_path: str, data_config: str) -> dict:
    """Validate trained model and return metrics."""
    from ultralytics import YOLO

    model = YOLO(model_path)
    metrics = model.val(data=data_config)
    return {
        "mAP50": float(metrics.box.map50),
        "mAP50-95": float(metrics.box.map),
        "precision": float(metrics.box.mp),
        "recall": float(metrics.box.mr),
    }

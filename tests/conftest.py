"""Shared test fixtures for all test modules."""

import pytest
import numpy as np
import tempfile
from pathlib import Path


@pytest.fixture
def sample_frame():
    """Create a sample RGB frame (640x640) for testing."""
    return np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)


@pytest.fixture
def sample_video_path():
    """Create a temporary test video file."""
    import cv2

    tmp = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(tmp.name, fourcc, 30.0, (640, 480))

    for _ in range(30):
        frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        writer.write(frame)
    writer.release()

    yield tmp.name
    Path(tmp.name).unlink(missing_ok=True)


@pytest.fixture
def sample_audio():
    """Create a sample audio array."""
    sr = 16000
    duration = 3  # seconds
    t = np.linspace(0, duration, sr * duration)
    audio = 0.5 * np.sin(2 * np.pi * 440 * t)  # 440 Hz tone
    return audio.astype(np.float32), sr


@pytest.fixture
def sample_audio_path(sample_audio):
    """Create a temporary test audio file."""
    import soundfile as sf

    audio, sr = sample_audio
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    sf.write(tmp.name, audio, sr)
    yield tmp.name
    Path(tmp.name).unlink(missing_ok=True)


@pytest.fixture
def sample_medical_text():
    """Sample medical text in Portuguese."""
    return (
        "Paciente gestante, 32 semanas, apresenta pressão arterial de 150/95 mmHg. "
        "Relata cefaleia e dor abdominal. Prescrito metildopa 500mg via oral. "
        "Batimentos fetais: 145 bpm. Exame de proteinúria positivo. "
        "Diagnóstico: pré-eclâmpsia moderada. Internação recomendada."
    )


@pytest.fixture
def sample_prescription_text():
    """Sample prescription text."""
    return (
        "Prescrição: metildopa 500mg VO 8/8h. Nifedipina 10mg VO se PA > 160/100. "
        "Sulfato de magnésio 4g IV dose de ataque. Ocitocina 5UI IM após parto."
    )


@pytest.fixture
def sample_detections():
    """Sample video detection results."""
    return [
        {
            "frame_idx": 0,
            "timestamp_seconds": 0.0,
            "detections": [
                {"class_id": 0, "class_name": "normal_tissue", "confidence": 0.95, "bbox": [100, 100, 200, 200]},
            ],
        },
        {
            "frame_idx": 10,
            "timestamp_seconds": 1.0,
            "detections": [
                {"class_id": 1, "class_name": "anomalous_bleeding", "confidence": 0.85, "bbox": [150, 200, 300, 350]},
            ],
        },
    ]


@pytest.fixture
def sample_vital_signs():
    """Sample vital signs readings."""
    return [
        {"systolic": 120, "diastolic": 80, "fetal_hr": 145, "maternal_hr": 78, "temperature": 36.5},
        {"systolic": 125, "diastolic": 82, "fetal_hr": 148, "maternal_hr": 80, "temperature": 36.7},
        {"systolic": 130, "diastolic": 85, "fetal_hr": 150, "maternal_hr": 82, "temperature": 36.6},
        {"systolic": 155, "diastolic": 98, "fetal_hr": 155, "maternal_hr": 95, "temperature": 37.0},
        {"systolic": 158, "diastolic": 100, "fetal_hr": 160, "maternal_hr": 98, "temperature": 37.2},
    ]

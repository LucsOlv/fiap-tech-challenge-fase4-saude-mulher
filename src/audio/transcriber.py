"""Speech-to-text transcription for clinical consultations."""

from pathlib import Path
from typing import Optional, Dict
import numpy as np


class AudioTranscriber:
    """Transcribe clinical audio recordings using Whisper or Azure Speech."""

    def __init__(self, model_name: str = "tiny", language: str = "pt",
                 use_azure: bool = False):
        self.model_name = model_name
        self.language = language
        self.use_azure = use_azure
        self._model = None

    def _load_whisper(self):
        """Lazy-load Whisper model."""
        if self._model is None and not self.use_azure:
            try:
                import whisper
                self._model = whisper.load_model(self.model_name)
            except ImportError:
                raise ImportError("openai-whisper not installed")
        return self._model

    def transcribe(self, audio_path: str) -> Dict:
        """Transcribe audio file to text with timestamps."""
        model = self._load_whisper()
        result = model.transcribe(
            audio_path,
            language=self.language,
            task="transcribe",
            verbose=False,
        )
        return {
            "text": result["text"],
            "language": result.get("language", self.language),
            "segments": [
                {
                    "start": seg["start"],
                    "end": seg["end"],
                    "text": seg["text"].strip(),
                }
                for seg in result["segments"]
            ],
            "duration_seconds": result["segments"][-1]["end"] if result["segments"] else 0,
        }

    def transcribe_array(self, audio: np.ndarray, sr: int) -> Dict:
        """Transcribe from numpy array."""
        import tempfile
        import soundfile as sf

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            sf.write(tmp.name, audio, sr)
            result = self.transcribe(tmp.name)
        Path(tmp.name).unlink(missing_ok=True)
        return result

    def detect_hesitation(self, segments: list) -> Dict:
        """Detect hesitation patterns from transcription segments."""
        if not segments:
            return {"hesitation_count": 0, "avg_pause_duration": 0, "has_excessive_pauses": False}

        pauses = []
        for i in range(1, len(segments)):
            pause = segments[i]["start"] - segments[i - 1]["end"]
            if pause > 0:
                pauses.append(pause)

        avg_pause = sum(pauses) / len(pauses) if pauses else 0
        return {
            "hesitation_count": len(pauses),
            "avg_pause_duration": round(avg_pause, 3),
            "total_pause_duration": round(sum(pauses), 3),
            "has_excessive_pauses": avg_pause > 2.0,
        }

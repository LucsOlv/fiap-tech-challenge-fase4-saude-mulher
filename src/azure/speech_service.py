"""Azure Speech Services wrapper for STT and sentiment analysis."""

from typing import Dict, Optional
from pathlib import Path


class AzureSpeechService:
    """Wrapper for Azure Cognitive Services Speech."""

    def __init__(self, config: dict = None):
        import os
        self.config = config or {
            "key": os.getenv("AZURE_SPEECH_KEY", ""),
            "region": os.getenv("AZURE_SPEECH_REGION", "brazilsouth"),
        }
        self._client = None

    def speech_to_text(self, audio_path: str, language: str = "pt-BR") -> Dict:
        """Convert speech to text using Azure Speech Services.

        Falls back to local whisper if Azure is not configured.
        """
        if not self.config.get("key"):
            return self._fallback_stt(audio_path, language)

        try:
            import azure.cognitiveservices.speech as speechsdk

            speech_config = speechsdk.SpeechConfig(
                subscription=self.config["key"],
                region=self.config["region"],
            )
            speech_config.speech_recognition_language = language

            audio_config = speechsdk.audio.AudioConfig(filename=audio_path)
            recognizer = speechsdk.SpeechRecognizer(
                speech_config=speech_config, audio_config=audio_config
            )

            result = recognizer.recognize_once()

            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                return {"text": result.text, "confidence": 0.95,
                        "service": "azure", "language": language}
            else:
                return {"text": "", "error": str(result.reason),
                        "service": "azure", "language": language}
        except ImportError:
            return self._fallback_stt(audio_path, language)
        except Exception as e:
            return {"error": str(e), "service": "azure"}

    def _fallback_stt(self, audio_path: str, language: str) -> Dict:
        """Fallback to local Whisper when Azure is not available."""
        try:
            import whisper
            model = whisper.load_model("tiny")
            result = model.transcribe(audio_path, language=language[:2],
                                       task="transcribe", verbose=False)
            return {"text": result["text"], "service": "whisper_local",
                    "language": language}
        except ImportError:
            return {"error": "No speech service available", "text": ""}

"""Azure Computer Vision wrapper."""

from typing import Dict, Optional
import os


class AzureVisionService:
    """Wrapper for Azure AI Vision / Computer Vision."""

    def __init__(self, config: dict = None):
        self.config = config or {
            "key": os.getenv("AZURE_VISION_KEY", ""),
            "endpoint": os.getenv("AZURE_VISION_ENDPOINT", ""),
        }

    def analyze_image(self, image_path: str) -> Dict:
        """Analyze medical image using Azure Vision."""
        if not self.config.get("key"):
            return {"service": "local_fallback",
                    "message": "Azure Vision not configured"}

        # Azure Vision API call would go here
        return {"service": "azure_vision", "status": "configured"}

"""Azure services configuration."""

import os
from typing import Optional


class AzureConfig:
    """Centralized Azure configuration from environment variables."""

    def __init__(self):
        self.speech_key = os.getenv("AZURE_SPEECH_KEY", "")
        self.speech_region = os.getenv("AZURE_SPEECH_REGION", "brazilsouth")
        self.vision_key = os.getenv("AZURE_VISION_KEY", "")
        self.vision_endpoint = os.getenv("AZURE_VISION_ENDPOINT", "")
        self.openai_key = os.getenv("AZURE_OPENAI_KEY", "")
        self.openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")
        self.openai_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4")
        self.storage_connection = os.getenv("AZURE_STORAGE_CONNECTION_STRING", "")
        self.storage_container = os.getenv("AZURE_STORAGE_CONTAINER", "saude-mulher-data")
        self.key_vault_url = os.getenv("AZURE_KEY_VAULT_URL", "")

    def is_configured(self) -> bool:
        """Check if minimum Azure configuration is present."""
        return bool(self.speech_key or self.vision_key or self.openai_key)

    def get_speech_config(self) -> dict:
        """Get Azure Speech Services configuration."""
        return {"key": self.speech_key, "region": self.speech_region}

    def get_vision_config(self) -> dict:
        """Get Azure Computer Vision configuration."""
        return {"key": self.vision_key, "endpoint": self.vision_endpoint}

    def get_openai_config(self) -> dict:
        """Get Azure OpenAI configuration."""
        return {
            "api_key": self.openai_key,
            "endpoint": self.openai_endpoint,
            "deployment": self.openai_deployment,
        }

"""Azure OpenAI Service wrapper for clinical text analysis."""

from typing import Dict, List, Optional
import os


class AzureOpenAIService:
    """Wrapper for Azure OpenAI for clinical text summarization and insights."""

    def __init__(self, config: dict = None):
        self.config = config or {
            "api_key": os.getenv("AZURE_OPENAI_KEY", ""),
            "endpoint": os.getenv("AZURE_OPENAI_ENDPOINT", ""),
            "deployment": os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4"),
        }

    def summarize_report(self, report_text: str,
                          max_tokens: int = 300) -> Dict:
        """Generate clinical summary using Azure OpenAI."""
        if not self.config.get("api_key"):
            return self._fallback_summary(report_text)

        # Azure OpenAI API call would go here
        return {"summary": "Azure OpenAI integration pending.",
                "service": "azure_openai"}

    def _fallback_summary(self, text: str) -> Dict:
        """Simple extractive summary as fallback."""
        sentences = [s.strip() for s in text.replace("!", ".").replace("?", ".").split(".") if s.strip()]
        summary = " ".join(sentences[:3]) if len(sentences) > 3 else text
        return {"summary": summary, "service": "local_extractive",
                "original_length": len(text), "summary_length": len(summary)}

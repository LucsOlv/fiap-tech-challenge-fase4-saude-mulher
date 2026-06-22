"""Sentiment analysis on transcribed clinical consultation text."""

from typing import Dict, List
import re


class SentimentAnalyzer:
    """Analyze sentiment in transcribed consultation text.

    Focuses on women's health context: detecting emotional distress,
    fear indicators, and positive/negative sentiment in patient discourse.
    """

    # Portuguese sentiment keywords for women's health context
    NEGATIVE_KEYWORDS = [
        "dor", "medo", "triste", "ansiosa", "preocupada", "não aguento",
        "sofrendo", "desespero", "angustiada", "choro", "sozinha",
        "violência", "abuso", "agressão", "apanhei", "ameaça",
        "sangramento", "hemorragia", "complicação", "perda",
    ]

    FEAR_KEYWORDS = [
        "medo", "pavor", "aterrorizada", "apavorada", "terror",
        "assustada", "insegura", "receio",
    ]

    POSITIVE_KEYWORDS = [
        "bem", "tranquila", "feliz", "grata", "aliviada", "segura",
        "confiante", "melhor", "ótima", "maravilhosa",
    ]

    def analyze(self, text: str) -> Dict:
        """Analyze sentiment of transcribed text.

        Returns:
            Dict with sentiment scores, emotions detected, and key phrases.
        """
        text_lower = text.lower()

        neg_count = sum(1 for kw in self.NEGATIVE_KEYWORDS if kw in text_lower)
        fear_count = sum(1 for kw in self.FEAR_KEYWORDS if kw in text_lower)
        pos_count = sum(1 for kw in self.POSITIVE_KEYWORDS if kw in text_lower)

        total = neg_count + pos_count + 1  # avoid division by zero
        sentiment_score = (pos_count - neg_count) / total
        sentiment_score = round(max(-1.0, min(1.0, sentiment_score)), 3)

        # Detect specific emotions
        emotions = []
        if fear_count > 0:
            emotions.append({"emotion": "fear", "intensity": min(fear_count / 3, 1.0)})
        if neg_count > 2:
            emotions.append({"emotion": "distress", "intensity": min(neg_count / 5, 1.0)})
        if pos_count > neg_count + 2:
            emotions.append({"emotion": "positive_outlook", "intensity": 0.7})

        # Risk indicators
        risk_signals = []
        violence_words = ["violência", "abuso", "agressão", "apanhei", "ameaça"]
        if any(w in text_lower for w in violence_words):
            risk_signals.append("possible_domestic_violence_disclosure")

        bleeding_words = ["sangramento", "hemorragia"]
        if any(w in text_lower for w in bleeding_words):
            risk_signals.append("bleeding_reported")

        return {
            "sentiment_score": sentiment_score,
            "sentiment_label": "positive" if sentiment_score > 0.1 else "negative" if sentiment_score < -0.1 else "neutral",
            "emotions_detected": emotions,
            "risk_signals": risk_signals,
            "negative_word_count": neg_count,
            "fear_word_count": fear_count,
            "positive_word_count": pos_count,
        }

    def analyze_segments(self, segments: List[Dict]) -> List[Dict]:
        """Analyze sentiment per transcription segment."""
        return [
            {
                "start": seg["start"],
                "end": seg["end"],
                "text": seg["text"],
                "sentiment": self.analyze(seg["text"]),
            }
            for seg in segments
        ]

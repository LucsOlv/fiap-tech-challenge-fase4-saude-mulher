"""Tests for sentiment analyzer module."""

from src.audio.sentiment import SentimentAnalyzer


class TestSentimentAnalyzer:
    """Test SentimentAnalyzer class."""

    def test_negative_sentiment(self):
        sa = SentimentAnalyzer()
        text = "Estou com muita dor, medo, triste e ansiosa. Não aguento mais."
        result = sa.analyze(text)
        assert result["sentiment_label"] == "negative"
        assert result["sentiment_score"] < 0

    def test_positive_sentiment(self):
        sa = SentimentAnalyzer()
        text = "Estou bem, tranquila e feliz. Me sinto ótima e confiante."
        result = sa.analyze(text)
        assert result["sentiment_label"] == "positive"

    def test_fear_detection(self):
        sa = SentimentAnalyzer()
        text = "Tenho muito medo e estou aterrorizada com essa situação."
        result = sa.analyze(text)
        assert result["fear_word_count"] > 0
        assert len(result["emotions_detected"]) > 0

    def test_violence_disclosure(self):
        sa = SentimentAnalyzer()
        text = "Sofri violência e abuso. Meu marido me agrediu e me ameaçou."
        result = sa.analyze(text)
        assert "possible_domestic_violence_disclosure" in result["risk_signals"]

    def test_bleeding_report(self):
        sa = SentimentAnalyzer()
        text = "Estou com sangramento desde ontem, acho que é hemorragia."
        result = sa.analyze(text)
        assert "bleeding_reported" in result["risk_signals"]

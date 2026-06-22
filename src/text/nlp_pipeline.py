"""NLP pipeline for medical text analysis in women's health."""

from typing import Dict, List, Optional


class NLPPipeline:
    """Complete NLP pipeline for processing medical reports and clinical text."""

    def __init__(self, language: str = "pt"):
        self.language = language
        self._nlp = None

    def _get_nlp(self):
        """Lazy-load spaCy model."""
        if self._nlp is None:
            try:
                import spacy
                model_name = "pt_core_news_sm" if self.language == "pt" else "en_core_web_sm"
                try:
                    self._nlp = spacy.load(model_name)
                except OSError:
                    # Fallback: use blank model
                    self._nlp = spacy.blank(self.language)
            except ImportError:
                # Minimal fallback without spaCy
                self._nlp = None
        return self._nlp

    def process(self, text: str) -> Dict:
        """Process clinical text and extract structured information.

        Returns:
            Dict with tokens, entities, sentences, and risk indicators.
        """
        nlp = self._get_nlp()

        if nlp is not None:
            doc = nlp(text)
            tokens = [{"text": t.text, "pos": t.pos_, "lemma": t.lemma_} for t in doc]
            entities = [{"text": e.text, "label": e.label_} for e in doc.ents]
            sentences = [s.text for s in doc.sents]
        else:
            # Basic fallback processing
            tokens = [{"text": w, "pos": "UNK", "lemma": w} for w in text.split()]
            entities = []
            sentences = [s.strip() for s in text.replace("!", ".").replace("?", ".").split(".") if s.strip()]

        # Rule-based clinical entity extraction
        clinical_entities = self._extract_clinical_entities(text)

        return {
            "text": text,
            "tokens": tokens,
            "entities": entities,
            "clinical_entities": clinical_entities,
            "sentences": sentences,
            "sentence_count": len(sentences),
            "word_count": len(text.split()),
        }

    def _extract_clinical_entities(self, text: str) -> Dict:
        """Rule-based extraction of clinical entities."""
        import re

        entities = {
            "medications": [],
            "dosages": [],
            "conditions": [],
            "procedures": [],
            "vital_signs": [],
        }

        # Medications
        med_patterns = [
            r"\b(\w+(ina|ol|am|ida|ona|zol)\w*)\b",
            r"\b(\w+(pril|sartan|statin|pam|lam)\w*)\b",
        ]
        for pattern in med_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities["medications"].extend([m[0] if isinstance(m, tuple) else m for m in matches])

        # Dosages
        dosage_pattern = r"\d+\s*(mg|mcg|g|ml|UI|mEq)"
        entities["dosages"] = re.findall(dosage_pattern, text, re.IGNORECASE)

        # Conditions
        conditions = [
            "pré-eclâmpsia", "eclâmpsia", "diabetes gestacional",
            "depressão pós-parto", "endometriose", "mioma",
            "câncer de mama", "câncer de colo de útero", "SOP",
            "hipertensão", "hemorragia", "infecção",
        ]
        entities["conditions"] = [c for c in conditions if c.lower() in text.lower()]

        # Vital signs
        vital_pattern = r"(pressão|PA|batimento|FC|temperatura|SatO2|glicemia)\s*[:=]?\s*\d+[\.,]?\d*"
        entities["vital_signs"] = re.findall(vital_pattern, text, re.IGNORECASE)

        return entities

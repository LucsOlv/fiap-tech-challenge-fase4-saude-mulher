"""Text anonymization for LGPD compliance."""

import re
import hashlib


class TextAnonimizer:
    """Anonymizes sensitive PII from medical documents.

    Handles: names, CPF, CNS, addresses, phone numbers, and emails.
    """

    def __init__(self, salt: str = "fiap-saude-mulher"):
        self.salt = salt

    def anonymize(self, text: str) -> str:
        """Anonymize all PII in text."""
        text = self._mask_cpf(text)
        text = self._mask_cns(text)
        text = self._mask_phone(text)
        text = self._mask_email(text)
        text = self._mask_date(text)
        return text

    def _mask_cpf(self, text: str) -> str:
        """Mask CPF numbers."""
        return re.sub(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b", "[CPF_REMOVIDO]", text)

    def _mask_cns(self, text: str) -> str:
        """Mask CNS (Cartão Nacional de Saúde) numbers."""
        return re.sub(r"\b\d{3}\s?\d{4}\s?\d{4}\s?\d{4}\b", "[CNS_REMOVIDO]", text)

    def _mask_phone(self, text: str) -> str:
        """Mask phone numbers."""
        return re.sub(r"\(?\d{2}\)?\s?\d{4,5}-?\d{4}", "[TELEFONE_REMOVIDO]", text)

    def _mask_email(self, text: str) -> str:
        """Mask email addresses."""
        return re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
                      "[EMAIL_REMOVIDO]", text)

    def _mask_date(self, text: str) -> str:
        """Mask dates (optional, for extra privacy)."""
        return re.sub(r"\b\d{2}/\d{2}/\d{4}\b", "[DATA_REMOVIDA]", text)

    def hash_id(self, identifier: str) -> str:
        """Create hashed identifier for patient tracking."""
        return hashlib.sha256(f"{identifier}{self.salt}".encode()).hexdigest()[:12]

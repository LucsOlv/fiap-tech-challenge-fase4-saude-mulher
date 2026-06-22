"""PII anonymization for LGPD compliance."""

import re
import hashlib


class DataAnonimizer:
    """Anonymize personally identifiable information from medical data."""

    def __init__(self, salt: str = "fiap-saude-mulher-v1"):
        self.salt = salt

    def anonymize_text(self, text: str) -> str:
        """Anonymize all PII in clinical text."""
        patterns = [
            (r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b", "[CPF]"),        # CPF
            (r"\b\d{3}\s?\d{4}\s?\d{4}\s?\d{4}\b", "[CNS]"),       # CNS
            (r"\(?\d{2}\)?\s?\d{4,5}-?\d{4}", "[TEL]"),               # Phone
            (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL]"),  # Email
            (r"CEP\s*[:=]?\s*\d{5}-?\d{3}", "[ENDERECO]"),              # CEP
        ]

        for pattern, replacement in patterns:
            text = re.sub(pattern, replacement, text)

        # Replace patient names (heuristic: capitalized words after "Paciente:")
        text = re.sub(r"(?<=Paciente:)\s*[A-Z][a-z]+\s+[A-Z][a-z]+", " [NOME]", text)

        return text

    def anonymize_dict(self, data: dict) -> dict:
        """Recursively anonymize dict values."""
        if isinstance(data, dict):
            return {k: self.anonymize_dict(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.anonymize_dict(v) for v in data]
        elif isinstance(data, str):
            return self.anonymize_text(data)
        return data

    def create_patient_hash(self, patient_id: str, extra_salt: str = "") -> str:
        """Create irreversible hash for patient identification."""
        combined = f"{patient_id}{self.salt}{extra_salt}"
        return hashlib.blake2b(combined.encode(), digest_size=16).hexdigest()

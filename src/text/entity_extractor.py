"""Clinical entity extraction from medical documents."""

from typing import Dict, List
import re


class EntityExtractor:
    """Extract clinical entities from medical text with regex and rules."""

    def __init__(self):
        self.patterns = {
            "cns": r"\b\d{3}\s?\d{4}\s?\d{4}\s?\d{4}\b",
            "cpf": r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b",
            "date": r"\b\d{2}/\d{2}/\d{4}\b",
            "weight": r"(\d+[\.,]?\d*)\s*(kg|quilos?)",
            "height": r"(\d+[\.,]?\d*)\s*(cm|m)\b",
            "pregnancy_week": r"(\d+)[ªa]?\s*semana",
            "blood_pressure": r"(\d{2,3})\s*/\s*(\d{2,3})\s*(mmHg|mmhg)?",
            "heart_rate": r"FC\s*[:=]?\s*(\d+)\s*bpm",
            "temperature": r"(\d+[\.,]?\d*)\s*[°º]\s*C",
        }

    def extract(self, text: str) -> Dict:
        """Extract all entities from medical text."""
        results = {}
        for entity_type, pattern in self.patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                results[entity_type] = matches if entity_type == "blood_pressure" else matches
        return results

    def extract_medications(self, text: str) -> List[str]:
        """Extract common OB/GYN medications."""
        meds = [
            "metformina", "insulina", "metildopa", "nifedipina",
            "hidralazina", "sulfato de magnésio", "misoprostol",
            "ocitocina", "progesterona", "estradiol", "levotiroxina",
            "sertralina", "fluoxetina", "ácido fólico", "sulfato ferroso",
        ]
        found = []
        text_lower = text.lower()
        for med in meds:
            if med in text_lower:
                found.append(med)
        return found

    def extract_diagnoses(self, text: str) -> List[Dict]:
        """Extract ICD-like diagnoses and conditions."""
        diagnoses = []
        conditions_map = {
            "preeclampsia": ["pré-eclâmpsia", "preeclampsia", "pré eclâmpsia"],
            "eclampsia": ["eclâmpsia", "eclampsia"],
            "diabetes_gestacional": ["diabetes gestacional", "DMG"],
            "dpp": ["depressão pós-parto", "depressão pós parto", "DPP"],
            "hemorragia_pos_parto": ["hemorragia pós-parto", "HPP"],
            "endometriose": ["endometriose"],
            "miomatose": ["mioma", "miomatose"],
            "cancer_mama": ["câncer de mama", "CA de mama"],
            "cancer_colo_utero": ["câncer de colo", "colo de útero"],
        }

        text_lower = text.lower()
        for condition, keywords in conditions_map.items():
            for kw in keywords:
                if kw in text_lower:
                    diagnoses.append({"condition": condition, "matched_term": kw})
                    break
        return diagnoses

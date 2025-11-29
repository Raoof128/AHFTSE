from typing import Any, Dict

from backend.core.logger import logger

from .citation_validator import CitationValidator
from .detector import HallucinationDetector


class TrustScoreEngine:
    """
    Aggregates signals from various detectors to compute a final Trust Score.
    """

    def __init__(self) -> None:
        self.detector = HallucinationDetector()
        self.validator = CitationValidator()
        logger.info("TrustScoreEngine initialized.")

    def calculate_trust_score(self, text: str, context: str = "") -> Dict[str, Any]:
        """
        Aggregates various signals to compute a final Trust Score (0-100).
        """
        logger.info("Calculating trust score...")

        # 1. Hallucination Check
        hallucination_result = self.detector.compute_hallucination_score(text, context)
        hallucination_prob = hallucination_result["hallucination_probability"]

        # 2. Citation/Grounding Check
        citation_result = self.validator.validate_citations(text)
        citation_score = citation_result["citation_score"]

        # 3. Compute Weighted Score
        base_score = 100
        # Increased penalty multiplier for stricter evaluation
        penalty = hallucination_prob * 1.5

        # Citation score helps, but can't fix a high hallucination prob completely
        grounding_bonus = (citation_score / 100) * 20

        final_score = base_score - penalty + grounding_bonus
        final_score = max(0, min(100, final_score))  # Clamp 0-100

        # Determine Category
        category = "Unsafe"
        if final_score > 70:
            category = "Strong"
        elif final_score > 30:
            category = "Caution"

        logger.info("Trust Score: %d (%s)", final_score, category)

        return {
            "trust_score": int(final_score),
            "risk_category": category,
            "breakdown": {
                "hallucination_penalty": -int(penalty),
                "grounding_bonus": int(grounding_bonus),
                "base_score": 100,
            },
            "details": {
                "hallucination": hallucination_result,
                "citations": citation_result,
            },
        }

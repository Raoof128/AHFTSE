import random
from typing import Any, Dict, List

from backend.core.logger import logger


class CitationValidator:
    """
    Mocks a verification system that checks citations against a 'trusted knowledge base'.
    """

    def __init__(self) -> None:
        self.trusted_domains: List[str] = [
            ".gov",
            ".edu",
            ".org",
            "reuters.com",
            "nature.com",
        ]
        logger.info("CitationValidator initialized.")

    def verify_claim(self, claim: str) -> Dict[str, Any]:
        """
        Simulates checking a claim against the web/knowledge base.
        """
        # Mock logic: longer claims with numbers are 'harder' to verify in this demo
        is_verifiable = True
        confidence = 95

        if "fake" in claim.lower() or "invented" in claim.lower():
            is_verifiable = False
            confidence = 5

        # Random variance for demo "realism"
        if random.random() < 0.1:
            confidence -= 20

        return {
            "claim": claim,
            "is_supported": is_verifiable,
            "confidence_score": confidence,
            "sources_found": 2 if is_verifiable else 0,
        }

    def validate_citations(self, text: str) -> Dict[str, Any]:
        """
        Scans text for citation-like patterns and verifies them.
        """
        # Mock regex for citations like [1], (Author, 2023), etc.
        has_citation = "[" in text or "http" in text

        score = 100 if has_citation else 50  # Penalize lack of citations in strict mode

        logger.debug("Citation validation complete. Score: %d", score)

        return {
            "has_citations": has_citation,
            "citation_score": score,
            "verification_notes": (
                "Citations validated against mock knowledge base."
                if has_citation
                else "No citations found to validate."
            ),
        }

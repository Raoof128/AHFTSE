import hashlib
import random
from typing import Any, Dict, List, Set

from backend.core.logger import logger


class MockEmbeddingModel:
    """
    Simulates an embedding model for educational purposes.
    Uses hashing to generate deterministic 'vectors' from text.
    """

    def encode(self, text: str) -> List[float]:
        """
        Generates a mock embedding vector for the given text.
        """
        # Create a deterministic seed from the text
        seed = int(hashlib.sha256(text.encode("utf-8")).hexdigest(), 16) % 10**8
        random.seed(seed)
        # Generate a mock 10-dim vector
        return [random.random() for _ in range(10)]


class HallucinationDetector:
    """
    Detects potential hallucinations in text using heuristics and mock embeddings.
    """

    def __init__(self) -> None:
        self.embedding_model = MockEmbeddingModel()
        self.risk_phrases: List[str] = [
            "probably",
            "i think",
            "maybe",
            "not sure",
            "could be",
            "rumored",
            "allegedly",
            "might",
        ]
        logger.info(
            "HallucinationDetector initialized with %d risk phrases.",
            len(self.risk_phrases),
        )

    def detect_risk_phrases(self, text: str) -> List[str]:
        """
        Scans text for known risk phrases indicating uncertainty.
        """
        found = []
        lower_text = text.lower()
        for phrase in self.risk_phrases:
            if phrase in lower_text:
                found.append(phrase)
        return found

    def compute_hallucination_score(
        self, text: str, context: str = ""
    ) -> Dict[str, Any]:
        """
        Analyzes text for potential hallucinations.
        Returns a probability score (0-100%) where 100% is high likelihood of hallucination.
        """
        logger.debug("Computing hallucination score for text length: %d", len(text))

        risk_phrases = self.detect_risk_phrases(text)

        # Heuristic 1: Risk Phrases
        phrase_score = len(risk_phrases) * 15

        # Heuristic 2: Length/Complexity
        # (Very short or very long run-on sentences can be risky)
        length_score = 0
        words = text.split()
        if len(words) < 3:
            length_score = 10  # Too short to be factual?

        # Heuristic 3: Mock Context Consistency (if context provided)
        consistency_score = 0
        if context:
            # Simulating semantic similarity check
            text_words: Set[str] = set(text.lower().split())
            context_words: Set[str] = set(context.lower().split())
            overlap = text_words.intersection(context_words)

            # Avoid division by zero
            if text_words and (len(overlap) / len(text_words) < 0.3):
                consistency_score = 40  # Low overlap with context
                logger.debug("Low context overlap detected.")

        total_score = min(100, phrase_score + length_score + consistency_score)

        logger.info("Hallucination score computed: %d", total_score)

        return {
            "hallucination_probability": total_score,
            "risk_factors": {
                "risk_phrases_detected": risk_phrases,
                "context_consistency_risk": consistency_score > 0,
                "length_risk": length_score > 0,
            },
            "explanation": (
                f"Detected {len(risk_phrases)} uncertainty markers. "
                f"Context overlap analysis {'failed' if consistency_score > 0 else 'passed'}."
            ),
        }

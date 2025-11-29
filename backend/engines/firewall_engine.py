from typing import Any, Dict, Optional

from backend.core.logger import logger


class FirewallEngine:
    """
    Enforces policies based on Trust Scores and operational modes.
    """

    def __init__(self) -> None:
        self.modes = ["strict", "balanced", "permissive"]
        self.current_mode = "balanced"
        logger.info("FirewallEngine initialized in '%s' mode.", self.current_mode)

    def set_mode(self, mode: str) -> None:
        """
        Updates the firewall operation mode.
        """
        if mode in self.modes:
            self.current_mode = mode
            logger.info("Firewall mode set to: %s", mode)
        else:
            logger.warning("Attempted to set invalid firewall mode: %s", mode)

    def enforce(
        self, text: str, trust_score: int, details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Decides the action based on Trust Score and current Mode.
        Actions: PASS, SOFTEN, BLOCK
        """
        action = "PASS"
        modified_text = text
        warning: Optional[str] = None

        # Thresholds
        block_threshold = 30
        warn_threshold = 70

        if self.current_mode == "strict":
            block_threshold = 50
            warn_threshold = 85
        elif self.current_mode == "permissive":
            block_threshold = 15
            warn_threshold = 50

        if trust_score < block_threshold:
            action = "BLOCK"
            modified_text = (
                "[CONTENT BLOCKED BY AHTSE FIREWALL: High Hallucination Risk Detected]"
            )
            warning = "This response was blocked due to low trust score."
            logger.warning(
                "Content BLOCKED. Score: %d < Threshold: %d",
                trust_score,
                block_threshold,
            )

        elif trust_score < warn_threshold:
            action = "SOFTEN"
            warning = "Caution: This response may contain unverified information."
            modified_text = f"[AHTSE WARNING: {warning}]\n\n{text}"
            logger.info(
                "Content SOFTENED. Score: %d < Threshold: %d",
                trust_score,
                warn_threshold,
            )

        return {
            "action": action,
            "original_text": text,
            "final_output": modified_text,
            "firewall_mode": self.current_mode,
            "warning_message": warning,
        }

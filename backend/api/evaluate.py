from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from backend.core.logger import logger
from backend.engines.firewall_engine import FirewallEngine
from backend.engines.trustscore import TrustScoreEngine

router = APIRouter()


# Dependency Injection
def get_trust_engine() -> TrustScoreEngine:
    return TrustScoreEngine()


def get_firewall_engine() -> FirewallEngine:
    return FirewallEngine()


class EvaluateRequest(BaseModel):
    text: str
    context: Optional[str] = ""
    mode: Optional[str] = "balanced"


class EvaluateResponse(BaseModel):
    trust_analysis: Dict[str, Any]
    firewall_decision: Dict[str, Any]


@router.post("/evaluate", response_model=EvaluateResponse)
async def evaluate_text(
    req: EvaluateRequest,
    trust_engine: TrustScoreEngine = Depends(get_trust_engine),
    firewall_engine: FirewallEngine = Depends(get_firewall_engine),
) -> EvaluateResponse:
    """
    Full evaluation pipeline: Trust Score + Firewall Decision.
    """
    logger.info("Received evaluation request. Mode: %s", req.mode)
    try:
        # 1. Compute Trust Score
        score_data = trust_engine.calculate_trust_score(req.text, req.context)

        # 2. Apply Firewall
        firewall_engine.set_mode(req.mode or "balanced")
        firewall_result = firewall_engine.enforce(
            req.text, score_data["trust_score"], score_data["details"]
        )

        return EvaluateResponse(
            trust_analysis=score_data, firewall_decision=firewall_result
        )
    except Exception as e:
        logger.error("Error during evaluation: %s", str(e), exc_info=True)
        raise HTTPException(
            status_code=500, detail="Internal Server Error during evaluation"
        )


@router.get("/health")
async def health_check() -> Dict[str, str]:
    return {"status": "AHTSE System Operational", "version": "1.0.0"}

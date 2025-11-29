from backend.engines.detector import HallucinationDetector
from backend.engines.firewall_engine import FirewallEngine
from backend.engines.trustscore import TrustScoreEngine


def test_hallucination_detector():
    detector = HallucinationDetector()

    # Test risky text
    risky_text = "I think it might be true probably."
    score = detector.compute_hallucination_score(risky_text)
    assert score["hallucination_probability"] > 0
    assert "probably" in score["risk_factors"]["risk_phrases_detected"]

    # Test safe text
    safe_text = "The quick brown fox jumps over the lazy dog."
    score = detector.compute_hallucination_score(safe_text)
    assert score["hallucination_probability"] < 20  # Should be low


def test_trust_score_engine():
    engine = TrustScoreEngine()

    # Test high trust
    text = "This is a verified fact. [1]"
    result = engine.calculate_trust_score(text)
    assert result["trust_score"] > 50

    # Test low trust
    text = "I think maybe this is fake."
    result = engine.calculate_trust_score(text)
    assert result["trust_score"] < 100


def test_firewall_engine():
    fw = FirewallEngine()

    # Test Block
    result = fw.enforce("Bad content", 10, {})
    assert result["action"] == "BLOCK"
    assert "BLOCKED" in result["final_output"]

    # Test Pass
    result = fw.enforce("Good content", 90, {})
    assert result["action"] == "PASS"
    assert result["final_output"] == "Good content"

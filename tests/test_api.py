def test_health_check(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "AHTSE System Operational"


def test_evaluate_endpoint(client):
    payload = {
        "text": "The sky is blue.",
        "context": "The sky is blue.",
        "mode": "balanced",
    }
    response = client.post("/api/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "trust_analysis" in data
    assert "firewall_decision" in data
    assert data["firewall_decision"]["action"] == "PASS"


def test_evaluate_risky_endpoint(client):
    payload = {"text": "I think maybe it is probably false.", "mode": "strict"}
    response = client.post("/api/evaluate", json=payload)
    assert response.status_code == 200
    data = response.json()
    # In strict mode, this should likely be softened or blocked
    assert data["firewall_decision"]["action"] in ["SOFTEN", "BLOCK"]

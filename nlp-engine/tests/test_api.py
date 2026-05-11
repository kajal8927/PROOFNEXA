from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "version" in data

def test_version_endpoint():
    response = client.get("/api/version")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data

def test_compare_two_texts():
    payload = {
        "text1": "This is the first test text for matching.",
        "text2": "This is the second test text for matching."
    }
    response = client.post("/api/compare-two-texts", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "similarity" in data
    assert "riskLevel" in data
    assert "matches" in data
    assert "processingTimeMs" in data

def test_analyze_text_validation_error():
    # Empty text should trigger validation error
    payload = {
        "text": ""
    }
    response = client.post("/api/analyze-text", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data["success"] is False
    assert "detail" in data

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_create_payment():
    payload = {
        "beneficiary":"Test Vendor", "country":"DE", "account_identifier":"DE123456789",
        "amount":1200, "currency":"EUR", "purpose":"Test services",
        "is_new_beneficiary":False, "country_risk":0.1, "invoice_match":True,
        "corridor_failure_rate":0.02, "transaction_frequency":10
    }
    r = client.post("/api/payments", json=payload)
    assert r.status_code == 200
    assert r.json()["reference"].startswith("TQI-")
    assert 0 <= r.json()["risk_score"] <= 100

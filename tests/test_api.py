from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_classify_endpoint():
    response = client.post(
        "/classify",
        json={
            "subject": "Suspicious account activity",
            "message": "We saw a phishing attempt and think the account was compromised.",
            "customer_tier": "pro",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["department"] == "security"
    assert body["priority"] in {"medium", "high", "urgent"}

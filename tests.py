from fastapi.testclient import TestClient

from main import app


def test_client():
    client = TestClient(app)
    response = client.get("/api/v1/subscription", params={"token": "test"})
    assert response.status_code
    print(response.text)

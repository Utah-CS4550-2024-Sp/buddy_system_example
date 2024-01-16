from fastapi.testclient import TestClient

from backend.main import app


def test_get_all_users():
    client = TestClient(app)
    response = client.get("/users")
    assert response.status_code == 200

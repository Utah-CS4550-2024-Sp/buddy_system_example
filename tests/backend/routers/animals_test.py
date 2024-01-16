from fastapi.testclient import TestClient

from backend.main import app


def test_get_all_animals():
    client = TestClient(app)
    response = client.get("/animals")
    assert response.status_code == 200
    
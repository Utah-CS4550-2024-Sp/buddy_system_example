from backend.auth import _build_access_token


def test_get_all_users(client, user_fixture):
    db_users = [user_fixture(username=username) for username in ["juniper", "reginald"]]
    response = client.get("/users")
    assert response.status_code == 200

    meta = response.json()["meta"]
    users = response.json()["users"]

    assert meta["count"] == len(db_users)
    assert {user["username"] for user in users} == {
        db_user.username for db_user in db_users
    }


def test_get_current_user(logged_in_client):
    response = logged_in_client.get("/users/me")
    assert response.status_code == 200
    user = response.json()["user"]
    assert user["username"] == "juniper"


def test_get_current_user_not_logged_in(client):
    response = client.get("/users/me")
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }
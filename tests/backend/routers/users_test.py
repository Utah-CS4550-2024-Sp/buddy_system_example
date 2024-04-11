import pytest

from backend import database as db


def test_get_all_users(client, session, user_fixture):
    db_users = [
        user_fixture(username=username)
        for username in ["juniper", "reginald"]
    ]

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
    assert response.json() == {"detail": "Not authenticated"}


#class TestGetUser:
#   """
#   Test class for `GET /user/{user_id}.





#   """

#   @classmethod
#   def convert_to_json(self, entity):
#       return {
#           key: value
#           for key, value in entity.model_dump(mode="json").items()
#           if key != "hashed_password"
#           and value is not None
#       }

#   @pytest.fixture(autouse=True)
#   def user(self, user_fixture):
#       return user_fixture()

#   @pytest.fixture
#   def user_json(self, session, user):
#       session.refresh(user)
#       return {
#           key: value
#           for key, value in user.model_dump(mode="json").items()
#           if key != "hashed_password"
#       }

#   @pytest.fixture(autouse=True)
#   def fosters(self, user, animal_fixture, add_foster_relation):
#       animals = [animal_fixture(name=name) for name in ["chompers", "waffle party"]]
#       for animal in animals:
#           add_foster_relation(user, animal)
#       return animals

#   @pytest.fixture(autouse=True)
#   def pets(self, user, animal_fixture, add_adoption_relation):
#       animals = [animal_fixture(name=name) for name in ["bagels", "paperclip"]]
#       for animal in animals:
#           add_adoption_relation(user, animal)
#       return animals

#   @pytest.fixture(autouse=True)
#   def other_animals(
#       self, user_fixture, animal_fixture, add_foster_relation, add_adoption_relation
#   ):
#       other_user = user_fixture("other user")
#       add_foster_relation(other_user, animal_fixture("other foster"))
#       add_adoption_relation(other_user, animal_fixture("other pet"))

#   def test_get_user(self, client, user, user_json):
#       response = client.get(f"/users/{user.id}")
#       assert response.status_code == 200
#       assert response.json() == {"user": user_json}

#   def test_get_user_with_fosters(self, client, session, user, user_json, fosters):
#       for foster in fosters:
#           session.refresh(foster)
#       session.refresh(user)

#       response = client.get(f"/users/{user.id}?include=fosters")
#       assert response.status_code == 200
#       assert response.json() == {
#           "user": user_json,
#           "fosters": [foster.model_dump(mode="json") for foster in fosters],
#       }

#   def test_get_user_with_pets(self, client, session, user, user_json, pets):
#       for pet in pets:
#           session.refresh(pet)

#       response = client.get(f"/users/{user.id}?include=pets")
#       assert response.status_code == 200
#       assert response.json() == {
#           "user": user_json,
#           "pets": [pet.model_dump(mode="json") for pet in pets],
#       }

#   def test_get_user_with_fosters_and_pets(self, client, session, user, user_json, fosters, pets):
#       for animal in [*fosters, *pets]:
#           session.refresh(animal)

#       response = client.get(f"/users/{user.id}?include=pets&include=fosters")
#       assert response.status_code == 200
#       assert response.json() == {
#           "user": user_json,
#           "pets": [pet.model_dump(mode="json") for pet in pets],
#           "fosters": [foster.model_dump(mode="json") for foster in fosters],
#       }

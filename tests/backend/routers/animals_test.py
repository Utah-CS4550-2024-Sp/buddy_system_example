from datetime import date

import pytest

from backend import database as db
from backend.entities import AnimalInDB


@pytest.fixture
def default_animals():
    return [
        AnimalInDB(
            id=1,
            name="chompers",
            age=2,
            kind="cat",
            fixed=True,
            vaccinated=False,
            intake_date=date.fromisoformat("2021-05-05"),
        ),
        AnimalInDB(
            id=2,
            name="paperclip",
            age=5,
            kind="dog",
            fixed=False,
            vaccinated=True,
            intake_date=date.fromisoformat("2020-02-02"),
        ),
        AnimalInDB(
            id=3,
            name="bagels",
            age=99,
            kind="turtle",
            fixed=True,
            vaccinated=True,
            intake_date=date.fromisoformat("2023-11-23"),
        ),
    ]


def test_get_all_animals(client, session, default_animals):
    expected_names = ["bagels", "chompers", "paperclip"]  # sorted by name
    session.add_all(default_animals)
    session.commit()

    response = client.get("/animals")
    assert response.status_code == 200

    meta = response.json()["meta"]
    animals = response.json()["animals"]

    assert meta["count"] == len(default_animals)
    assert [animal["name"] for animal in animals] == expected_names


def test_get_all_animals_sorted_by_age(client, session, default_animals):
    expected_names = ["chompers", "paperclip", "bagels"]  # sorted by age
    session.add_all(default_animals)
    session.commit()

    response = client.get("/animals?sort=age")
    assert response.status_code == 200

    meta = response.json()["meta"]
    animals = response.json()["animals"]

    assert meta["count"] == len(default_animals)
    assert [animal["name"] for animal in animals] == expected_names


def test_get_all_animals_sorted_by_intake_date(client, session, default_animals):
    expected_names = ["paperclip", "chompers", "bagels"]  # sorted by intake date
    session.add_all(default_animals)
    session.commit()

    response = client.get("/animals?sort=intake_date")
    assert response.status_code == 200

    meta = response.json()["meta"]
    animals = response.json()["animals"]

    assert meta["count"] == len(default_animals)
    assert [animal["name"] for animal in animals] == expected_names


def test_get_all_animals_after_date(client, session, default_animals):
    expected_names = ["bagels", "chompers"]  # sorted by age, filtered for intake after 2021-01-01
    session.add_all(default_animals)
    session.commit()

    response = client.get("/animals?intake_after=2021-01-01")
    assert response.status_code == 200

    meta = response.json()["meta"]
    animals = response.json()["animals"]

    assert meta["count"] == len(expected_names)
    assert [animal["name"] for animal in animals] == expected_names


def test_get_all_animals_before_date(client, session, default_animals):
    expected_names = ["chompers", "paperclip"]  # sorted by age, filtered for intake before 2022-12-31
    session.add_all(default_animals)
    session.commit()

    response = client.get("/animals?intake_before=2022-12-31")
    assert response.status_code == 200

    meta = response.json()["meta"]
    animals = response.json()["animals"]

    assert meta["count"] == len(expected_names)
    assert [animal["name"] for animal in animals] == expected_names


def test_get_all_animals_between_dates(client, session, default_animals):
    expected_names = ["chompers"]  # filterd for intake in 2021 or 2022
    session.add_all(default_animals)
    session.commit()

    response = client.get("/animals?intake_after=2021-01-01&intake_before=2022-12-31")
    assert response.status_code == 200

    meta = response.json()["meta"]
    animals = response.json()["animals"]

    assert meta["count"] == len(expected_names)
    assert [animal["name"] for animal in animals] == expected_names


def test_create_animal(client, session):
    create_params = {
        "name": "karl barx",
        "age": 3,
        "kind": "dog",
    }
    response = client.post("/animals", json=create_params)

    assert response.status_code == 200
    data = response.json()
    assert "animal" in data
    animal = data["animal"]
    for key, value in create_params.items():
        assert animal[key] == value
    assert animal["intake_date"] == date.today().isoformat()

    # test that new animal is persisted
    assert session.get(AnimalInDB, animal["id"]) is not None


def test_get_animal(client, session, default_animals):
    db_animal = default_animals[0]
    session.add(db_animal)
    session.commit()

    animal_id = db_animal.id
    response = client.get(f"/animals/{animal_id}")
    assert response.status_code == 200

    animal = response.json()["animal"]
    expected_animal = db_animal.model_dump(mode="json")
    for key, value in animal.items():
        assert value == expected_animal[key]


def test_get_animal_invalid_id(client):
    animal_id = 999
    response = client.get(f"/animals/{animal_id}")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Animal",
            "entity_id": animal_id,
        },
    }


def test_update_animal_name_age(client, session, default_animals):
    db_animal = default_animals[0]
    session.add(db_animal)
    session.commit()

    update_params = {"name": "nibbles", "age": 15}
    response = client.put(f"/animals/{db_animal.id}", json=update_params)
    assert response.status_code == 200

    animal = response.json()["animal"]
    old_animal = db_animal.model_dump(mode="json")
    for key, value in animal.items():
        if key in update_params:
            assert value == update_params[key]
        else:
            assert value == old_animal[key]

    # test that updates are persisted
    session.refresh(db_animal)
    for key, value in update_params.items():
        assert value == getattr(db_animal, key)


def test_update_animal_invalid_id(client):
    animal_id = 999
    update_params = {
        "name": "updated name",
        "age": 100,
    }
    response = client.put(f"/animals/{animal_id}", json=update_params)
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Animal",
            "entity_id": animal_id,
        },
    }


def test_delete_animal(client, session, default_animals):
    db_animal = default_animals[0]
    session.add(db_animal)
    session.commit()

    response = client.delete(f"/animals/{db_animal.id}")
    assert response.status_code == 204
    assert response.content == b""

    # test that the delete is persisted
    assert session.get(AnimalInDB, db_animal.id) is None


def test_delete_animal_invalid_id(client):
    animal_id = 999
    response = client.delete(f"/animals/{animal_id}")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Animal",
            "entity_id": animal_id,
        },
    }

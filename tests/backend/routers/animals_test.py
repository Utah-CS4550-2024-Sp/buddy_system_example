from datetime import date

from fastapi.testclient import TestClient

from backend.main import app


def test_get_all_animals():
    client = TestClient(app)
    response = client.get("/animals")
    assert response.status_code == 200

    meta = response.json()["meta"]
    animals = response.json()["animals"]
    assert meta["count"] == len(animals)
    assert animals == sorted(animals, key=lambda animal: animal["name"])


def test_get_all_animals_sorted_by_age():
    client = TestClient(app)
    response = client.get("/animals?sort=age")
    assert response.status_code == 200

    meta = response.json()["meta"]
    animals = response.json()["animals"]
    assert meta["count"] == len(animals)
    assert animals == sorted(animals, key=lambda animal: animal["age"])


def test_get_all_animals_sorted_by_intake_date():
    client = TestClient(app)
    response = client.get("/animals?sort=intake_date")
    assert response.status_code == 200

    meta = response.json()["meta"]
    animals = response.json()["animals"]
    assert meta["count"] == len(animals)
    assert animals == sorted(
        animals,
        key=lambda animal: date.fromisoformat(animal["intake_date"]),
    )
    # date ISO format: yyyy-mm-dd
    # datetime ISO format: yyyy-mm-ddThh:mm:ss


def test_get_all_animals_after_date():
    client = TestClient(app)
    response = client.get("/animals?intake_after=2023-05-10")
    assert response.status_code == 200

    meta = response.json()["meta"]
    animals = response.json()["animals"]
    assert meta["count"] == len(animals)

    lower_bound = date(2023, 5, 10)
    for animal in animals:
        intake_date = date.fromisoformat(animal["intake_date"])
        assert intake_date >= lower_bound


def test_get_all_animals_before_date():
    client = TestClient(app)
    response = client.get("/animals?intake_before=2023-05-10")
    assert response.status_code == 200

    meta = response.json()["meta"]
    animals = response.json()["animals"]
    assert meta["count"] == len(animals)

    upper_bound = date(2023, 5, 10)
    for animal in animals:
        intake_date = date.fromisoformat(animal["intake_date"])
        assert intake_date <= upper_bound


def test_get_all_animals_between_dates():
    client = TestClient(app)
    response = client.get("/animals?intake_after=2022-05-10&intake_before=2023-02-25")
    assert response.status_code == 200

    meta = response.json()["meta"]
    animals = response.json()["animals"]
    assert meta["count"] == len(animals)

    lower_bound = date(2022, 5, 10)
    upper_bound = date(2023, 2, 25)
    for animal in animals:
        intake_date = date.fromisoformat(animal["intake_date"])
        assert lower_bound <= intake_date <= upper_bound


def test_create_animal():
    create_params = {
        "name": "karl barx",
        "age": 3,
        "kind": "dog",
    }
    client = TestClient(app)
    response = client.post("/animals", json=create_params)

    assert response.status_code == 200
    # old thing
    # animal = response.json()
    # new thing
    # animal = resposne.json()["animal"]
    data = response.json()
    assert "animal" in data
    animal = data["animal"]
    for key, value in create_params.items():
        assert animal[key] == value

    response = client.get(f"/animals/{animal['id']}")
    assert response.status_code == 200
    data = response.json()
    assert "animal" in data
    animal = data["animal"]
    for key, value in create_params.items():
        assert animal[key] == value


def test_get_animal():
    animal_id = "75ada30d3f504c9682683c3b6fad4bff"
    expected_animal = {
        "id": animal_id,
        "name": "nibbles",
        "age": 2,
        "kind": "cat",
        "fixed": False,
        "vaccinated": False,
        "intake_date": "2023-12-10",
    }
    client = TestClient(app)
    response = client.get(f"/animals/{animal_id}")
    assert response.status_code == 200
    assert response.json() == {"animal": expected_animal}


def test_get_animal_invalid_id():
    animal_id = "abcdefghijklmnopqrstrv1234567890"
    client = TestClient(app)
    response = client.get(f"/animals/{animal_id}")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Animal",
            "entity_id": animal_id,
        },
    }


def test_update_animal_name_age():
    animal_id = "75ada30d3f504c9682683c3b6fad4bff"
    update_params = {"name": "nibbles, jr", "age": 3}
    expected_animal = {
        "id": animal_id,
        "name": update_params["name"],
        "age": update_params["age"],
        "kind": "cat",
        "fixed": False,
        "vaccinated": False,
        "intake_date": "2023-12-10",
    }
    client = TestClient(app)
    response = client.put(f"/animals/{animal_id}", json=update_params)
    assert response.status_code == 200
    assert response.json() == {"animal": expected_animal}

    # test that the update is persisted
    response = client.get(f"/animals/{animal_id}")
    assert response.status_code == 200
    assert response.json() == {"animal": expected_animal}


def test_update_animal_invalid_id():
    animal_id = "invalid_id"
    update_params = {
        "name": "updated name",
        "age": 100,
    }
    client = TestClient(app)
    response = client.put(f"/animals/{animal_id}", json=update_params)
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Animal",
            "entity_id": animal_id,
        },
    }


def test_delete_animal():
    animal_id = "75ada30d3f504c9682683c3b6fad4bff"
    client = TestClient(app)
    response = client.delete(f"/animals/{animal_id}")
    assert response.status_code == 204
    assert response.content == b""

    # test that the delete is persisted
    response = client.get(f"/animals/{animal_id}")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Animal",
            "entity_id": animal_id,
        },
    }


def test_delete_animal_invalid_id():
    animal_id = "invalid_id"
    client = TestClient(app)
    response = client.delete(f"/animals/{animal_id}")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Animal",
            "entity_id": animal_id,
        },
    }

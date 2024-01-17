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
        animals, key=lambda animal: date.fromisoformat(animal["intake_date"])
    )


def test_get_all_animals_after_date():
    client = TestClient(app)
    response = client.get("/animals?intake_after=2023-05-10")
    assert response.status_code == 200

    meta = response.json()["meta"]
    animals = response.json()["animals"]
    assert meta["count"] == len(animals)
    for animal in animals:
        intake_date = date.fromisoformat(animal["intake_date"])
        assert intake_date.year >= 2023
        if intake_date.year == 2023:
            assert intake_date.month >= 5
            if intake_date.month == 5:
                assert intake_date.day >= 10


def test_get_all_animals_before_date():
    client = TestClient(app)
    response = client.get("/animals?intake_before=2023-05-10")
    assert response.status_code == 200

    meta = response.json()["meta"]
    animals = response.json()["animals"]
    assert meta["count"] == len(animals)
    for animal in animals:
        intake_date = date.fromisoformat(animal["intake_date"])
        assert intake_date.year <= 2023
        if intake_date.year == 2023:
            assert intake_date.month <= 5
            if intake_date.month == 5:
                assert intake_date.day <= 10


def test_get_all_animals_between_dates():
    client = TestClient(app)
    response = client.get("/animals?intake_after=2022-05-10&intake_before=2023-02-25")
    assert response.status_code == 200

    meta = response.json()["meta"]
    animals = response.json()["animals"]
    assert meta["count"] == len(animals)
    for animal in animals:
        intake_date = date.fromisoformat(animal["intake_date"])
        assert 2022 <= intake_date.year <= 2023
        if intake_date.year == 2023:
            assert intake_date.month <= 2
            if intake_date.month == 2:
                assert intake_date.day <= 25
        if intake_date.year == 2022:
            assert intake_date.month >= 5
            if intake_date.month == 5:
                assert intake_date.day >= 10


def test_create_animal():
    create_params = {
        "name": "karl barx",
        "age": 3,
        "kind": "dog",
    }
    client = TestClient(app)
    response = client.post("/animals", json=create_params)

    assert response.status_code == 200
    animal = response.json()
    for key, value in create_params.items():
        assert animal[key] == value

    response = client.get(f"/animals/{response.json()['id']}")
    assert response.status_code == 200
    animal = response.json()
    for key, value in create_params.items():
        assert animal[key] == value

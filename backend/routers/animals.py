from datetime import date
from typing import Literal

from fastapi import APIRouter

from backend.entities import (
    AnimalCollection,
    AnimalCreate,
    AnimalInDB,
    AnimalUpdate,
)
from backend import database as db

animals_router = APIRouter(prefix="/animals", tags=["Animals"])


@animals_router.get("", response_model=AnimalCollection)
def get_animals(
    sort: Literal["age", "name", "intake_date"] = "name",
    intake_after: date = None,
    intake_before: date = None,
):
    """Get a collection of animals."""

    # getattr(animal, "age") ~> animal.age
    sort_key = lambda animal: getattr(animal, sort)
    animals = db.get_all_animals()

    if intake_after is not None:
        animals = [animal for animal in animals if animal.intake_date >= intake_after]

    if intake_before is not None:
        animals = [animal for animal in animals if animal.intake_date <= intake_before]

    return AnimalCollection(
        meta={"count": len(animals)},
        animals=sorted(animals, key=sort_key),
    )


@animals_router.post("", response_model=AnimalInDB)
def create_animal(animal_create: AnimalCreate):
    """Add a new animal to the buddy system."""

    return db.create_animal(animal_create)


@animals_router.get(
    "/{animal_id}",
    response_model=AnimalInDB,
    description="Get an animal for a given animal id.",
)
def get_animal(animal_id: str):
    """Get an animal for a given id."""

    return db.get_animal_by_id(animal_id)


@animals_router.put("/{animal_id}", response_model=AnimalInDB)
def update_animal(animal_id: str, animal_update: AnimalUpdate):
    """Update an animal for a given id."""

    return db.update_animal(animal_id, animal_update)


@animals_router.delete(
    "/{animal_id}",
    status_code=204,
    response_model=None,
)
def delete_animal(animal_id: str) -> None:
    db.delete_animal(animal_id)


@animals_router.get("/{animal_id}/foster")
def get_animal_foster(animal_id: str):
    pass


@animals_router.get("/{animal_id}/adoption")
def get_animal_adoption(animal_id: str):
    pass

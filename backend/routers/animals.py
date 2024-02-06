from datetime import date
from typing import Literal

from fastapi import APIRouter, Depends
from sqlmodel import Session

from backend.entities import (
    AnimalCollection,
    AnimalCreate,
    AnimalUpdate,
    AnimalResponse,
)
from backend import database as db

animals_router = APIRouter(prefix="/animals", tags=["Animals"])


@animals_router.get("", response_model=AnimalCollection)
def get_animals(
    sort: Literal["age", "name", "intake_date"] = "name",
    intake_after: date = None,
    intake_before: date = None,
    session: Session = Depends(db.get_session)
):
    """Get a collection of animals."""

    # getattr(animal, "age") ~> animal.age
    sort_key = lambda animal: getattr(animal, sort)
    animals = db.get_all_animals(session)

    if intake_after is not None:
        animals = [animal for animal in animals if animal.intake_date >= intake_after]

    if intake_before is not None:
        animals = [animal for animal in animals if animal.intake_date <= intake_before]

    return AnimalCollection(
        meta={"count": len(animals)},
        animals=sorted(animals, key=sort_key),
    )


@animals_router.post("", response_model=AnimalResponse)
def create_animal(
    animal_create: AnimalCreate,
    session: Session = Depends(db.get_session)
):
    """Add a new animal."""

    return AnimalResponse(animal=db.create_animal(session, animal_create))


@animals_router.get("/{animal_id}", response_model=AnimalResponse)
def get_animal(
    animal_id: int,
    session: Session = Depends(db.get_session)
):
    """Get an animal for a given id."""

    return AnimalResponse(animal=db.get_animal_by_id(session, animal_id))


@animals_router.put("/{animal_id}", response_model=AnimalResponse)
def update_animal(
    animal_id: str,
    animal_update: AnimalUpdate,
    session: Session = Depends(db.get_session),
):
    """Update an animal for a given id."""

    return AnimalResponse(
        animal=db.update_animal(session, animal_id, animal_update),
    )


@animals_router.delete("/{animal_id}", status_code=204, response_model=None)
def delete_animal(
    animal_id: int,
    session: Session = Depends(db.get_session),
) -> None:
    db.delete_animal(session, animal_id)

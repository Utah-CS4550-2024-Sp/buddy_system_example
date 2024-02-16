from datetime import date

from backend.entities import *


def test_relationships(session):
    juniper = UserInDB(
        username="juniper",
        email="juniper@cool.email",
        hashed_password="hashed___password",
    )
    nibbles = AnimalInDB(
        name="nibbles jr",
        age=5,
        kind="cat",
        fixed=True,
        vaccinated=True,
        adopter=juniper,
        adoption_date=date(2024, 2, 13),
    )
    session.add(juniper)
    session.add(nibbles)
    session.commit()
    session.refresh(juniper)
    session.refresh(nibbles)

    assert nibbles.adopter == juniper
    assert nibbles in juniper.pets

import json
from datetime import date
from uuid import uuid4

from backend.entities import (
    AnimalInDB,
    AnimalCreate,
    AnimalUpdate,
    UserInDB,
    UserCreate,
    UserUpdate,
)

with open("backend/fake_db.json", "r") as f:
    DB = json.load(f)


#   -------- animals --------   #


def get_all_animals() -> list[AnimalInDB]:
    """
    Retrieve all animals from the database.

    :return: ordered list of animals
    """

    return [AnimalInDB(**animal_data) for animal_data in DB["animals"].values()]


def create_animal(animal_create: AnimalCreate) -> AnimalInDB:
    """
    Create a new animal in the database.

    :param animal_create: attributes of the animal to be created
    :return: the newly created animal
    """

    animal = AnimalInDB(
        id=uuid4().hex,
        intake_date=date.today(),
        **animal_create.model_dump(),
    )
    DB["animals"][animal.id] = animal.model_dump()
    return animal


def get_animal_by_id(animal_id: str) -> AnimalInDB:
    """
    Retrieve an animal from the database.

    :param animal_id: id of the animal to be retrieved
    :return: the retrieved animal
    """

    return AnimalInDB(**DB["animals"][animal_id])


def update_animal(animal_id: str, animal_update: AnimalUpdate) -> AnimalInDB:
    """
    Update an animal in the database.

    :param animal_id: id of the animal to be updated
    :param animal_update: attributes to be updated on the animal
    :return: the updated animal
    """

    animal = get_animal_by_id(animal_id)
    for key, value in animal_update.update_attributes().items():
        setattr(animal, key, value)
    return animal


def delete_animal(animal_id: str):
    """
    Delete an animal from the database.

    :param animal_id: the id of the animal to be deleted
    :raises EntityNotFoundException: if no such animal exists
    """

    animal = get_animal_by_id(animal_id)
    del DB["animals"][animal.id]


#   -------- users --------   #


def get_all_users() -> list[UserInDB]:
    """
    Retrieve all users from the database.

    :return: ordered list of users
    """

    return [UserInDB(**user_data) for user_data in DB["users"].values()]


def create_user(user_create: UserCreate) -> UserInDB:
    """
    Create a new user in the database.

    :param user_create: attributes of the user to be created
    :return: the newly created user
    """

    user = UserInDB(
        id=uuid4().hex,
        intake_date=date.today(),
        **user_create.model_dump(),
    )
    DB["users"][user.id] = user.model_dump()
    return user


def get_user_by_id(user_id: str) -> UserInDB:
    """
    Retrieve an user from the database.

    :param user_id: id of the user to be retrieved
    :return: the retrieved user
    """

    return UserInDB(**DB["users"][user_id])


def update_user(user_id: str, user_update: UserUpdate) -> UserInDB:
    """
    Update an user in the database.

    :param user_id: id of the user to be updated
    :param user_update: attributes to be updated on the user
    :return: the updated user
    """

    user = get_user_by_id(user_id)
    for key, value in user_update.update_attributes().items():
        setattr(user, key, value)
    return user


def delete_user(user_id: str):
    """
    Delete an user from the database.

    :param user_id: the id of the user to be deleted
    """

    user = get_user_by_id(user_id)
    del DB["users"][user.id]

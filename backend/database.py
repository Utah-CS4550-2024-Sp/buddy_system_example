import json
from datetime import date
from uuid import uuid4

from sqlmodel import Session, SQLModel, create_engine, select

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

engine = create_engine(
    "sqlite:///backend/buddy_system.db",
    echo=True,
    connect_args={"check_same_thread": False},
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


class EntityNotFoundException(Exception):
    def __init__(self, *, entity_name: str, entity_id: str):
        self.entity_name = entity_name
        self.entity_id = entity_id


#   -------- animals --------   #


def get_all_animals(session: Session) -> list[AnimalInDB]:
    """
    Retrieve all animals from the database.

    :return: ordered list of animals
    """
    return session.exec(select(AnimalInDB)).all()


def create_animal(session: Session, animal_create: AnimalCreate) -> AnimalInDB:
    """
    Create a new animal in the database.

    :param animal_create: attributes of the animal to be created
    :return: the newly created animal
    """

    animal = AnimalInDB(**animal_create.model_dump())
    session.add(animal)
    session.commit()
    session.refresh(animal)
    return animal


def get_animal_by_id(session: Session, animal_id: int) -> AnimalInDB:
    """
    Retrieve an animal from the database.

    :param animal_id: id of the animal to be retrieved
    :return: the retrieved animal
    :raises EntityNotFoundException: if no such animal id exists
    """
    animal = session.get(AnimalInDB, animal_id)
    if animal:
        return animal

    raise EntityNotFoundException(entity_name="Animal", entity_id=animal_id)


def update_animal(
    session: Session,
    animal_id: int,
    animal_update: AnimalUpdate,
) -> AnimalInDB:
    """
    Update an animal in the database.

    :param animal_id: id of the animal to be updated
    :param animal_update: attributes to be updated on the animal
    :return: the updated animal
    :raises EntityNotFoundException: if no such animal id exists
    """

    animal = get_animal_by_id(session, animal_id)
    for attr, value in animal_update.model_dump(exclude_unset=True).items():
        setattr(animal, attr, value)

    session.add(animal)
    session.commit()
    session.refresh(animal)

    return animal


def delete_animal(session: Session, animal_id: int):
    """
    Delete an animal from the database.

    :param animal_id: the id of the animal to be deleted
    :raises EntityNotFoundException: if no such animal exists
    """

    animal = get_animal_by_id(session, animal_id)
    session.delete(animal)
    session.commit()


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

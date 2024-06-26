import os

from sqlalchemy import func
from sqlmodel import Session, SQLModel, create_engine, select

from backend.entities import (
    AnimalInDB,
    AnimalCreate,
    AnimalUpdate,
    FosterInDB,
    UserInDB,
    UserUpdate,
    Foster,
)


def get_db_url():
    loc = os.environ.get("DB_LOCATION")
    if loc == "efs":
        return "sqlite:////mnt/efs/buddy_system.db"
    if loc == "rds":
        username = os.environ.get("PG_USERNAME")
        password = os.environ.get("PG_PASSWORD")
        endpoint = os.environ.get("PG_ENDPOINT")
        port = os.environ.get("PG_PORT")
        return f"postgresql://{username}:{password}@{endpoint}:{port}/{username}"

    return "sqlite:///backend/buddy_system.db"


def get_engine():
    db_url = get_db_url()
    echo = os.environ.get("DB_DEBUG", default="False").lower() in ("true", "1", "t")
    if os.environ.get("DB_LOCATION") == "rds":
        connect_args = {}
    else:
        connect_args = {"check_same_thread": False}

    return create_engine(db_url, echo=echo, connect_args=connect_args)


engine = get_engine()


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


class EntityNotFoundException(Exception):
    def __init__(self, *, entity_name: str, entity_id: int):
        self.entity_name = entity_name
        self.entity_id = entity_id


#   -------- animals --------   #


def get_all_animals(session: Session) -> list[AnimalInDB]:
    """
    Retrieve all animals from the database.

    :return: list of animals
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


def get_foster_count(session: Session, user_id: int) -> int:
    statement = select(
        func(count(FosterInDB.id))
    ).where(FosterInDB.user_id == user_id)
    return session.scalar(statement)


def get_fosters(session: Session, user_id: int) -> list[Foster]:
    user = get_user_by_id(session, user_id)
    statement = select(
        FosterInDB,
        AnimalInDB,
    ).join(
        AnimalInDB,
        FosterInDB.animal_id == AnimalInDB.id,
    ).where(
        FosterInDB.user_id == user_id
    )
    results = session.exec(statement).all()
    return [
        Foster(
            animal=animal,
            user=user,
            start_date=foster.start_date,
            end_date=foster.end_date,
        )
        for foster, animal in results
    ]


#   -------- users --------   #


def get_all_users(session: Session) -> list[UserInDB]:
    """
    Retrieve all users from the database.

    :return: list of users
    """

    return session.exec(select(UserInDB)).all()


def get_user_by_id(session: Session, user_id: int) -> UserInDB:
    """
    Retrieve a user from the database.

    :param user_id: id of the user to be retrieved
    :return: the retrieved user
    """

    user = session.get(UserInDB, user_id)
    if user:
        return user

    raise EntityNotFoundException(entity_name="User", entity_id=user_id)


def update_user(session: Session, user_id: int, user_update: UserUpdate) -> UserInDB:
    """
    Update a user in the database.

    :param user_id: id of the user to be updated
    :param user_update: attributes to be updated on the user
    :return: the updated user
    """

    user = get_user_by_id(session, user_id)
    for key, value in user_update.update_attributes().items():
        setattr(user, key, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def delete_user(session: Session, user_id: int):
    """
    Delete a user from the database.

    :param user_id: the id of the user to be deleted
    """

    user = get_user_by_id(session, user_id)
    session.delete(user)
    session.commit()


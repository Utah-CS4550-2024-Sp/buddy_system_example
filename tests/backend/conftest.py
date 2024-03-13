from datetime import date, datetime

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, StaticPool, create_engine

from backend import auth
from backend.main import app
from backend import database as db


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def client(session):
    def _get_session_override():
        return session

    app.dependency_overrides[db.get_session] = _get_session_override

    yield TestClient(app)

    app.dependency_overrides.clear()


@pytest.fixture
def logged_in_client(session, user_fixture):
    def _get_session_override():
        return session

    def _get_current_user_override():
        return user_fixture(username="juniper")

    app.dependency_overrides[db.get_session] = _get_session_override
    app.dependency_overrides[auth.get_current_user] = _get_current_user_override

    yield TestClient(app)

    app.dependency_overrides.clear()


@pytest.fixture
def animal_fixture(session):
    def _build_animal(
        name: str = "chompers",
        age: int = 2,
        kind: str = "cat",
        fixed: bool = True,
        vaccinated: bool = True,
        intake_date: date = date.today(),
    ) -> db.AnimalInDB:
        animal = db.AnimalInDB(
            name=name,
            age=age,
            kind=kind,
            fixed=fixed,
            vaccinated=vaccinated,
            intake_date=intake_date,
        )

        session.add(animal)
        session.commit()
        session.refresh(animal)

        return animal

    return _build_animal


@pytest.fixture
def user_fixture(session):
    def _build_user(
        username: str = "juniper",
        email: str = "juniper@cool.email",
        password: str = "password",
    ) -> db.UserInDB:
        return auth.register_new_user(
            auth.UserRegistration(
                username=username,
                email=email,
                password=password,
            ),
            session,
        )

    return _build_user


@pytest.fixture
def add_foster_relation(session):
    def _build_foster(
        user: db.UserInDB,
        animal: db.AnimalInDB,
        start_date: date = date(2024, 1, 15),
        end_date: date = date(2024, 2, 10),
    ) -> db.FosterInDB:
        foster = db.FosterInDB(
            user_id=user.id,
            animal_id=animal.id,
            start_date=start_date,
            end_date=end_date,
        )
        session.add(foster)
        session.commit()
        session.refresh(foster)
        return foster

    return _build_foster


@pytest.fixture
def add_adoption_relation(session):
    def _add_adoption(
        user: db.UserInDB,
        animal: db.AnimalInDB,
        adoption_date: date = date.today(),
    ):
        animal.adopter_id = user.id
        animal.adoption_date = adoption_date
        session.add(animal)
        session.commit()
        session.refresh(animal)

    return _add_adoption

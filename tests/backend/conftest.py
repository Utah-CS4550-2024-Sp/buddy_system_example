from datetime import datetime

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
        created_at: datetime = datetime.now(),
    ) -> db.AnimalInDB:
        animal = db.AnimalInDB(
            name=name,
            age=age,
            kind=kind,
            fixed=fixed,
            vaccinated=vaccinated,
            created_at=created_at,
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

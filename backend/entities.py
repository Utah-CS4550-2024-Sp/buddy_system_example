from datetime import date, datetime

from pydantic import BaseModel, Field


class AnimalInDB(BaseModel):
    """Represents an animal in the database."""

    id: str
    name: str
    age: int
    kind: str
    fixed: bool
    vaccinated: bool
    intake_date: date


class UserInDB(BaseModel):
    """Represents a user in the database."""

    id: str
    name: str
    email: str
    created_at: datetime


class AnimalResponse(BaseModel):
    """Represents an API response for an animal."""

    animal: AnimalInDB


class Animal(AnimalInDB):
    """(unused) Represents an API response for an animal."""

    adopter: str = None
    adoption_date: date = None


class User(BaseModel):
    """Represents an API response for a user."""

    id: str
    name: str
    created_at: datetime


class Foster(BaseModel):
    """Represents an API response for a foster."""

    user: User
    animal: Animal
    start_date: date
    end_date: date


class Adoption(BaseModel):
    """Represents an API response for an adoption."""

    user: User
    animal: Animal
    adoption_date: date


class AnimalCreate(BaseModel):
    """Represents parameters for adding a new animal to the system."""

    name: str
    age: int
    kind: str
    fixed: bool = False
    vaccinated: bool = False


class AnimalUpdate(BaseModel):
    """Represents parameters for updating an animal in the system."""

    name: str = None
    age: int = None
    kind: str = Field(
        default=None,
        description="the type of animal",
        examples=["dog", "cat", "turtle"],
    )
    fixed: bool = None
    vaccinated: bool = None


class UserCreate(BaseModel):
    """Represents parameters for adding a new user to the system."""

    id: str
    email: str


class UserUpdate(BaseModel):
    """Represents parameters for updating a user in the system."""

    id: str = None
    email: str = None


class Metadata(BaseModel):
    """Represents metadata for a collection."""

    count: int


class AnimalCollection(BaseModel):
    """Represents an API response for a collection of animals."""

    meta: Metadata
    animals: list[AnimalInDB]


class UserCollection(BaseModel):
    """Represents an API response for a collection of users."""

    meta: Metadata
    users: list[User]

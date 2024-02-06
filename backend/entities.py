from datetime import date, datetime

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class Metadata(BaseModel):
    """Represents metadata for a collection."""

    count: int


# ---------- animals ---------- #

class AnimalInDB(SQLModel, table=True):
    """Database model for an animal."""

    __tablename__ = "animals"

    id: int = Field(default=None, primary_key=True)
    name: str
    age: int
    kind: str
    fixed: bool
    vaccinated: bool
    intake_date: date = Field(default_factory=date.today)


# ----- request models ----- #

class AnimalCreate(SQLModel):
    """Represents parameters for adding a new animal to the system."""

    name: str
    age: int
    kind: str
    fixed: bool = Field(default=False)
    vaccinated: bool = Field(default=False)


class AnimalUpdate(SQLModel):
    """Represents parameters for updating an animal in the system."""

    name: str = None
    age: int = None
    kind: str = None
    fixed: bool = None
    vaccinated: bool = None


# ----- response models ----- #

class Animal(SQLModel):
    """Data model for an animal."""
    id: int
    name: str
    age: int
    kind: str
    fixed: bool
    vaccinated: bool
    intake_date: date


class AnimalResponse(BaseModel):
    """Represents an API response for an animal."""

    animal: Animal


class AnimalCollection(BaseModel):
    """Represents an API response for a collection of animals."""

    meta: Metadata
    animals: list[Animal]


# ---------- users ---------- #


class UserInDB(BaseModel):
    """Represents a user in the database."""

    id: str
    name: str
    email: str
    created_at: datetime


class User(BaseModel):
    """Represents an API response for a user."""

    id: str
    name: str
    created_at: datetime


class UserCreate(BaseModel):
    """Represents parameters for adding a new user to the system."""

    id: str
    email: str


class UserUpdate(BaseModel):
    """Represents parameters for updating a user in the system."""

    id: str = None
    email: str = None



class UserCollection(BaseModel):
    """Represents an API response for a collection of users."""

    meta: Metadata
    users: list[User]

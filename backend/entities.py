from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel


# ------------------------------------- #
#            database models            #
# ------------------------------------- #

class FosterInDB(SQLModel, table=True):
    __tablename__ = "fosters"

    user_id: int = Field(primary_key=True, foreign_key="users.id")
    animal_id: int = Field(primary_key=True, foreign_key="animals.id")
    start_date: date
    end_date: date


class AnimalInDB(SQLModel, table=True):
    """Database model for animal."""

    __tablename__ = "animals"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    kind: str
    fixed: bool
    vaccinated: bool
    intake_date: Optional[date] = Field(default_factory=date.today)
    adopter_id: Optional[int] = Field(default=None, foreign_key="users.id")
    adoption_date: Optional[date] = Field(default=None)

    adopter: Optional["UserInDB"] = Relationship()
    foster_users: list["UserInDB"] = Relationship(link_model=FosterInDB)


class UserInDB(SQLModel, table=True):
    """Database model for user."""

    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    email: str
    hashed_password: str
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    pets: list[AnimalInDB] = Relationship()
    foster_animals: list[AnimalInDB] = Relationship(link_model=FosterInDB)


# ------------------------------------- #
#            request models            #
# ------------------------------------- #

class AnimalCreate(SQLModel):
    """Request model for adding new animal to the system."""

    name: str
    age: int
    kind: str
    fixed: bool = Field(default=False)
    vaccinated: bool = Field(default=False)


class AnimalUpdate(SQLModel):
    """Request model for updating animal in the system."""

    name: str = None
    age: int = None
    kind: str = None
    fixed: bool = None
    vaccinated: bool = None
    adopter_id: Optional[int] = None
    adoption_date: Optional[date] = None


class UserCreate(SQLModel):
    """Request model for adding new user to the system."""

    id: str
    username: str
    email: str
    password: str


class UserUpdate(SQLModel):
    """Request model for updating user in the system."""

    username: str = None
    email: str = None
    password: str = None


# ------------------------------------- #
#            response models            #
# ------------------------------------- #

class Metadata(BaseModel):
    """Represents metadata for a collection."""

    count: int


class Animal(SQLModel):
    """Data model for animal."""

    id: int
    name: str
    age: int
    kind: str
    fixed: bool
    vaccinated: bool
    intake_date: date


class AnimalResponse(BaseModel):
    """API response for animal."""

    animal: Animal


class AnimalCollection(BaseModel):
    """API response for a collection of animals."""

    meta: Metadata
    animals: list[Animal]


class User(SQLModel):
    """Data model for user."""

    id: str
    username: str
    email: str
    created_at: datetime


class UserResponse(BaseModel):
    """API response for user."""

    user: User


class UserCollection(BaseModel):
    """API response for a collection of users."""

    meta: Metadata
    users: list[User]

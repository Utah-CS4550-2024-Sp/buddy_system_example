from fastapi import APIRouter, Depends
from sqlmodel import Session

from backend import database as db
from backend.auth import get_current_user
from backend.entities import AnimalCollection, UserInDB, UserCollection, UserResponse

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("", response_model=UserCollection)
def get_users(session: Session = Depends(db.get_session)):
    users = db.get_all_users(session)
    return UserCollection(
        meta={"count": len(users)},
        users=users,
    )


@users_router.get("/me", response_model=UserResponse)
def get_self(user: UserInDB = Depends(get_current_user)):
    """Get current user."""
    return UserResponse(user=user)


@users_router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, session: Session = Depends(db.get_session)):
    return UserResponse(
        user=db.get_user_by_id(session, user_id),
    )


@users_router.delete("/{user_id}", status_code=204)
def delete_user(user_id: str, session: Session = Depends(db.get_session)):
    db.delete_user(session, user_id)


@users_router.get("/{user_id}/fosters", response_model=AnimalCollection)
def get_user_fosters(user_id: str, session: Session = Depends(db.get_session)):
    user = db.get_user_by_id(session, user_id)
    foster_animals = user.foster_animals
    return AnimalCollection(
        meta={"count": len(foster_animals)},
        animals=foster_animals,
    )


@users_router.get("/{user_id}/adoptions")
def get_user_adoptions(user_id: str):
    pass

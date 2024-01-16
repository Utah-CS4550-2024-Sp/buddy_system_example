from fastapi import APIRouter

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("")
def get_users():
    pass


@users_router.post("")
def create_user():
    pass


@users_router.get("/{user_id}")
def get_user(user_id: str):
    pass


@users_router.put("/{user_id}")
def update_user(user_id: str):
    pass


@users_router.delete("/{user_id}")
def delete_user(user_id: str):
    pass


@users_router.get("/{user_id}/fosters")
def get_user_fosters(user_id: str):
    pass


@users_router.get("/{user_id}/adoptions")
def get_user_adoptions(user_id: str):
    pass

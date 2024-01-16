from fastapi import APIRouter

animals_router = APIRouter(prefix="/animals", tags=["Animals"])


@animals_router.get("")
def get_animals():
    pass


@animals_router.post("")
def create_animal():
    pass


@animals_router.get("/{animal_id}")
def get_animal(animal_id: str):
    pass


@animals_router.put("/{animal_id}")
def update_animal(animal_id: str):
    pass


@animals_router.delete("/{animal_id}")
def delete_animal(animal_id: str):
    pass


@animals_router.get("/{animal_id}/foster")
def get_animal_foster(animal_id: str):
    pass


@animals_router.get("/{animal_id}/adoption")
def get_animal_adoption(animal_id: str):
    pass

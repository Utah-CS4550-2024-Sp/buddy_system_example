import json
from datetime import date, datetime

from sqlmodel import Session

from backend.auth import pwd_context
from backend.database import engine, create_db_and_tables
from backend.entities import *


def seed_database():
    with open("backend/fake_db.json", "r") as f:
        DB = json.load(f)

    create_db_and_tables()

    with Session(engine) as session:
        animals = [
            AnimalInDB(
                **{
                    **animal_data,
                    "id": None,
                    "intake_date": date.fromisoformat(
                        animal_data["intake_date"],
                    ),
                }
            )
            for animal_data in DB["animals"].values()
        ]

        users = [
            UserInDB(
                **{
                    **user_data,
                    "id": None,
                    "username": user_data["id"],
                    "created_at": datetime.fromisoformat(
                        user_data["created_at"],
                    ).replace(
                        microsecond=0
                    ),
                    "hashed_password": pwd_context.hash("password"),
                }
            )
            for user_data in DB["users"].values()
        ]

        session.add_all(animals)
        session.add_all(users)
        session.commit()

        for adoption in DB["adoptions"]:
            animal_name = DB["animals"][adoption["animal_id"]]["name"]
            user_name = adoption["user_id"]
            animal = next(a for a in animals if a.name == animal_name)
            user = next(u for u in users if u.username == user_name)
            animal.adopter_id = user.id
            animal.adoption_date = date.fromisoformat(adoption["adoption_date"])

        session.add_all(animals)
        session.commit()

        for foster in DB["fosters"]:
            animal_name = DB["animals"][foster["animal_id"]]["name"]
            user_name = foster["user_id"]
            animal = next(a for a in animals if a.name == animal_name)
            user = next(u for u in users if u.username == user_name)
            foster = FosterInDB(
                user_id=user.id,
                animal_id=animal.id,
                start_date=date.fromisoformat(foster["start_date"]),
                end_date=date.fromisoformat(foster["end_date"]),
            )
            session.add(foster)

        session.commit()

        return {
            "user_count": len(users),
            "animal_count": len(animals),
        }

def lambda_handler(event, context):
    try:
        result = seed_database()
        return {
            "statusCode": 200,
            "body": json.dumps(result)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }


if __name__ == "__main__":
    seed_database()


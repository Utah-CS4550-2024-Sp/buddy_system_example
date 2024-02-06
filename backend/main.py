from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse

from sqlmodel import Field, Session, SQLModel, create_engine, select

from backend.routers.animals import animals_router
from backend.routers.users import users_router
from backend.database import create_db_and_tables, EntityNotFoundException

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="buddy system API",
    description="API for managing fosters and adoptions.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(animals_router)
app.include_router(users_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# # define a table # class Person(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str


# # create an engine
# engine = create_engine(
#     "sqlite:///test.db",
#     echo=True,
#     connect_args={"check_same_thread": False},
# )


# # create database and tables
# SQLModel.metadata.create_all(engine)


# # define session dependency
# # a dependency is a callable function (takes no arguments)

# def get_session():
#     with Session(engine) as session:
#         yield session


# # define routes that use the database

# @app.get("/persons", response_model=list[Person])
# def get_persons(session: Session = Depends(get_session)):
#     return session.exec(select(Person)).all()


# @app.post("/persons", response_model=Person)
# def create_person(person: Person, session: Session = Depends(get_session)):
#     session.add(person)
#     session.commit()
#     session.refresh(person)
#     return person


# @app.get("/persons/{person_id}", response_model=Person)
# def get_person(person_id: int, session: Session = Depends(get_session)):
#     person = session.get(Person, person_id)
#     if person:
#         return person
#     raise EntityNotFoundException(entity_name="Person", entity_id=person_id)


@app.exception_handler(EntityNotFoundException)
def handle_entity_not_found(
    _request: Request,
    exception: EntityNotFoundException,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "detail": {
                "type": "entity_not_found",
                "entity_name": exception.entity_name,
                "entity_id": exception.entity_id,
            },
        },
    )


@app.get("/", include_in_schema=False)
def default() -> str:
    return HTMLResponse(
        content=f"""
        <html>
            <body>
                <h1>{app.title}</h1>
                <p>{app.description}</p>
                <h2>API docs</h2>
                <ul>
                    <li><a href="/docs">Swagger</a></li>
                    <li><a href="/redoc">ReDoc</a></li>
                </ul>
            </body>
        </html>
        """,
    )

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from mangum import Mangum

from backend.auth import auth_router
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

app.include_router(auth_router)
app.include_router(animals_router)
app.include_router(users_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/greet")
def greet():
    """Greet a collection of people."""
    greeting = "hello to nobody"
    return {"greeting": greeting}


lambda_app = FastAPI()
lambda_app.mount("/default", app)

handler = Mangum(lambda_app)


from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse

from backend.routers.animals import animals_router
from backend.routers.users import users_router
from backend.database import EntityNotFoundException

app = FastAPI(
    title="buddy system API",
    description="API for managing fosters and adoptions.",
    version="0.1.0",
)

app.include_router(animals_router)
app.include_router(users_router)


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

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from .core.config import settings
from .db.session import create_db_and_tables
from .api.endpoints import user, auth

app = FastAPI(
    title="USER SERVICE APIs",
    version="0.0.1",
    servers=[
        {
            "url": "http://127.0.0.1:8000",  # ADD NGROK URL Here Before Creating GPT Action
            "description": "Development Server"
        }
    ]
)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    print("Creating tables...")
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "User Service is running"}

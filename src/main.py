from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from src.db import engine
from src.api.router import main_router
from src.models.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    print("Все таблицы созданы")
    yield

app = FastAPI(
    title="JARVIS",
    lifespan=lifespan,
)
app.include_router(main_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:5501",
        "http://127.0.0.1:5501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


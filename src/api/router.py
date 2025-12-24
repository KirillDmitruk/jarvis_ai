from fastapi import APIRouter

from src.api.jarvis import router as jarvis_router

main_router = APIRouter()

main_router.include_router(jarvis_router)

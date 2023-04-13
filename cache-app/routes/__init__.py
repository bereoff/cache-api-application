from fastapi import APIRouter

from .books import router as books_router
from .health import router as health_router

main_router = APIRouter()

main_router.include_router(books_router, prefix="/api/v1", tags=["books"])
main_router.include_router(health_router, prefix="/api/v1", tags=["health"])

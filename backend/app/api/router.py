from fastapi import APIRouter

from app.api.routes import autenticacao, health, usuarios


api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(autenticacao.router)
api_router.include_router(usuarios.router)

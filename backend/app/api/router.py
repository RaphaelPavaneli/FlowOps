from fastapi import APIRouter

from app.api.routes import autenticacao, dashboard, equipes, health, usuarios


api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(autenticacao.router)
api_router.include_router(usuarios.router)
api_router.include_router(equipes.router)
api_router.include_router(dashboard.router)

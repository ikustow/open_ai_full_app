"""
Основной маршрутизатор API v1
"""
from fastapi import APIRouter
from src.api.v1.endpoints import agents, chat_simple as chat

api_router = APIRouter()

# Подключение эндпоинтов
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])

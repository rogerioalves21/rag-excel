from fastapi import APIRouter
from app.api.routes import (
    data_analysis,
    files,
    ollama,
    chat
)

api_router = APIRouter()

api_router.include_router(ollama.router, tags=["ollama"])
api_router.include_router(files.router, tags=["files"])
api_router.include_router(data_analysis.router, tags=["data-analysis"])
api_router.include_router(chat.router, tags=["chat"])

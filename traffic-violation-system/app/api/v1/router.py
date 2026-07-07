from fastapi import APIRouter
from app.api.v1.routes import system

api_router = APIRouter()

# Include system and other future routers under version 1
api_router.include_router(system.router)

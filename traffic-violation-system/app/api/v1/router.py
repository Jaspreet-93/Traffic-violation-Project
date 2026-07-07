from fastapi import APIRouter
from app.api.v1.routes import system, camera, violation, email_logs

api_router = APIRouter()

# Include system and other routers under version 1
api_router.include_router(system.router)
api_router.include_router(camera.router)
api_router.include_router(violation.router)
api_router.include_router(email_logs.router)

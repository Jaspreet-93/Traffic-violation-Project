import os
import time
import shutil
import random
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from app.database.connection import check_db_connection, SessionLocal

try:
    import psutil
except ImportError:
    psutil = None

router = APIRouter(tags=["System"])

START_TIME = time.time()

RECENT_ERRORS = []

def log_system_error(service: str, message: str):
    RECENT_ERRORS.append({
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "service": service,
        "error": message
    })
    if len(RECENT_ERRORS) > 15:
        RECENT_ERRORS.pop(0)

@router.get("/")
async def root():
    """
    Welcome endpoint returning basic metadata about the API.
    """
    return {
        "message": "Traffic Violation Detection Backend Running"
    }

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Checks database, SOTA models, storage space, and system resources.
    """
    from app.services.system.health_service import HealthService
    return HealthService.get_health_status()

from fastapi import WebSocket, WebSocketDisconnect
from app.services.system.health_service import ws_manager

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)

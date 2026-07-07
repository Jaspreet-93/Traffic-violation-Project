from fastapi import APIRouter, status
from app.schemas.helmet import (
    HelmetStatusResponse,
    HelmetStartResponse,
    HelmetStopResponse
)
from app.services.helmet.helmet_service import helmet_service

router = APIRouter(prefix="/helmet", tags=["Helmet Detection"])

@router.post("/start", response_model=HelmetStartResponse, status_code=status.HTTP_200_OK)
def start_helmet_detection():
    """
    Enables custom YOLOv8 helmet detection on the active camera stream.
    """
    helmet_service.start_helmet_detection()
    return {
        "message": "Helmet detection started",
        "status": "running"
    }

@router.post("/stop", response_model=HelmetStopResponse, status_code=status.HTTP_200_OK)
def stop_helmet_detection():
    """
    Disables custom YOLOv8 helmet detection on the active camera stream.
    """
    helmet_service.stop_helmet_detection()
    return {
        "message": "Helmet detection stopped",
        "status": "stopped"
    }

@router.get("/status", response_model=HelmetStatusResponse, status_code=status.HTTP_200_OK)
def get_helmet_status():
    """
    Retrieves the running status of the helmet detection pipeline.
    """
    return {
        "running": helmet_service.get_status()
    }

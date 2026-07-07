from fastapi import APIRouter, status
from app.schemas.detection import (
    DetectionStatusResponse,
    DetectionStartResponse,
    DetectionStopResponse
)
from app.services.detection.detection_service import detection_service

router = APIRouter(prefix="/detection", tags=["Vehicle Detection"])

@router.post("/start", response_model=DetectionStartResponse, status_code=status.HTTP_200_OK)
def start_detection():
    """
    Enables real-time YOLOv8 vehicle detection on the active camera stream.
    """
    detection_service.start_detection()
    return {
        "message": "Vehicle detection started",
        "status": "running"
    }

@router.post("/stop", response_model=DetectionStopResponse, status_code=status.HTTP_200_OK)
def stop_detection():
    """
    Disables real-time YOLOv8 vehicle detection on the active camera stream.
    """
    detection_service.stop_detection()
    return {
        "message": "Vehicle detection stopped",
        "status": "stopped"
    }

@router.get("/status", response_model=DetectionStatusResponse, status_code=status.HTTP_200_OK)
def get_detection_status():
    """
    Retrieves the running status of the real-time vehicle detection pipeline.
    """
    return {
        "running": detection_service.get_status()
    }

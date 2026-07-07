from fastapi import APIRouter, status
from app.schemas.number_plate import (
    PlateStatusResponse,
    PlateStartResponse,
    PlateStopResponse
)
from app.services.number_plate.plate_service import plate_service

router = APIRouter(prefix="/number-plate", tags=["Number Plate Detection"])

@router.post("/start", response_model=PlateStartResponse, status_code=status.HTTP_200_OK)
def start_plate_detection():
    """
    Enables custom YOLOv8 vehicle number plate detection on the active camera stream.
    """
    plate_service.start_plate_detection()
    return {
        "message": "Number plate detection started",
        "status": "running"
    }

@router.post("/stop", response_model=PlateStopResponse, status_code=status.HTTP_200_OK)
def stop_plate_detection():
    """
    Disables custom YOLOv8 vehicle number plate detection on the active camera stream.
    """
    plate_service.stop_plate_detection()
    return {
        "message": "Number plate detection stopped",
        "status": "stopped"
    }

@router.get("/status", response_model=PlateStatusResponse, status_code=status.HTTP_200_OK)
def get_plate_status():
    """
    Retrieves the running status of the vehicle number plate detection pipeline.
    """
    return {
        "running": plate_service.get_status()
    }

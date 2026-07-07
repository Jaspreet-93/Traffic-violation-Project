from fastapi import APIRouter, status
from app.schemas.driver_behavior import (
    DriverBehaviorStatusResponse,
    DriverBehaviorStartResponse,
    DriverBehaviorStopResponse
)
from app.services.driver_behavior.behavior_service import behavior_service

router = APIRouter(prefix="/driver-behavior", tags=["Driver Behavior Detection"])

@router.post("/start", response_model=DriverBehaviorStartResponse, status_code=status.HTTP_200_OK)
def start_driver_behavior():
    """
    Enables custom YOLOv8 driver behavior detection on the active stream.
    """
    behavior_service.start_behavior_detection()
    return {
        "message": "Driver behavior detection started",
        "status": "running"
    }

@router.post("/stop", response_model=DriverBehaviorStopResponse, status_code=status.HTTP_200_OK)
def stop_driver_behavior():
    """
    Disables custom YOLOv8 driver behavior detection on the active stream.
    """
    behavior_service.stop_behavior_detection()
    return {
        "message": "Driver behavior detection stopped",
        "status": "stopped"
    }

@router.get("/status", response_model=DriverBehaviorStatusResponse, status_code=status.HTTP_200_OK)
def get_driver_behavior_status():
    """
    Retrieves the running status of the driver behavior detection pipeline.
    """
    return {
        "running": behavior_service.get_status()
    }

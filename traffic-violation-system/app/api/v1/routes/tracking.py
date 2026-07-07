from fastapi import APIRouter, status
from app.schemas.tracking import (
    TrackingStatusResponse,
    TrackingStartResponse,
    TrackingStopResponse
)
from app.services.tracking.tracking_service import tracking_service

router = APIRouter(prefix="/tracking", tags=["Vehicle Tracking"])

@router.post("/start", response_model=TrackingStartResponse, status_code=status.HTTP_200_OK)
def start_tracking():
    """
    Enables ByteTrack multi-object vehicle tracking on the active camera stream.
    """
    tracking_service.start_tracking()
    return {
        "message": "Vehicle tracking started",
        "status": "running"
    }

@router.post("/stop", response_model=TrackingStopResponse, status_code=status.HTTP_200_OK)
def stop_tracking():
    """
    Disables ByteTrack multi-object vehicle tracking on the active camera stream.
    """
    tracking_service.stop_tracking()
    return {
        "message": "Vehicle tracking stopped",
        "status": "stopped"
    }

@router.get("/status", response_model=TrackingStatusResponse, status_code=status.HTTP_200_OK)
def get_tracking_status():
    """
    Gets the running status of the real-time vehicle tracking pipeline.
    """
    return {
        "running": tracking_service.get_status()
    }

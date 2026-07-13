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

from fastapi import HTTPException
from app.services.tracking.track_manager import track_manager

@router.get("/active")
def get_active_tracks():
    """
    Returns list of all active tracked vehicles.
    """
    return track_manager.get_active_tracks()

@router.get("/statistics")
def get_tracking_statistics():
    """
    Returns general tracking statistics counters.
    """
    return track_manager.get_statistics()

@router.get("/{track_id}")
def get_track_details(track_id: int):
    """
    Returns latest tracking details for a specific track ID.
    """
    details = track_manager.get_track_by_id(track_id)
    if not details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Track ID {track_id} not found"
        )
    return details

@router.get("/history/{track_id}")
def get_track_history(track_id: int):
    """
    Returns historical centroids and frame bbox logs for a specific track ID.
    """
    history = track_manager.get_track_history(track_id)
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Track ID {track_id} has no history records"
        )
    return history

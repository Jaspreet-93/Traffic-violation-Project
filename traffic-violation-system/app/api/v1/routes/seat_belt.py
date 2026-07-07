from fastapi import APIRouter, status
from app.schemas.seat_belt import (
    SeatBeltStatusResponse,
    SeatBeltStartResponse,
    SeatBeltStopResponse
)
from app.services.seat_belt.seat_belt_service import seat_belt_service

router = APIRouter(prefix="/seat-belt", tags=["Seat Belt Detection"])

@router.post("/start", response_model=SeatBeltStartResponse, status_code=status.HTTP_200_OK)
def start_seat_belt():
    """
    Enables custom YOLOv8 seat belt usage detection on the active stream.
    """
    seat_belt_service.start_seat_belt_detection()
    return {
        "message": "Seat belt detection started",
        "status": "running"
    }

@router.post("/stop", response_model=SeatBeltStopResponse, status_code=status.HTTP_200_OK)
def stop_seat_belt():
    """
    Disables custom YOLOv8 seat belt usage detection on the active stream.
    """
    seat_belt_service.stop_seat_belt_detection()
    return {
        "message": "Seat belt detection stopped",
        "status": "stopped"
    }

@router.get("/status", response_model=SeatBeltStatusResponse, status_code=status.HTTP_200_OK)
def get_seat_belt_status():
    """
    Retrieves the running status of the seat belt detection pipeline.
    """
    return {
        "running": seat_belt_service.get_status()
    }

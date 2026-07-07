from fastapi import APIRouter, status
from app.schemas.traffic_light import (
    TrafficLightStatusResponse,
    TrafficLightStartResponse,
    TrafficLightStopResponse
)
from app.services.traffic_light.traffic_light_service import traffic_light_service

router = APIRouter(prefix="/traffic-light", tags=["Traffic Light Detection"])

@router.post("/start", response_model=TrafficLightStartResponse, status_code=status.HTTP_200_OK)
def start_traffic_light():
    """
    Enables custom YOLOv8 traffic light detection on the active stream.
    """
    traffic_light_service.start_traffic_light_detection()
    return {
        "message": "Traffic light detection started",
        "status": "running"
    }

@router.post("/stop", response_model=TrafficLightStopResponse, status_code=status.HTTP_200_OK)
def stop_traffic_light():
    """
    Disables custom YOLOv8 traffic light detection on the active stream.
    """
    traffic_light_service.stop_traffic_light_detection()
    return {
        "message": "Traffic light detection stopped",
        "status": "stopped"
    }

@router.get("/status", response_model=TrafficLightStatusResponse, status_code=status.HTTP_200_OK)
def get_traffic_light_status():
    """
    Retrieves the running status of the traffic light detection pipeline.
    """
    return {
        "running": traffic_light_service.get_status()
    }

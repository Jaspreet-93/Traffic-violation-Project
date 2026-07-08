from fastapi import APIRouter, HTTPException, status
from typing import List

from app.schemas.camera_management import (
    CameraCreate,
    CameraUpdate,
    CameraResponse,
    CameraStatusResponse,
    CameraHealthResponse
)

from app.services.camera_management.camera_service import camera_service
from app.services.camera_management.camera_health import CameraHealthMonitor
from app.services.camera_management.stream_monitor import StreamMonitor

router = APIRouter(prefix="/cameras", tags=["Enterprise Camera Management"])

@router.get("", response_model=List[CameraResponse])
def get_all_cameras():
    """
    Returns list of all registered cameras.
    """
    return camera_service.list_cameras()

@router.post("", response_model=CameraResponse, status_code=status.HTTP_201_CREATED)
def create_camera(payload: CameraCreate):
    """
    Registers a new camera device.
    """
    return camera_service.create_camera(payload.model_dump())

@router.put("/{id}", response_model=CameraResponse)
def update_camera(id: int, payload: CameraUpdate):
    """
    Modifies details of an existing camera.
    """
    res = camera_service.update_camera(id, payload.model_dump())
    if not res:
        raise HTTPException(status_code=404, detail=f"Camera with ID {id} not found.")
    return res

@router.delete("/{id}")
def delete_camera(id: int):
    """
    Removes a camera config from system tracking.
    """
    success = camera_service.delete_camera(id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Camera with ID {id} not found.")
    return {"success": True, "message": f"Camera {id} successfully removed."}

@router.get("/status", response_model=CameraStatusResponse)
def get_status():
    """
    Returns aggregate stream status values.
    """
    return StreamMonitor.get_status_summary()

@router.get("/health/{camera_id}", response_model=CameraHealthResponse)
def get_health(camera_id: int):
    """
    Returns packet loss and jitter diagnostics.
    """
    return CameraHealthMonitor.get_health_metrics(camera_id)

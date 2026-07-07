from fastapi import APIRouter, status, HTTPException
from fastapi.responses import StreamingResponse
from app.schemas.camera_stream import (
    CameraStartRequest,
    CameraStartResponse,
    CameraStopResponse,
    CameraStatusResponse
)
from app.services.camera.camera_manager import camera_manager
from app.services.camera.stream_service import StreamService

router = APIRouter(prefix="/camera", tags=["Camera Stream"])

@router.post("/start", response_model=CameraStartResponse, status_code=status.HTTP_200_OK)
def start_camera(payload: CameraStartRequest):
    """
    Starts the video capture stream from a local webcam or IP camera URL.
    """
    try:
        camera_manager.start_stream(source=payload.source)
        return {
            "message": "Camera started successfully",
            "status": "running",
            "source": payload.source
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/stop", response_model=CameraStopResponse, status_code=status.HTTP_200_OK)
def stop_camera():
    """
    Stops the active camera stream and frees video capture resources.
    """
    camera_manager.stop_stream()
    return {"message": "Camera stopped successfully"}

@router.get("/status", response_model=CameraStatusResponse)
def get_camera_status():
    """
    Gets status and active video source properties of the camera stream.
    """
    return camera_manager.get_status()

@router.get("/stream")
def get_camera_stream():
    """
    Returns a live multipart MJPEG video stream.
    """
    return StreamingResponse(
        StreamService.generate_mjpeg_stream(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

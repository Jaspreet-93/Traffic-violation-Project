from fastapi import APIRouter, status, HTTPException, File, UploadFile
from fastapi.responses import StreamingResponse
import shutil
import os
import cv2
from typing import Dict, Any

from app.schemas.camera_stream import (
    CameraStartRequest,
    CameraStartResponse,
    CameraStopResponse,
    CameraStatusResponse
)
from app.services.camera.camera_manager import camera_manager
from app.services.camera.stream_service import StreamService
from app.services.violation.violation_service import violation_service

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

@router.post("/upload")
def upload_file_detection(file: UploadFile = File(...)):
    """
    Uploads an image or video file. Videos are streamed; images are analyzed directly.
    """
    # Create uploads directory
    uploads_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "uploads"))
    os.makedirs(uploads_dir, exist_ok=True)
    
    file_path = os.path.join(uploads_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    ext = os.path.splitext(file.filename)[1].lower()
    
    # 1. Handle Video
    if ext in [".mp4", ".avi", ".mov", ".mkv"]:
        try:
            # Stop any existing running stream first
            camera_manager.stop_stream()
            # Start stream with video path as source
            camera_manager.start_stream(source=file_path)
            return {
                "type": "video",
                "message": "Video stream started successfully",
                "source": file_path
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
            
    # 2. Handle Image
    elif ext in [".jpg", ".jpeg", ".png", ".bmp"]:
        frame = cv2.imread(file_path)
        if frame is None:
            raise HTTPException(status_code=400, detail="Uploaded file is not a valid image.")
            
        # Clear violations cache so we only get violations detected in this image
        violation_service.clear_session()
        
        # Process the single frame
        annotated_frame = camera_manager.process_single_frame(frame)
        
        # Save the processed image back to outputs/violations/images/
        from app.utils.file_utils import generate_evidence_filename
        out_filename = generate_evidence_filename(99, "Uploaded Detection", "jpg")
        
        images_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "outputs", "violations", "images"))
        os.makedirs(images_dir, exist_ok=True)
        
        dest_path = os.path.join(images_dir, out_filename)
        cv2.imwrite(dest_path, annotated_frame)
        
        # Get relative path for rendering in frontend
        rel_path = f"outputs/violations/images/{out_filename}"
        
        # Retrieve generated violations
        detected_violations = list(violation_service.recorded_violations)
        
        return {
            "type": "image",
            "message": "Image analyzed successfully",
            "image_path": rel_path,
            "violations": detected_violations
        }
        
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported file format: {ext}")


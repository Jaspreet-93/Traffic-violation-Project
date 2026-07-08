import uuid
from datetime import datetime
from fastapi import APIRouter, File, UploadFile, status, HTTPException
from typing import List

from app.schemas.upload_detection import (
    UploadResponse,
    JobStatusResponse,
    DetectionResultResponse,
    HistoryResponse,
    DeleteHistoryResponse
)

from app.utils.file_validator import FileValidator
from app.services.upload_detection.upload_service import UploadService
from app.services.upload_detection.image_detector import ImageDetector
from app.services.upload_detection.video_detector import VideoDetector, jobs_registry, results_registry
from app.services.upload_detection.result_generator import ResultGenerator

router = APIRouter(prefix="/upload", tags=["Upload Detection Center"])

@router.post("/image", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_image(file: UploadFile = File(...)):
    """
    Uploads a traffic snapshot image and triggers synchronous pipeline validation.
    """
    contents = await file.read()
    size_bytes = len(contents)
    
    # 1. Validation check
    FileValidator.validate_image_file(file.filename, size_bytes)
    
    # 2. Save file
    filepath = UploadService.save_file(file.filename, contents)
    
    # 3. Create job id
    job_id = str(uuid.uuid4())
    
    # 4. Process image detection sync
    try:
        result = ImageDetector.process_image(filepath, job_id)
        results_registry[job_id] = result
        
        # Save history entry
        summary_text = result["evidence"]["summary_text"]
        UploadService.add_history_entry(job_id, file.filename, "image", "Completed", summary_text)
        
        return {
            "job_id": job_id,
            "filename": file.filename,
            "file_type": "image",
            "status": "Completed",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        UploadService.add_history_entry(job_id, file.filename, "image", "Failed", str(e))
        raise HTTPException(
            status_code=status.HTTP_550_INTERNAL_SERVER_ERROR,
            detail=f"Inference execution failure: {str(e)}"
        )

@router.post("/video", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_video(file: UploadFile = File(...)):
    """
    Uploads a video clip and registers an async frame processing job thread.
    """
    contents = await file.read()
    size_bytes = len(contents)
    
    # 1. Validation check
    FileValidator.validate_video_file(file.filename, size_bytes)
    
    # 2. Save file
    filepath = UploadService.save_file(file.filename, contents)
    
    # 3. Create job id
    job_id = str(uuid.uuid4())
    
    # 4. Trigger video processing thread
    VideoDetector.start_video_processing(filepath, job_id)
    UploadService.add_history_entry(job_id, file.filename, "video", "Processing", "Worker initialized.")

    return {
        "job_id": job_id,
        "filename": file.filename,
        "file_type": "video",
        "status": "Processing",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@router.get("/status/{job_id}", response_model=JobStatusResponse)
def get_job_status(job_id: str):
    """
    Retrieves progress coordinates for video jobs.
    """
    # If it's an image job already in results, it is Completed
    if job_id in results_registry:
        return {
            "job_id": job_id,
            "status": "Completed",
            "progress": 100.0
        }
        
    status_entry = jobs_registry.get(job_id)
    if not status_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Surveillance job '{job_id}' not found."
        )
    return status_entry

@router.get("/history", response_model=HistoryResponse)
def get_upload_history():
    """
    Audit index of uploaded media.
    """
    items = UploadService.load_history()
    return {"history": items}

@router.get("/result/{job_id}", response_model=DetectionResultResponse)
def get_detection_result(job_id: str):
    """
    Compiles box coordinates and confidence levels.
    """
    res = ResultGenerator.get_job_result(job_id)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Results for job '{job_id}' are pending, failed, or missing."
        )
    return res

@router.delete("/history/{job_id}", response_model=DeleteHistoryResponse)
def delete_history_log(job_id: str):
    """
    Purges historical logs entries.
    """
    deleted = UploadService.delete_history_entry(job_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Audit log entry for job '{job_id}' not found."
        )
    return {
        "success": True,
        "message": f"Log entry for job '{job_id}' successfully purged."
    }

from fastapi import APIRouter, status
from app.schemas.ocr import (
    OCRStatusResponse,
    OCRStartResponse,
    OCRStopResponse
)
from app.services.ocr.ocr_service import ocr_service

router = APIRouter(prefix="/ocr", tags=["Number Plate OCR"])

@router.post("/start", response_model=OCRStartResponse, status_code=status.HTTP_200_OK)
def start_ocr():
    """
    Enables custom character recognition on detected number plates.
    """
    ocr_service.start_ocr()
    return {
        "message": "OCR started",
        "status": "running"
    }

@router.post("/stop", response_model=OCRStopResponse, status_code=status.HTTP_200_OK)
def stop_ocr():
    """
    Disables custom character recognition on detected number plates.
    """
    ocr_service.stop_ocr()
    return {
        "message": "OCR stopped",
        "status": "stopped"
    }

@router.get("/status", response_model=OCRStatusResponse, status_code=status.HTTP_200_OK)
def get_ocr_status():
    """
    Retrieves the running status of the OCR text extraction pipeline.
    """
    return {
        "running": ocr_service.get_status()
    }

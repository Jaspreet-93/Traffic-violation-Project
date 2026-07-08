from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from typing import List
import os

from app.schemas.evidence import (
    EvidenceResponse,
    EvidenceDetail,
    EvidenceMetadataResponse,
    EvidenceIntegrityResponse,
    DeleteEvidenceResponse
)

from app.services.evidence.evidence_service import evidence_service
from app.services.evidence.metadata_service import MetadataService
from app.services.evidence.integrity_service import IntegrityService
from app.services.evidence.preview_service import PreviewService
from app.services.evidence.download_service import DownloadService

router = APIRouter(prefix="/evidence", tags=["Enterprise Evidence Locker"])

@router.get("", response_model=List[EvidenceResponse])
def get_all_evidence():
    """
    Returns index list of all evidence logs.
    """
    raw = evidence_service.get_all_evidence()
    return [
        EvidenceResponse(
            evidence_id=item["evidence_id"],
            violation_id=item["violation_id"],
            vehicle_id=item.get("vehicle_id"),
            violation=item["violation"],
            image_path=item["image_path"],
            video_path=item.get("video_path"),
            timestamp=item["timestamp"]
        )
        for item in raw
    ]

@router.get("/{id}", response_model=EvidenceDetail)
def get_evidence_by_id(id: int):
    """
    Retrieves details of a specific evidence record.
    """
    res = evidence_service.get_evidence_by_id(id)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evidence with ID {id} not found."
        )
    return EvidenceDetail(
        evidence_id=res["evidence_id"],
        violation_id=res["violation_id"],
        vehicle_id=res.get("vehicle_id"),
        plate_number=res.get("plate_number"),
        violation=res["violation"],
        image_path=res.get("image_path"),
        video_path=res.get("video_path"),
        timestamp=res["timestamp"]
    )

@router.get("/metadata/{id}", response_model=EvidenceMetadataResponse)
def get_metadata(id: int):
    """
    Returns resolution, models version, and file sizes metadata details.
    """
    res = evidence_service.get_evidence_by_id(id)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evidence with ID {id} not found."
        )
    return MetadataService.get_metadata(id, res.get("violation", "No Helmet"))

@router.get("/download/{id}")
def download_evidence(id: int):
    """
    Initiates file download.
    """
    res = evidence_service.get_evidence_by_id(id)
    if not res or not res.get("image_path"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evidence file not found."
        )
        
    path = DownloadService.get_download_path(res["image_path"])
    if not os.path.exists(path):
        # Fallback to standard placeholder file
        placeholder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "uploads", "processed_snapshot_mock1.jpg"))
        if os.path.exists(placeholder):
            return FileResponse(placeholder, media_type="application/octet-stream", filename=f"evidence_{id}.jpg")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File has been archived or does not exist on disk."
        )
    return FileResponse(path, media_type="application/octet-stream", filename=os.path.basename(path))

@router.get("/preview/{id}")
def preview_evidence(id: int):
    """
    Initiates image file preview.
    """
    res = evidence_service.get_evidence_by_id(id)
    if not res or not res.get("image_path"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evidence preview not available."
        )
        
    path = DownloadService.get_download_path(res["image_path"])
    if not os.path.exists(path):
        placeholder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "uploads", "processed_snapshot_mock1.jpg"))
        if os.path.exists(placeholder):
            return FileResponse(placeholder, media_type="image/jpeg")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File preview is missing."
        )
    return FileResponse(path, media_type="image/jpeg")

@router.get("/integrity/{id}", response_model=EvidenceIntegrityResponse)
def verify_integrity(id: int):
    """
    Calculates SHA-256 checksum and returns integrity status.
    """
    res = evidence_service.get_evidence_by_id(id)
    if not res:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evidence with ID {id} not found."
        )
    path = DownloadService.get_download_path(res.get("image_path", ""))
    return IntegrityService.get_integrity_status(id, path)

@router.delete("/{id}", response_model=DeleteEvidenceResponse)
def delete_evidence(id: int):
    """
    Purges an evidence log record.
    """
    success = evidence_service.delete_evidence(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evidence record with ID {id} not found."
        )
    return {
        "success": True,
        "message": f"Evidence record {id} successfully purged from locker."
    }

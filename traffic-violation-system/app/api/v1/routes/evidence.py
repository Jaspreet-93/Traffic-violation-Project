from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from typing import List, Optional
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
            timestamp=item["timestamp"],
            original_image_path=item.get("original_image_path"),
            original_video_path=item.get("original_video_path"),
            annotated_image_path=item.get("annotated_image_path"),
            annotated_video_path=item.get("annotated_video_path"),
            confidence=item.get("confidence"),
            camera_id=item.get("camera_id")
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
        timestamp=res["timestamp"],
        original_image_path=res.get("original_image_path"),
        original_video_path=res.get("original_video_path"),
        annotated_image_path=res.get("annotated_image_path"),
        annotated_video_path=res.get("annotated_video_path"),
        confidence=res.get("confidence"),
        camera_id=res.get("camera_id")
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

@router.get("/{id}/original")
def get_original_media(id: int, type: str = "image"):
    """
    Returns the original uploaded or captured media file.
    """
    res = evidence_service.get_evidence_by_id(id)
    if not res:
        raise HTTPException(status_code=404, detail="Evidence record not found.")
    
    if type == "image":
        media_path = res.get("original_image_path") or res.get("image_path")
        if media_path and "/processed_" in media_path:
            # strip processed_ prefix for original
            directory, filename = os.path.split(media_path)
            if filename.startswith("processed_"):
                filename = filename.replace("processed_", "", 1)
            media_path = os.path.join(directory, filename).replace('\\', '/')
    else:
        media_path = res.get("original_video_path") or res.get("video_path") or res.get("original_image_path") or res.get("image_path")
        if media_path and "/processed_" in media_path:
            directory, filename = os.path.split(media_path)
            if filename.startswith("processed_"):
                filename = filename.replace("processed_", "", 1)
            media_path = os.path.join(directory, filename).replace('\\', '/')

    if not media_path:
        raise HTTPException(status_code=404, detail="Original media path is missing.")
        
    path = DownloadService.get_download_path(media_path)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Original media file not found on disk.")
        
    media_type = "video/mp4" if path.endswith(".mp4") else "image/jpeg"
    return FileResponse(path, media_type=media_type)

@router.get("/{id}/processed")
def get_processed_media(id: int, type: str = "image"):
    """
    Returns the AI-processed media file with overlays.
    """
    res = evidence_service.get_evidence_by_id(id)
    if not res:
        raise HTTPException(status_code=404, detail="Evidence record not found.")
        
    if type == "image":
        media_path = res.get("annotated_image_path") or res.get("image_path")
        if media_path and not os.path.basename(media_path).startswith("processed_"):
            directory, filename = os.path.split(media_path)
            filename = f"processed_{filename}"
            media_path = os.path.join(directory, filename).replace('\\', '/')
    else:
        media_path = res.get("annotated_video_path") or res.get("video_path") or res.get("annotated_image_path") or res.get("image_path")
        if media_path and not os.path.basename(media_path).startswith("processed_"):
            directory, filename = os.path.split(media_path)
            filename = f"processed_{filename}"
            media_path = os.path.join(directory, filename).replace('\\', '/')

    if not media_path:
        raise HTTPException(status_code=404, detail="Processed media path is missing.")
        
    path = DownloadService.get_download_path(media_path)
    if not os.path.exists(path):
        # Fallback to original if processed version doesn't exist
        fallback_path = res.get("original_image_path") or res.get("image_path")
        path = DownloadService.get_download_path(fallback_path)
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail="Processed media file not found on disk.")
            
    media_type = "video/mp4" if path.endswith(".mp4") else "image/jpeg"
    return FileResponse(path, media_type=media_type)

@router.get("/{id}/snapshot")
def get_snapshot(id: int):
    """
    Returns the snapshot frame (processed image).
    """
    res = evidence_service.get_evidence_by_id(id)
    if not res or not res.get("image_path"):
        raise HTTPException(status_code=404, detail="Snapshot not available.")
        
    path = DownloadService.get_download_path(res["image_path"])
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Snapshot file not found.")
        
    return FileResponse(path, media_type="image/jpeg")

@router.get("/{id}/download")
def download_evidence_attachment(id: int):
    """
    Triggers direct file download.
    """
    res = evidence_service.get_evidence_by_id(id)
    if not res:
        raise HTTPException(status_code=404, detail="Evidence record not found.")
        
    media_path = res.get("video_path") or res.get("image_path")
    if not media_path:
        raise HTTPException(status_code=404, detail="Media file not found.")
        
    path = DownloadService.get_download_path(media_path)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File is missing on disk.")
        
    return FileResponse(path, media_type="application/octet-stream", filename=os.path.basename(path))

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

@router.get("/search", response_model=List[EvidenceResponse])
def search_evidence(
    plate_number: Optional[str] = None,
    vehicle_id: Optional[int] = None,
    evidence_id: Optional[int] = None,
    violation_type: Optional[str] = None,
    date: Optional[str] = None,
    camera: Optional[str] = None
):
    """
    Search evidence by various query params.
    """
    all_records = evidence_service.get_all_evidence()
    filtered = []
    for item in all_records:
        if plate_number and plate_number.lower() not in item.get("plate_number", "").lower():
            continue
        if vehicle_id and item.get("vehicle_id") != vehicle_id:
            continue
        if evidence_id and item.get("evidence_id") != evidence_id:
            continue
        if violation_type and violation_type.lower() not in item.get("violation", "").lower():
            continue
        if date and date not in item.get("timestamp", ""):
            continue
        if camera and camera.lower() not in item.get("camera_id", "").lower():
            continue
        filtered.append(item)
    return [
        EvidenceResponse(
            evidence_id=item["evidence_id"],
            violation_id=item["violation_id"],
            vehicle_id=item.get("vehicle_id"),
            violation=item["violation"],
            image_path=item["image_path"],
            video_path=item.get("video_path"),
            timestamp=item["timestamp"],
            original_image_path=item.get("original_image_path"),
            original_video_path=item.get("original_video_path"),
            annotated_image_path=item.get("annotated_image_path"),
            annotated_video_path=item.get("annotated_video_path"),
            confidence=item.get("confidence"),
            camera_id=item.get("camera_id")
        )
        for item in filtered
    ]

@router.get("/download/original/{id}")
def download_original(id: int):
    """
    Downloads original media attachment.
    """
    res = evidence_service.get_evidence_by_id(id)
    if not res:
        raise HTTPException(status_code=404, detail="Evidence not found.")
    media_path = res.get("original_video_path") or res.get("original_image_path") or res.get("image_path")
    if media_path and "/processed_" in media_path:
        directory, filename = os.path.split(media_path)
        if filename.startswith("processed_"):
            filename = filename.replace("processed_", "", 1)
        media_path = os.path.join(directory, filename).replace('\\', '/')
    if not media_path:
        raise HTTPException(status_code=404, detail="Original media path is missing.")
    path = DownloadService.get_download_path(media_path)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Original media file not found on disk.")
    return FileResponse(path, media_type="application/octet-stream", filename=os.path.basename(path))

@router.get("/download/annotated/{id}")
def download_annotated(id: int):
    """
    Downloads annotated media attachment.
    """
    res = evidence_service.get_evidence_by_id(id)
    if not res:
        raise HTTPException(status_code=404, detail="Evidence not found.")
    media_path = res.get("annotated_video_path") or res.get("annotated_image_path") or res.get("image_path")
    if media_path and not os.path.basename(media_path).startswith("processed_"):
        directory, filename = os.path.split(media_path)
        filename = f"processed_{filename}"
        media_path = os.path.join(directory, filename).replace('\\', '/')
    if not media_path:
        raise HTTPException(status_code=404, detail="Annotated media path is missing.")
    path = DownloadService.get_download_path(media_path)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Annotated media file not found on disk.")
    return FileResponse(path, media_type="application/octet-stream", filename=os.path.basename(path))

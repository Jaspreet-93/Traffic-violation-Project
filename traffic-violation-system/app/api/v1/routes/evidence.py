from fastapi import APIRouter, HTTPException, status, Body
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
def get_all_evidence(page: int = 1, limit: int = 20):
    """
    Returns index list of all evidence logs.
    """
    raw = evidence_service.get_all_evidence()
    start = (page - 1) * limit
    end = start + limit
    paged = raw[start:end]
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
        for item in paged
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
def preview_evidence(id: int, size: str = "thumbnail"):
    """
    Initiates image file preview. Supports thumbnail, medium, and original sizes.
    """
    res = evidence_service.get_evidence_by_id(id)
    if not res or not res.get("image_path"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evidence preview not available."
        )
        
    path = DownloadService.get_download_path(res["image_path"])
    if not os.path.exists(path):
        placeholder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "uploads", "processed_snapshot_mock1.jpg"))
        if not os.path.exists(placeholder):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File preview is missing."
            )
        path = placeholder

    if size == "original" or not (path.lower().endswith(".jpg") or path.lower().endswith(".jpeg") or path.lower().endswith(".png")):
        return FileResponse(path, media_type="image/jpeg")

    base_dir = os.path.dirname(path)
    thumb_dir = os.path.join(base_dir, "thumbnails")
    os.makedirs(thumb_dir, exist_ok=True)
    
    filename = os.path.basename(path)
    name_part, ext = os.path.splitext(filename)
    thumb_filename = f"{name_part}_{size}{ext}"
    thumb_path = os.path.join(thumb_dir, thumb_filename)
    
    if not os.path.exists(thumb_path):
        try:
            import cv2
            img = cv2.imread(path)
            if img is not None:
                h, w = img.shape[:2]
                target_w = 320 if size == "thumbnail" else 800
                if w > target_w:
                    aspect = w / h
                    target_h = int(target_w / aspect)
                    resized = cv2.resize(img, (target_w, target_h), interpolation=cv2.INTER_AREA)
                    cv2.imwrite(thumb_path, resized, [cv2.IMWRITE_JPEG_QUALITY, 80])
                else:
                    cv2.imwrite(thumb_path, img, [cv2.IMWRITE_JPEG_QUALITY, 80])
            else:
                return FileResponse(path, media_type="image/jpeg")
        except Exception:
            return FileResponse(path, media_type="image/jpeg")
            
    return FileResponse(thumb_path, media_type="image/jpeg")

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

from app.schemas.evidence import DeleteEvidenceBulkRequest, DeleteEvidenceBulkResponse, BulkDeleteProgressResponse
from app.services.evidence.evidence_service import bulk_delete_progress
import uuid

@router.delete("", response_model=DeleteEvidenceBulkResponse)
def delete_all_evidence():
    """
    Deletes all evidence records and files.
    """
    evidence_ids = evidence_service.get_all_evidence_ids()
    job_id = str(uuid.uuid4())
    bulk_delete_progress[job_id] = {
        "total": len(evidence_ids),
        "current": 0,
        "status": "processing"
    }
    evidence_service.delete_evidence_bulk(evidence_ids, job_id=job_id)
    return {
        "success": True,
        "message": f"Successfully queued bulk deletion of all {len(evidence_ids)} evidence records.",
        "job_id": job_id
    }

@router.delete("/bulk", response_model=DeleteEvidenceBulkResponse)
def delete_evidence_bulk(req: DeleteEvidenceBulkRequest = Body(...)):
    """
    Deletes selected evidence records by IDs in batch.
    """
    evidence_ids = req.ids
    job_id = str(uuid.uuid4())
    bulk_delete_progress[job_id] = {
        "total": len(evidence_ids),
        "current": 0,
        "status": "processing"
    }
    evidence_service.delete_evidence_bulk(evidence_ids, job_id=job_id)
    return {
        "success": True,
        "message": f"Successfully queued bulk deletion of {len(evidence_ids)} evidence records.",
        "job_id": job_id
    }

@router.get("/bulk/progress/{job_id}", response_model=BulkDeleteProgressResponse)
def get_bulk_delete_progress(job_id: str):
    """
    Returns progress metrics of a queued bulk deletion job.
    """
    prog = bulk_delete_progress.get(job_id)
    if not prog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bulk deletion job {job_id} not found."
        )
    return prog

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
    camera: Optional[str] = None,
    page: int = 1,
    limit: int = 20
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
    start = (page - 1) * limit
    end = start + limit
    paged = filtered[start:end]
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
        for item in paged
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

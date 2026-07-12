from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.violation import ViolationResponse, ViolationDetail
from app.services.violation.violation_service import violation_service

router = APIRouter(prefix="/violations", tags=["violations"])

@router.get("", response_model=List[ViolationResponse])
def get_violations():
    """
    Returns list of all detected violations.
    """
    try:
        raw_violations = violation_service.get_all_violations()
        return [
            ViolationResponse(
                id=item.get("id"),
                vehicle_id=item["vehicle_id"],
                plate_number=item["plate_number"],
                violation=item.get("violation_type") or item.get("violation") or "No Helmet",
                confidence=item["confidence"],
                vehicle_type=item.get("vehicle_type", "car"),
                timestamp=item.get("timestamp"),
                camera_id=item.get("camera_id"),
                evidence_id=item.get("evidence_id"),
                original_image_path=item.get("original_image_path"),
                annotated_image_path=item.get("annotated_image_path"),
                status=item.get("status")
            )
            for item in raw_violations
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{id}")
def delete_violation(id: int):
    """
    Purges a violation record by ID.
    """
    res = violation_service.delete_violation(id)
    if not res:
        raise HTTPException(
            status_code=404,
            detail=f"Violation with ID {id} not found."
        )
    return {"message": "Violation record purged successfully."}

@router.get("/{id}")
def get_violation_or_vehicle(id: int):
    """
    If the ID corresponds to a Violation, returns details of that single violation.
    Otherwise, returns list of violations for that vehicle ID.
    """
    try:
        single = violation_service.get_violation_by_id(id)
        if single:
            return single
            
        raw_violations = violation_service.get_violations_by_vehicle(id)
        return [
            ViolationDetail(
                camera_id=item["camera_id"],
                vehicle_id=item["vehicle_id"],
                plate_number=item["plate_number"],
                vehicle_type=item["vehicle_type"],
                violation_type=item["violation_type"],
                confidence=item["confidence"],
                evidence_path=item["evidence_path"]
            )
            for item in raw_violations
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}/download")
def download_evidence_package(id: int):
    """
    Downloads all evidence crops, original, and annotated frames as a single ZIP file.
    """
    import zipfile
    import io
    import os
    from fastapi.responses import StreamingResponse
    
    single = violation_service.get_violation_by_id(id)
    if not single:
        raise HTTPException(status_code=404, detail="Violation package not found")
        
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for key in ["original_image", "annotated_image", "vehicle_crop", "helmet_crop", "seatbelt_crop", "plate_crop", "trafficlight_crop", "mobile_crop", "lane_crop"]:
            rel_path = single.get(key)
            if rel_path:
                # Strip leading slash
                clean_path = rel_path.lstrip("/")
                if os.path.exists(clean_path):
                    zip_file.write(clean_path, os.path.basename(clean_path))
                    
    zip_buffer.seek(0)
    return StreamingResponse(
        zip_buffer,
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": f"attachment; filename=evidence_package_{id}.zip"}
    )

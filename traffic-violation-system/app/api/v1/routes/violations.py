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

@router.get("/{vehicle_id}", response_model=List[ViolationDetail])
def get_vehicle_violations(vehicle_id: int):
    """
    Returns list of violations for a specific vehicle by ID.
    """
    try:
        raw_violations = violation_service.get_violations_by_vehicle(vehicle_id)
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

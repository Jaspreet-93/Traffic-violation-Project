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
        # Map raw database results to matching schema format requested in the prompt
        return [
            ViolationResponse(
                vehicle_id=item["vehicle_id"],
                plate_number=item["plate_number"],
                violation=item["violation_type"],
                confidence=item["confidence"]
            )
            for item in raw_violations
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

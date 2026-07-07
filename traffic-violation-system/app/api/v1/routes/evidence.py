from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.evidence import EvidenceResponse, EvidenceDetail
from app.services.evidence.evidence_service import evidence_service

router = APIRouter(prefix="/evidence", tags=["evidence"])

@router.get("", response_model=List[EvidenceResponse])
def get_all_evidence():
    """
    Returns list of all evidence records.
    """
    try:
        raw_evidence = evidence_service.get_all_evidence()
        return [
            EvidenceResponse(
                vehicle_id=item["vehicle_id"],
                violation=item["violation"],
                image_path=item["image_path"],
                timestamp=item["timestamp"]
            )
            for item in raw_evidence
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{violation_id}", response_model=EvidenceDetail)
def get_violation_evidence(violation_id: int):
    """
    Returns evidence metadata for a specific violation ID.
    """
    try:
        res = evidence_service.get_evidence_by_violation(violation_id)
        if not res:
            raise HTTPException(status_code=404, detail=f"Evidence for violation ID {violation_id} not found.")
        return EvidenceDetail(
            evidence_id=res["evidence_id"],
            violation_id=res["violation_id"],
            vehicle_id=res["vehicle_id"],
            plate_number=res["plate_number"],
            violation=res["violation"],
            image_path=res["image_path"],
            video_path=res["video_path"],
            timestamp=res["timestamp"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

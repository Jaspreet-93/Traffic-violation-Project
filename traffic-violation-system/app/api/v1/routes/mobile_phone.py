from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.services.driver_behavior.mobile_phone_manager import mobile_phone_manager

router = APIRouter(prefix="/mobile-phone", tags=["Mobile Phone Detection Center"])

class ReverifyRequest(BaseModel):
    id: str
    track_id: int

@router.get("", status_code=status.HTTP_200_OK)
def list_mobile_phone_records():
    """
    Returns list of processed mobile phone track sessions.
    """
    records = []
    for t_id, track in mobile_phone_manager.vehicle_tracks.items():
        records.append({
            "track_id": t_id,
            "phone_use_seen": track["phone_use_seen"],
            "history_length": len(track["history"]),
            "violation_registered": track.get("violation_registered", False)
        })
    return {"records": records}

@router.get("/statistics", status_code=status.HTTP_200_OK)
def get_mobile_phone_statistics():
    """
    Returns Mobile Phone Detection statistics.
    """
    return mobile_phone_manager.get_statistics()

@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_mobile_phone_record_by_id(id: int):
    """
    Returns Mobile Phone track history record by track ID.
    """
    record = mobile_phone_manager.vehicle_tracks.get(id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mobile phone vehicle track ID '{id}' not found."
        )
    return record

@router.post("/reverify", status_code=status.HTTP_200_OK)
def trigger_reverify(payload: ReverifyRequest):
    """
    Triggers reverification of target mobile phone violation.
    """
    record = mobile_phone_manager.vehicle_tracks.get(payload.track_id)
    if not record:
        # Create a mock record
        new_record = {
            "track_id": payload.track_id,
            "phone_use_seen": True,
            "violation_registered": True,
            "history": []
        }
        mobile_phone_manager.vehicle_tracks[payload.track_id] = new_record
        return new_record
        
    record["violation_registered"] = True
    return record

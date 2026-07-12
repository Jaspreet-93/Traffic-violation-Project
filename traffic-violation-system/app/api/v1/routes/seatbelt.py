from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.services.seat_belt.seat_belt_manager import seat_belt_manager

router = APIRouter(prefix="/seatbelt", tags=["Seat Belt Detection Center"])

class ReverifyRequest(BaseModel):
    id: str
    track_id: int

@router.get("", status_code=status.HTTP_200_OK)
def list_seatbelt_records():
    """
    Returns list of processed seatbelt track sessions.
    """
    records = []
    for t_id, track in seat_belt_manager.vehicle_tracks.items():
        records.append({
            "track_id": t_id,
            "seat_belt_seen": track["seat_belt_seen"],
            "history_length": len(track["history"]),
            "violation_registered": track.get("violation_registered", False)
        })
    return {"records": records}

@router.get("/statistics", status_code=status.HTTP_200_OK)
def get_seatbelt_statistics():
    """
    Returns Seat Belt Detection statistics.
    """
    return seat_belt_manager.get_statistics()

@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_seatbelt_record_by_id(id: int):
    """
    Returns Seat Belt track history record by track ID.
    """
    record = seat_belt_manager.vehicle_tracks.get(id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Seatbelt vehicle track ID '{id}' not found."
        )
    return record

@router.post("/reverify", status_code=status.HTTP_200_OK)
def trigger_reverify(payload: ReverifyRequest):
    """
    Triggers reverification of target seatbelt violation.
    """
    record = seat_belt_manager.vehicle_tracks.get(payload.track_id)
    if not record:
        # Create a mock record
        new_record = {
            "track_id": payload.track_id,
            "seat_belt_seen": False,
            "violation_registered": True,
            "history": []
        }
        seat_belt_manager.vehicle_tracks[payload.track_id] = new_record
        return new_record
        
    record["violation_registered"] = True
    return record

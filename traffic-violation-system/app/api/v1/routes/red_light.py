from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.services.traffic_light.traffic_light_manager import traffic_light_manager

router = APIRouter(prefix="/red-light", tags=["Traffic Light Violation Center"])

class ReverifyRequest(BaseModel):
    id: str
    track_id: int

@router.get("", status_code=status.HTTP_200_OK)
def list_red_light_records():
    """
    Returns list of processed red light track sessions.
    """
    records = []
    for t_id, track in traffic_light_manager.vehicle_tracks.items():
        records.append({
            "track_id": t_id,
            "history_length": len(track["history"]),
            "violation_registered": track.get("violation_registered", False)
        })
    return {"records": records}

@router.get("/statistics", status_code=status.HTTP_200_OK)
def get_red_light_statistics():
    """
    Returns Traffic Light Detection statistics.
    """
    return traffic_light_manager.get_statistics()

@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_red_light_record_by_id(id: int):
    """
    Returns Red Light track history record by track ID.
    """
    record = traffic_light_manager.vehicle_tracks.get(id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Red light vehicle track ID '{id}' not found."
        )
    return record

@router.post("/reverify", status_code=status.HTTP_200_OK)
def trigger_reverify(payload: ReverifyRequest):
    """
    Triggers reverification of target red light violation.
    """
    record = traffic_light_manager.vehicle_tracks.get(payload.track_id)
    if not record:
        # Create a mock record
        new_record = {
            "track_id": payload.track_id,
            "violation_registered": True,
            "history": []
        }
        traffic_light_manager.vehicle_tracks[payload.track_id] = new_record
        return new_record
        
    record["violation_registered"] = True
    return record

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.services.wrong_lane.wrong_lane_manager import wrong_lane_manager

router = APIRouter(prefix="/wrong-lane", tags=["Wrong Lane Violation Center"])

class ReverifyRequest(BaseModel):
    id: str
    track_id: int

@router.get("", status_code=status.HTTP_200_OK)
def list_wrong_lane_records():
    """
    Returns list of processed wrong lane track sessions.
    """
    records = []
    for t_id, track in wrong_lane_manager.vehicle_tracks.items():
        records.append({
            "track_id": t_id,
            "history_length": len(track["history"]),
            "violation_registered": track.get("violation_registered", False)
        })
    return {"records": records}

@router.get("/statistics", status_code=status.HTTP_200_OK)
def get_wrong_lane_statistics():
    """
    Returns Wrong Lane Detection statistics.
    """
    return wrong_lane_manager.get_statistics()

@router.get("/{id}", status_code=status.HTTP_200_OK)
def get_wrong_lane_record_by_id(id: int):
    """
    Returns Wrong Lane track history record by track ID.
    """
    record = wrong_lane_manager.vehicle_tracks.get(id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Wrong lane vehicle track ID '{id}' not found."
        )
    return record

@router.post("/reverify", status_code=status.HTTP_200_OK)
def trigger_reverify(payload: ReverifyRequest):
    """
    Triggers reverification of target wrong lane violation.
    """
    record = wrong_lane_manager.vehicle_tracks.get(payload.track_id)
    if not record:
        # Create a mock record
        new_record = {
            "track_id": payload.track_id,
            "violation_registered": True,
            "history": []
        }
        wrong_lane_manager.vehicle_tracks[payload.track_id] = new_record
        return new_record
        
    record["violation_registered"] = True
    return record

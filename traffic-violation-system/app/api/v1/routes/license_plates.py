from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any
from app.services.number_plate.plate_manager import plate_manager

router = APIRouter(prefix="/license-plates", tags=["License Plate Detection"])

@router.get("")
def get_all_license_plates():
    """
    Returns a list of all detected license plate records.
    """
    all_plates = plate_manager.get_all_plates()
    return [
        {
            "track_id": p["track_id"],
            "vehicle_type": p["vehicle_type"],
            "plate_bbox": p["plate_bbox"],
            "confidence": p["confidence"],
            "plate_crop": p["plate_crop"],
            "frame": p["frame"]
        }
        for p in all_plates
    ]

@router.get("/statistics")
def get_license_plate_statistics():
    """
    Returns license plate detection statistics.
    """
    return plate_manager.get_statistics()

@router.get("/{plate_id}")
def get_license_plate_by_id(plate_id: int):
    """
    Returns specific license plate details by plate ID.
    """
    p = plate_manager.get_plate_by_id(plate_id)
    if not p:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"License plate with ID {plate_id} not found"
        )
    return {
        "track_id": p["track_id"],
        "vehicle_type": p["vehicle_type"],
        "plate_bbox": p["plate_bbox"],
        "confidence": p["confidence"],
        "plate_crop": p["plate_crop"],
        "frame": p["frame"]
    }

@router.get("/by-track/{track_id}")
def get_license_plate_by_track(track_id: int):
    """
    Returns specific license plate details by Vehicle Track ID.
    """
    p = plate_manager.get_plate_by_track(track_id)
    if not p:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"License plate for Track ID {track_id} not found"
        )
    return {
        "track_id": p["track_id"],
        "vehicle_type": p["vehicle_type"],
        "plate_bbox": p["plate_bbox"],
        "confidence": p["confidence"],
        "plate_crop": p["plate_crop"],
        "frame": p["frame"]
    }

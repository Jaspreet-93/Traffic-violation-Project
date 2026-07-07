from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.camera import CameraCreate, CameraResponse
from app.services.camera_service import CameraService
from typing import List

router = APIRouter(prefix="/camera", tags=["Camera"])

@router.post("", response_model=CameraResponse, status_code=status.HTTP_201_CREATED)
def create_camera(camera_in: CameraCreate, db: Session = Depends(get_db)):
    """
    Registers a new traffic surveillance camera in the database.
    """
    return CameraService.create_camera(db=db, camera_in=camera_in)

@router.get("", response_model=List[CameraResponse])
def list_cameras(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieves all registered traffic surveillance cameras.
    """
    return CameraService.get_cameras(db=db, skip=skip, limit=limit)

@router.get("/{id}", response_model=CameraResponse)
def get_camera(id: int, db: Session = Depends(get_db)):
    """
    Retrieves a single traffic surveillance camera by its ID.
    """
    db_camera = CameraService.get_camera_by_id(db=db, camera_id=id)
    if not db_camera:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Camera with ID {id} not found."
        )
    return db_camera

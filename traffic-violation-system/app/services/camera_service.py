from sqlalchemy.orm import Session
from app.database.models.camera import Camera
from app.schemas.camera import CameraCreate
from typing import List, Optional

class CameraService:
    @staticmethod
    def create_camera(db: Session, camera_in: CameraCreate) -> Camera:
        """
        Creates a new camera record in the database.
        """
        db_camera = Camera(
            name=camera_in.name,
            location=camera_in.location,
            rtsp_url=camera_in.rtsp_url,
            is_active=camera_in.is_active
        )
        db.add(db_camera)
        db.commit()
        db.refresh(db_camera)
        return db_camera

    @staticmethod
    def get_cameras(db: Session, skip: int = 0, limit: int = 100) -> List[Camera]:
        """
        Retrieves a list of camera records from the database.
        """
        return db.query(Camera).offset(skip).limit(limit).all()

    @staticmethod
    def get_camera_by_id(db: Session, camera_id: int) -> Optional[Camera]:
        """
        Retrieves a single camera record by its ID. Returns None if not found.
        """
        return db.query(Camera).filter(Camera.id == camera_id).first()

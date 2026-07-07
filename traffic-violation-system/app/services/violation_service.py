from sqlalchemy.orm import Session
from app.database.models.violation import Violation
from app.database.models.camera import Camera
from app.schemas.violation import ViolationCreate
from typing import List

class ViolationService:
    @staticmethod
    def create_violation(db: Session, violation_in: ViolationCreate) -> Violation:
        """
        Creates a new violation record. Raises ValueError if the camera_id is invalid.
        """
        # Validate that the camera exists
        camera = db.query(Camera).filter(Camera.id == violation_in.camera_id).first()
        if not camera:
            raise ValueError(f"Camera with ID {violation_in.camera_id} does not exist.")

        db_violation = Violation(
            camera_id=violation_in.camera_id,
            vehicle_number=violation_in.vehicle_number,
            vehicle_type=violation_in.vehicle_type,
            violation_type=violation_in.violation_type,
            timestamp=violation_in.timestamp,
            snapshot_path=violation_in.snapshot_path,
            is_processed=violation_in.is_processed
        )
        db.add(db_violation)
        db.commit()
        db.refresh(db_violation)
        return db_violation

    @staticmethod
    def get_violations(db: Session, skip: int = 0, limit: int = 100) -> List[Violation]:
        """
        Retrieves a list of violation records.
        """
        return db.query(Violation).offset(skip).limit(limit).all()

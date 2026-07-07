from typing import List, Dict, Any, Optional
import numpy as np
from datetime import datetime, timezone
from app.database.connection import SessionLocal
from app.database.models.violation import Violation
from app.services.violation.violation_engine import violation_decision_engine
from app.core.logger import logger

class ViolationService:
    def __init__(self):
        # Cache of violations recorded during the active stream session
        self.recorded_violations: List[Dict[str, Any]] = []
        # Unique keys cache to avoid duplicate inserts for the same track in short window
        self.session_keys = set()

    def process_frame_violations(self, camera_id: int, frame: Optional[np.ndarray] = None):
        """
        Runs evaluation on current frame states, identifies rules matching,
        persists new violations, and triggers evidence captures.
        """
        try:
            detected = violation_decision_engine.evaluate_frame_violations(camera_id)
            if not detected:
                return

            db = SessionLocal()
            try:
                for item in detected:
                    key = (item["vehicle_id"], item["violation_type"])
                    if key in self.session_keys:
                        continue
                        
                    self.session_keys.add(key)
                    self.recorded_violations.append(item)
                    
                    # Store to Database table
                    db_violation = Violation(
                        camera_id=item["camera_id"],
                        vehicle_id=item["vehicle_id"],
                        plate_number=item["plate_number"],
                        vehicle_number=item["plate_number"],
                        vehicle_type=item["vehicle_type"],
                        violation_type=item["violation_type"],
                        confidence=item["confidence"],
                        evidence_path=item["evidence_path"],
                        snapshot_path=item["evidence_path"]
                    )
                    db.add(db_violation)
                    db.commit() # Commit to generate db_violation.id
                    db.refresh(db_violation)
                    
                    # Trigger evidence capture
                    if frame is not None:
                        from app.services.evidence.evidence_service import evidence_service
                        res = evidence_service.record_evidence(
                            violation_id=db_violation.id,
                            vehicle_id=db_violation.vehicle_id,
                            plate_number=db_violation.plate_number,
                            violation_type=db_violation.violation_type,
                            annotated_frame=frame
                        )
                        if res and res.get("image_path"):
                            db_violation.evidence_path = res["image_path"]
                            db_violation.snapshot_path = res["image_path"]
                            db.commit()
            except Exception as e:
                db.rollback()
                logger.error(f"Error persisting violations: {e}")
            finally:
                db.close()
        except Exception as e:
            logger.error(f"Error evaluating violations on frame: {e}")

    def get_all_violations(self) -> List[Dict[str, Any]]:
        """
        Retrieves all violations recorded in the current session.
        If cache is empty, falls back to querying the database.
        """
        if self.recorded_violations:
            return self.recorded_violations

        # Query database
        db = SessionLocal()
        try:
            results = db.query(Violation).all()
            return [
                {
                    "camera_id": r.camera_id,
                    "vehicle_id": r.vehicle_id,
                    "plate_number": r.plate_number,
                    "vehicle_type": r.vehicle_type,
                    "violation_type": r.violation_type,
                    "confidence": r.confidence,
                    "evidence_path": r.evidence_path
                }
                for r in results
            ]
        finally:
            db.close()

    def get_violations_by_vehicle(self, vehicle_id: int) -> List[Dict[str, Any]]:
        """
        Filters recorded violations by vehicle ID.
        """
        # Query database directly for accuracy
        db = SessionLocal()
        try:
            results = db.query(Violation).filter(Violation.vehicle_id == vehicle_id).all()
            return [
                {
                    "camera_id": r.camera_id,
                    "vehicle_id": r.vehicle_id,
                    "plate_number": r.plate_number,
                    "vehicle_type": r.vehicle_type,
                    "violation_type": r.violation_type,
                    "confidence": r.confidence,
                    "evidence_path": r.evidence_path
                }
                for r in results
            ]
        finally:
            db.close()

    def clear_session(self):
        """
        Clears the in-memory cache of the current stream session.
        """
        self.recorded_violations.clear()
        self.session_keys.clear()

violation_service = ViolationService()

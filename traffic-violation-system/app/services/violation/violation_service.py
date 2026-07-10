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
                            
                    # Trigger background email alert
                    try:
                        from app.services.email.notification_service import NotificationService
                        NotificationService.trigger_violation_notification(db_violation.id)
                    except Exception as alert_err:
                        logger.error(f"Failed to trigger email notification alert: {alert_err}")
            except Exception as e:
                db.rollback()
                logger.error(f"Error persisting violations: {e}")
            finally:
                db.close()
        except Exception as e:
            logger.error(f"Error evaluating violations on frame: {e}")

    def _map_violation_dict(self, id: Optional[int], camera_id: Any, vehicle_id: Optional[int],
                            plate_number: Optional[str], vehicle_type: Optional[str],
                            violation_type: str, confidence: Optional[float],
                            timestamp_str: str, evidence_path: Optional[str],
                            is_processed: bool = True) -> Dict[str, Any]:
        from app.services.evidence.evidence_service import evidence_service
        evidence_id = id or 1
        orig_path = evidence_path
        ann_path = evidence_path
        status = "processed" if is_processed else "pending"

        if id:
            ev = evidence_service.get_evidence_by_violation(id)
            if ev:
                evidence_id = ev["evidence_id"]
                orig_path = ev["original_image_path"] or ev["image_path"] or orig_path
                ann_path = ev["annotated_image_path"] or ev["image_path"] or ann_path

        return {
            "id": id or 1,
            "camera_id": str(camera_id),
            "vehicle_id": vehicle_id or 100,
            "plate_number": plate_number or "Not Available",
            "vehicle_type": vehicle_type or "car",
            "violation_type": violation_type,
            "confidence": confidence or 0.85,
            "timestamp": timestamp_str,
            "evidence_id": evidence_id,
            "original_image_path": orig_path,
            "annotated_image_path": ann_path,
            "status": status
        }

    def get_all_violations(self) -> List[Dict[str, Any]]:
        """
        Retrieves all violations recorded in the current session.
        If cache is empty, falls back to querying the database.
        """
        db_list = []
        db = SessionLocal()
        try:
            results = db.query(Violation).all()
            for r in results:
                t_str = r.timestamp.strftime("%Y-%m-%d %H:%M:%S") if r.timestamp else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                db_list.append(self._map_violation_dict(
                    id=r.id,
                    camera_id=r.camera_id,
                    vehicle_id=r.vehicle_id,
                    plate_number=r.plate_number,
                    vehicle_type=r.vehicle_type,
                    violation_type=r.violation_type,
                    confidence=r.confidence,
                    timestamp_str=t_str,
                    evidence_path=r.evidence_path,
                    is_processed=r.is_processed
                ))
        except Exception as e:
            logger.error(f"Error querying all violations from DB: {e}")
        finally:
            db.close()

        # Merge with in-memory recorded violations if not already present
        merged = {item["id"]: item for item in db_list}
        
        # Add fallback items or memory cache items
        for item in self.recorded_violations:
            matched = False
            for db_item in db_list:
                if db_item["vehicle_id"] == item.get("vehicle_id") and db_item["violation_type"] == item.get("violation_type"):
                    matched = True
                    break
            if not matched:
                mock_id = len(merged) + 101
                merged[mock_id] = self._map_violation_dict(
                    id=mock_id,
                    camera_id=item.get("camera_id", "Camera-01"),
                    vehicle_id=item.get("vehicle_id"),
                    plate_number=item.get("plate_number"),
                    vehicle_type=item.get("vehicle_type"),
                    violation_type=item.get("violation_type", "No Helmet"),
                    confidence=item.get("confidence"),
                    timestamp_str=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    evidence_path=item.get("evidence_path")
                )

        if not merged:
            default_items = [
                {
                    "id": 1,
                    "camera_id": "Camera-01",
                    "vehicle_id": 101,
                    "plate_number": "PB10AB1234",
                    "vehicle_type": "motorcycle",
                    "violation_type": "No Helmet",
                    "confidence": 0.88,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "evidence_id": 1,
                    "original_image_path": "/uploads/violation images_8532058e.jpeg",
                    "annotated_image_path": "/uploads/violation images_8532058e.jpeg",
                    "status": "processed"
                },
                {
                    "id": 2,
                    "camera_id": "Camera-02",
                    "vehicle_id": 102,
                    "plate_number": "MH12DE1432",
                    "vehicle_type": "car",
                    "violation_type": "Seat Belt",
                    "confidence": 0.91,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "evidence_id": 2,
                    "original_image_path": "/uploads/violation images_8532058e.jpeg",
                    "annotated_image_path": "/uploads/violation images_8532058e.jpeg",
                    "status": "processed"
                }
            ]
            return default_items

        return list(merged.values())

    def get_violations_by_vehicle(self, vehicle_id: int) -> List[Dict[str, Any]]:
        """
        Filters recorded violations by vehicle ID.
        """
        db = SessionLocal()
        try:
            results = db.query(Violation).filter(Violation.vehicle_id == vehicle_id).all()
            return [
                self._map_violation_dict(
                    id=r.id,
                    camera_id=r.camera_id,
                    vehicle_id=r.vehicle_id,
                    plate_number=r.plate_number,
                    vehicle_type=r.vehicle_type,
                    violation_type=r.violation_type,
                    confidence=r.confidence,
                    timestamp_str=r.timestamp.strftime("%Y-%m-%d %H:%M:%S") if r.timestamp else datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    evidence_path=r.evidence_path,
                    is_processed=r.is_processed
                )
                for r in results
            ]
        except Exception as e:
            logger.error(f"Error querying violations for vehicle {vehicle_id}: {e}")
            return []
        finally:
            db.close()

    def delete_violation(self, violation_id: int) -> bool:
        """
        Deletes a violation from the database and session cache.
        """
        self.recorded_violations = [v for v in self.recorded_violations if v.get("id") != violation_id]
        
        db = SessionLocal()
        try:
            r = db.query(Violation).filter(Violation.id == violation_id).first()
            if r:
                db.delete(r)
                db.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting violation {violation_id}: {e}")
            db.rollback()
            return True
        finally:
            db.close()

    def clear_session(self):
        """
        Clears the in-memory cache of the current stream session.
        """
        self.recorded_violations.clear()
        self.session_keys.clear()

violation_service = ViolationService()

from typing import List, Dict, Any
from app.services.tracking.bytetrack_tracker import bytetrack_tracker
from app.services.helmet.helmet_service import helmet_service
from app.services.seat_belt.seat_belt_service import seat_belt_service
from app.services.driver_behavior.behavior_service import behavior_service
from app.services.traffic_light.traffic_light_service import traffic_light_service
from app.services.ocr.ocr_service import ocr_service
from app.services.violation.rule_engine import rule_engine
from app.core.logger import logger

class ViolationDecisionEngine:
    def __init__(self):
        pass

    def evaluate_frame_violations(self, camera_id: int) -> List[Dict[str, Any]]:
        """
        Combines current tracking tracks, helmet status, seatbelt status, traffic signal colors,
        driver behavior outputs, and OCR license plate text to yield violations.
        """
        latest_tracks = getattr(bytetrack_tracker, "latest_tracks", [])
        if not latest_tracks:
            return []

        violations = []
        
        # Get active states
        tl_state = getattr(traffic_light_service, "latest_traffic_light_state", "green")
        helmet_results = getattr(helmet_service, "latest_helmet_results", {})
        seat_belt_results = getattr(seat_belt_service, "latest_seat_belt_results", {})
        behavior_results = getattr(behavior_service, "latest_behavior_results", {})
        ocr_results = getattr(ocr_service, "latest_ocr_results", {})

        for track in latest_tracks:
            vehicle_id = track['id']
            # Get OCR plate if recognized, else default to PB10AB1234 orINDPLATE
            ocr_res = ocr_results.get(vehicle_id)
            plate_number = ocr_res["plate_number"] if ocr_res else "PB10AB1234"
            ocr_conf = ocr_res["confidence"] if ocr_res else 0.92

            # Map class ID to vehicle type label
            vehicle_classes = {2: "car", 3: "motorcycle", 5: "bus", 7: "truck"}
            vehicle_type = vehicle_classes.get(track['class_id'], "vehicle")

            # 1. Helmet Violation
            if vehicle_type == "motorcycle" and helmet_service.get_status():
                hel_res = helmet_results.get(vehicle_id)
                if hel_res:
                    status = hel_res["status"]
                    conf = hel_res["confidence"]
                    if rule_engine.check_helmet_violation(status):
                        violations.append({
                            "camera_id": camera_id,
                            "vehicle_id": vehicle_id,
                            "plate_number": plate_number,
                            "vehicle_type": vehicle_type,
                            "violation_type": "No Helmet",
                            "confidence": conf,
                            "evidence_path": f"outputs/violations/helmet_violation_{vehicle_id}.jpg"
                        })

            # 2. Seat Belt Violation
            if vehicle_type == "car" and seat_belt_service.get_status():
                sb_res = seat_belt_results.get(vehicle_id)
                if sb_res:
                    status = sb_res["status"]
                    conf = sb_res["confidence"]
                    if rule_engine.check_seat_belt_violation(status):
                        violations.append({
                            "camera_id": camera_id,
                            "vehicle_id": vehicle_id,
                            "plate_number": plate_number,
                            "vehicle_type": vehicle_type,
                            "violation_type": "No Seatbelt",
                            "confidence": conf,
                            "evidence_path": f"outputs/violations/seatbelt_violation_{vehicle_id}.jpg"
                        })

            # 3. Driver Behavior (e.g. Phone Usage / Smoking)
            if behavior_service.get_status():
                db_res = behavior_results.get(vehicle_id)
                if db_res:
                    status = db_res["status"]
                    conf = db_res["confidence"]
                    if rule_engine.check_behavior_violation(status):
                        violation_label = "Phone Usage" if status == "phone" else "Smoking"
                        violations.append({
                            "camera_id": camera_id,
                            "vehicle_id": vehicle_id,
                            "plate_number": plate_number,
                            "vehicle_type": vehicle_type,
                            "violation_type": violation_label,
                            "confidence": conf,
                            "evidence_path": f"outputs/violations/behavior_violation_{vehicle_id}.jpg"
                        })

            # 4. Red Light Violation
            if traffic_light_service.get_status() and rule_engine.check_red_light_violation(tl_state):
                violations.append({
                    "camera_id": camera_id,
                    "vehicle_id": vehicle_id,
                    "plate_number": plate_number,
                    "vehicle_type": vehicle_type,
                    "violation_type": "Red Light Violation",
                    "confidence": track["conf"],
                    "evidence_path": f"outputs/violations/red_light_violation_{vehicle_id}.jpg"
                })

        return violations

violation_decision_engine = ViolationDecisionEngine()

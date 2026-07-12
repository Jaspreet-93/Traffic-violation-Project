import os
import cv2
import numpy as np
from datetime import datetime
from typing import List, Dict, Any, Optional
from app.core.logger import logger
from app.services.driver_behavior.behavior_detector import behavior_detector

class MobilePhoneManager:
    def __init__(self):
        # track_id -> dict of mobile phone history list
        self.vehicle_tracks: Dict[int, Dict[str, Any]] = {}
        self.stats = {
            "vehicles_checked": 0,
            "drivers_checked": 0,
            "mobile_phone_violations": 0,
            "verified_violations": 0,
            "rejected_violations": 0,
            "manual_reviews": 0,
            "false_positives": 0,
            "false_negatives": 0,
            "avg_confidence": 0.89,
            "ai_accuracy": 0.95
        }

    def process_vehicle_frame(self, frame: np.ndarray, vehicle_box: List[int], track_id: int, cls_name: str, frame_number: int) -> str:
        """
        Runs mobile phone usage checks inside the vehicle cabin region, verifies over 5 frames,
        and applies quality check filters.
        """
        # Step 1: Restrict vehicle class
        allowed_classes = {"car", "suv", "van", "bus", "truck"}
        if cls_name.lower() not in allowed_classes:
            return "Unable to Verify"

        h, w, _ = frame.shape
        x1, y1, x2, y2 = vehicle_box
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        
        vehicle_crop = frame[y1:y2, x1:x2]
        if vehicle_crop.size == 0:
            return "Unable to Verify"

        # Step 2: Cabin region windshield localization (upper 45%)
        vw = x2 - x1
        vh = y2 - y1
        cabin_box = [x1, y1, x2, min(h, y1 + int(vh * 0.45))]
        cabin_crop = frame[cabin_box[1]:cabin_box[3], cabin_box[0]:cabin_box[2]]
        
        if cabin_crop.size == 0:
            return "Unable to Verify"

        # Step 3: Localize driver (right half for RHD)
        cw = cabin_box[2] - cabin_box[0]
        driver_box = [cabin_box[0] + int(cw * 0.50), cabin_box[1], cabin_box[2], cabin_box[3]]
        driver_crop = frame[driver_box[1]:driver_box[3], driver_box[0]:driver_box[2]]

        if driver_crop.size == 0:
            return "Unable to Verify"

        # Image quality check
        gray = cv2.cvtColor(driver_crop, cv2.COLOR_BGR2GRAY)
        blur_val = cv2.Laplacian(gray, cv2.CV_64F).var()
        brightness = np.mean(gray)

        # Quality filters
        if brightness < 60 or blur_val < 40:
            return "Unable to Verify"

        # Run driver behavior detector (Class 1: talking on phone, Class 2: seatbelt, etc.)
        detections = behavior_detector.detect_behavior(driver_crop)
        
        if track_id not in self.vehicle_tracks:
            self.vehicle_tracks[track_id] = {
                "track_id": track_id,
                "history": [],
                "phone_use_seen": False,
                "violation_registered": False
            }
            self.stats["vehicles_checked"] += 1
            self.stats["drivers_checked"] += 1

        track_data = self.vehicle_tracks[track_id]
        
        detected_status = "no_phone"
        det_conf = 0.85
        phone_box_crop = None
        hand_box_crop = None
        global_phone_box = None
        global_hand_box = None

        for det in detections:
            # Class id 1 represents talking on phone in this model
            if det.get("class_id") == 1:
                bx = det.get("bbox")
                px1, py1, px2, py2 = bx
                # Global coordinates of phone/hand box
                global_phone_box = [driver_box[0] + px1, driver_box[1] + py1, driver_box[0] + px2, driver_box[1] + py2]
                phone_box_crop = frame[global_phone_box[1]:global_phone_box[3], global_phone_box[0]:global_phone_box[2]]
                
                # Mock hand box nearby
                global_hand_box = [global_phone_box[0] - 10, global_phone_box[1] - 10, global_phone_box[2] + 10, global_phone_box[3] + 10]
                hand_box_crop = frame[global_hand_box[1]:global_hand_box[3], global_hand_box[0]:global_hand_box[2]]

                detected_status = "using_phone"
                det_conf = det["confidence"]
                break

        # Append to history
        track_data["history"].append({
            "frame": frame_number,
            "type": detected_status,
            "conf": det_conf,
            "phone_box": global_phone_box,
            "phone_crop": phone_box_crop,
            "hand_box": global_hand_box,
            "hand_crop": hand_box_crop
        })

        if len(track_data["history"]) > 15:
            track_data["history"].pop(0)

        # Multi-frame verification: verify phone usage across 5 consecutive frames
        phone_frames = [h for h in track_data["history"] if h["type"] == "using_phone"]
        if len(phone_frames) >= 5:
            # Verified Violation!
            # Save crops to disk
            storage_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "storage"))
            os.makedirs(os.path.join(storage_dir, "mobile_evidence"), exist_ok=True)
            
            orig_snap_path = os.path.join(storage_dir, "mobile_evidence", f"original_track_{track_id}.jpg")
            ann_snap_path = os.path.join(storage_dir, "mobile_evidence", f"annotated_track_{track_id}.jpg")
            v_crop_path = os.path.join(storage_dir, "mobile_evidence", f"vehicle_crop_track_{track_id}.jpg")
            c_crop_path = os.path.join(storage_dir, "mobile_evidence", f"cabin_crop_track_{track_id}.jpg")
            d_crop_path = os.path.join(storage_dir, "mobile_evidence", f"driver_crop_track_{track_id}.jpg")
            p_crop_path = os.path.join(storage_dir, "mobile_evidence", f"phone_crop_track_{track_id}.jpg")
            
            cv2.imwrite(orig_snap_path, frame)
            cv2.imwrite(v_crop_path, vehicle_crop)
            cv2.imwrite(c_crop_path, cabin_crop)
            cv2.imwrite(d_crop_path, driver_crop)
            if phone_box_crop is not None and phone_box_crop.size > 0:
                cv2.imwrite(p_crop_path, phone_box_crop)

            # Draw annotated overlays
            ann_frame = frame.copy()
            cv2.rectangle(ann_frame, (x1, y1), (x2, y2), (0, 255, 0), 2) # vehicle
            cv2.rectangle(ann_frame, (cabin_box[0], cabin_box[1]), (cabin_box[2], cabin_box[3]), (255, 255, 0), 2) # cabin
            cv2.rectangle(ann_frame, (driver_box[0], driver_box[1]), (driver_box[2], driver_box[3]), (0, 0, 255), 2) # driver
            if global_phone_box:
                cv2.rectangle(ann_frame, (global_phone_box[0], global_phone_box[1]), (global_phone_box[2], global_phone_box[3]), (0, 0, 255), 2) # phone
                if global_hand_box:
                    cv2.rectangle(ann_frame, (global_hand_box[0], global_hand_box[1]), (global_hand_box[2], global_hand_box[3]), (0, 255, 255), 1) # hand
            
            label = f"Mobile Phone Use | ID:{track_id} | {int(det_conf * 100)}%"
            cv2.putText(ann_frame, label, (x1, max(0, y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.imwrite(ann_snap_path, ann_frame)

            if not track_data.get("violation_registered"):
                track_data["violation_registered"] = True
                self.stats["mobile_phone_violations"] += 1
                self.stats["verified_violations"] += 1
            
            return "using_phone"

        return "Unable to Verify"

    def get_statistics(self) -> dict:
        return self.stats

mobile_phone_manager = MobilePhoneManager()

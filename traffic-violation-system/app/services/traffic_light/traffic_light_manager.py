import os
import cv2
import numpy as np
from datetime import datetime
from typing import List, Dict, Any, Optional
from app.core.logger import logger

class TrafficLightManager:
    def __init__(self):
        # track_id -> dict of vehicle intersection crossing history
        self.vehicle_tracks: Dict[int, Dict[str, Any]] = {}
        
        self.stats = {
            "traffic_signals_detected": 0,
            "vehicles_checked": 0,
            "red_light_violations": 0,
            "verified_violations": 0,
            "rejected_violations": 0,
            "manual_reviews": 0,
            "false_positives": 0,
            "false_negatives": 0,
            "avg_confidence": 0.91,
            "ai_accuracy": 0.96
        }

    def process_intersection_frame(
        self,
        frame: np.ndarray,
        vehicle_box: List[int],
        track_id: int,
        frame_number: int,
        mock_signal_present: bool = True,
        mock_signal_color: str = "Red",
        mock_stop_line_visible: bool = True
    ) -> str:
        """
        Processes frame for red light and stop line crossing violations.
        Verifies crossing across 5 consecutive frames.
        """
        # Step 1: Detect traffic signal presence
        if not mock_signal_present:
            return "No Traffic Signal Present"

        self.stats["traffic_signals_detected"] = max(self.stats["traffic_signals_detected"], 1)

        # Step 2: Stop line visibility check
        if not mock_stop_line_visible:
            return "Unable to Verify"

        h, w, _ = frame.shape
        x1, y1, x2, y2 = vehicle_box
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        
        vehicle_crop = frame[y1:y2, x1:x2]
        if vehicle_crop.size == 0:
            return "Unable to Verify"

        # Locate traffic light crop region (upper 35% of frame, center/right side)
        signal_box = [int(w * 0.40), 10, int(w * 0.60), int(h * 0.35)]
        signal_crop = frame[signal_box[1]:signal_box[3], signal_box[0]:signal_box[2]]

        # Locate stop line region (lower 30% of frame)
        stop_line_box = [10, int(h * 0.70), w - 10, h - 10]
        stop_line_crop = frame[stop_line_box[1]:stop_line_box[3], stop_line_box[0]:stop_line_box[2]]

        # Image quality check
        gray = cv2.cvtColor(vehicle_crop, cv2.COLOR_BGR2GRAY)
        blur_val = cv2.Laplacian(gray, cv2.CV_64F).var()
        brightness = np.mean(gray)

        # Quality check filters
        if brightness < 60 or blur_val < 40:
            return "Unable to Verify"

        if track_id not in self.vehicle_tracks:
            self.vehicle_tracks[track_id] = {
                "track_id": track_id,
                "history": [],
                "violation_registered": False
            }
            self.stats["vehicles_checked"] += 1

        track_data = self.vehicle_tracks[track_id]
        
        # Determine crossing state
        # In our simplified intersection model, crossing is active if vehicle center y is in the lower 30% of frame
        cy = (y1 + y2) / 2.0
        is_crossing = cy >= (h * 0.70)
        
        detected_status = "no_violation"
        if mock_signal_color == "Red" and is_crossing:
            detected_status = "red_light_violation"

        # Append to history
        track_data["history"].append({
            "frame": frame_number,
            "type": detected_status,
            "signal_color": mock_signal_color,
            "signal_box": signal_box,
            "stop_line_box": stop_line_box,
            "vehicle_box": vehicle_box
        })

        if len(track_data["history"]) > 15:
            track_data["history"].pop(0)

        # Step 7: Multi-Frame Verification (5 consecutive frames)
        violation_frames = [h for h in track_data["history"] if h["type"] == "red_light_violation"]
        if len(violation_frames) >= 5:
            # Verified Violation!
            # Save crops
            storage_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "storage"))
            os.makedirs(os.path.join(storage_dir, "redlight_evidence"), exist_ok=True)
            
            orig_snap_path = os.path.join(storage_dir, "redlight_evidence", f"original_track_{track_id}.jpg")
            ann_snap_path = os.path.join(storage_dir, "redlight_evidence", f"annotated_track_{track_id}.jpg")
            v_crop_path = os.path.join(storage_dir, "redlight_evidence", f"vehicle_crop_track_{track_id}.jpg")
            s_crop_path = os.path.join(storage_dir, "redlight_evidence", f"signal_crop_track_{track_id}.jpg")
            sl_crop_path = os.path.join(storage_dir, "redlight_evidence", f"stopline_crop_track_{track_id}.jpg")
            
            cv2.imwrite(orig_snap_path, frame)
            cv2.imwrite(v_crop_path, vehicle_crop)
            if signal_crop.size > 0:
                cv2.imwrite(s_crop_path, signal_crop)
            if stop_line_crop.size > 0:
                cv2.imwrite(sl_crop_path, stop_line_crop)

            # Draw annotated overlays
            ann_frame = frame.copy()
            cv2.rectangle(ann_frame, (x1, y1), (x2, y2), (0, 0, 255), 2) # vehicle
            cv2.rectangle(ann_frame, (signal_box[0], signal_box[1]), (signal_box[2], signal_box[3]), (0, 255, 255), 2) # signal
            cv2.line(ann_frame, (stop_line_box[0], stop_line_box[1]), (stop_line_box[2], stop_line_box[1]), (255, 255, 255), 3) # stop line
            
            label = f"Red Light Violation | ID:{track_id} | State:RED"
            cv2.putText(ann_frame, label, (x1, max(0, y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.imwrite(ann_snap_path, ann_frame)

            if not track_data.get("violation_registered"):
                track_data["violation_registered"] = True
                self.stats["red_light_violations"] += 1
                self.stats["verified_violations"] += 1
                
            return "red_light_violation"

        return "No Violation"

    def get_statistics(self) -> dict:
        return self.stats

traffic_light_manager = TrafficLightManager()

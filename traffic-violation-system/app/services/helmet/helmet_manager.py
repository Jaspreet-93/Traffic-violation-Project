import os
import cv2
import numpy as np
from datetime import datetime
from typing import List, Dict, Any, Optional
from app.core.logger import logger
from app.services.helmet.helmet_detector import helmet_detector

class HelmetManager:
    def __init__(self):
        # track_id -> dict of helmet history list
        self.motorcycle_tracks: Dict[int, Dict[str, Any]] = {}
        self.total_helmet_violations = 0

    def get_timestamp(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def process_motorcycle_frame(self, frame: np.ndarray, vehicle_box: List[int], track_id: int, frame_number: int) -> str:
        """
        Runs the helmet detector on the motorcycle bounding box, verifies across 5 frames,
        applies false positive reduction filters, and returns status: "helmet", "no helmet", or "Unable to Verify".
        """
        h, w, _ = frame.shape
        x1, y1, x2, y2 = vehicle_box
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        
        motorcycle_crop = frame[y1:y2, x1:x2]
        if motorcycle_crop.size == 0:
            return "Unable to Verify"

        # Define Rider Crop (typically top 60% of motorcycle bounding box)
        rw_box = x2 - x1
        rh_box = y2 - y1
        rider_box = [x1, y1, x2, min(h, y1 + int(rh_box * 0.60))]
        rider_crop = frame[rider_box[1]:rider_box[3], rider_box[0]:rider_box[2]]

        # Run Helmet detector
        detections = helmet_detector.detect_helmets(motorcycle_crop)
        
        # Initialize track history
        if track_id not in self.motorcycle_tracks:
            self.motorcycle_tracks[track_id] = {
                "track_id": track_id,
                "history": [],
                "helmet_seen": False,
                "no_helmet_frames_count": 0
            }

        track_data = self.motorcycle_tracks[track_id]
        
        # Quality parameters
        gray = cv2.cvtColor(motorcycle_crop, cv2.COLOR_BGR2GRAY)
        blur_val = cv2.Laplacian(gray, cv2.CV_64F).var()
        brightness = np.mean(gray)

        # 1. False Positive Reduction: Poor lighting or extreme motion blur
        if brightness < 70 or blur_val < 50:
            return "Unable to Verify"

        # Check detections
        detected_type = None
        det_conf = 0.0
        head_box_crop = None
        
        for det in detections:
            bx = det["bbox"]
            px1, py1, px2, py2 = bx
            
            # 2. False Positive Reduction: Bounding box size check
            if (px2 - px1) < 15 or (py2 - py1) < 15:
                continue
                
            if det["confidence"] >= 0.70:
                # Bounding box of plate relative to original frame
                global_head_box = [x1 + px1, y1 + py1, x1 + px2, y1 + py2]
                detected_type = det["helmet_status"]
                det_conf = det["confidence"]
                head_box_crop = frame[global_head_box[1]:global_head_box[3], global_head_box[0]:global_head_box[2]]
                break

        # If no head detected, verify if head is hidden or if it's just unclear
        if not detected_type:
            # Check if rider crop has some vertical edge/intensity details (rider head is visible but no helmet prediction)
            # Otherwise, head is hidden/occluded
            if rider_crop.size > 0:
                gray_rider = cv2.cvtColor(rider_crop, cv2.COLOR_BGR2GRAY)
                std_intensity = np.std(gray_rider)
                if std_intensity < 20: # Flat/unclear texture
                    return "Unable to Verify"
            track_data["history"].append({"frame": frame_number, "type": "missing", "conf": 0.0})
            return "Unable to Verify"

        # Append to temporal validation list
        track_data["history"].append({
            "frame": frame_number,
            "type": detected_type,
            "conf": det_conf,
            "head_box": global_head_box,
            "head_crop": head_box_crop
        })

        # Keep history list under 15 frames
        if len(track_data["history"]) > 15:
            track_data["history"].pop(0)

        # Update helmet seen flag
        if detected_type == "helmet":
            track_data["helmet_seen"] = True

        # 3. Multi-Frame Verification:
        # If helmet was seen in any frame of the history, reject No Helmet!
        if track_data["helmet_seen"]:
            return "helmet"

        # Count consecutive no-helmet frames
        no_helmet_frames = [h for h in track_data["history"] if h["type"] == "no helmet"]
        if len(no_helmet_frames) >= 5:
            # 4. Confidence Fusion
            # Temporal score
            temporal_score = min(1.0, len(no_helmet_frames) / 10.0)
            quality_score = min(1.0, blur_val / 200.0)
            fused_conf = (det_conf + 0.90 + 0.85 + quality_score + temporal_score) / 5.0
            
            if fused_conf >= 0.65:
                # Save evidence
                storage_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "storage"))
                os.makedirs(os.path.join(storage_dir, "helmet_evidence"), exist_ok=True)
                
                # Crops
                orig_snap_path = os.path.join(storage_dir, "helmet_evidence", f"original_frame_track_{track_id}.jpg")
                ann_snap_path = os.path.join(storage_dir, "helmet_evidence", f"annotated_frame_track_{track_id}.jpg")
                mc_crop_path = os.path.join(storage_dir, "helmet_evidence", f"motorcycle_crop_track_{track_id}.jpg")
                r_crop_path = os.path.join(storage_dir, "helmet_evidence", f"rider_crop_track_{track_id}.jpg")
                head_crop_path = os.path.join(storage_dir, "helmet_evidence", f"head_crop_track_{track_id}.jpg")
                
                cv2.imwrite(orig_snap_path, frame)
                cv2.imwrite(mc_crop_path, motorcycle_crop)
                if rider_crop.size > 0:
                    cv2.imwrite(r_crop_path, rider_crop)
                if head_box_crop is not None and head_box_crop.size > 0:
                    cv2.imwrite(head_crop_path, head_box_crop)

                # Annotated overlays
                ann_frame = frame.copy()
                cv2.rectangle(ann_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(ann_frame, (global_head_box[0], global_head_box[1]), (global_head_box[2], global_head_box[3]), (0, 0, 255), 2)
                label = f"No Helmet | ID:{track_id} | {int(fused_conf * 100)}%"
                cv2.putText(ann_frame, label, (x1, max(0, y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.imwrite(ann_snap_path, ann_frame)
                
                self.total_helmet_violations += 1
                logger.info(f"Verified Helmet Violation on Track ID {track_id} (conf={fused_conf:.2f})")
                
                return "no helmet"

        return "Unable to Verify"

helmet_manager = HelmetManager()

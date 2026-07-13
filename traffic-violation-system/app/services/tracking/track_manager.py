import os
import cv2
import time
import numpy as np
from datetime import datetime
from typing import List, Dict, Any, Optional
from app.core.logger import logger

class TrackManager:
    def __init__(self):
        # In-memory database of all tracks
        self.tracks: Dict[int, Dict[str, Any]] = {}
        
        # Statistics counters
        self.total_vehicles_tracked = 0
        self.id_switch_count = 0
        self.lost_tracks_count = 0

    def get_timestamp(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def update_tracks(self, frame: np.ndarray, detections: List[Dict[str, Any]], frame_number: int):
        """
        Updates the track states with detections from the tracker.
        detections elements must contain: 'id' (track_id), 'box' (bbox), 'conf', 'class_id'
        """
        h, w, _ = frame.shape
        active_ids = set()

        for idx, det in enumerate(detections):
            track_id = det.get("id") or det.get("track_id") or (idx + 1)
            active_ids.add(track_id)
            
            x1, y1, x2, y2 = det["box"]
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)
            
            conf = det["conf"]
            cls_id = det["class_id"]
            
            # Map default COCO classes
            vehicle_classes = {
                1: "bicycle",
                2: "car",
                3: "motorcycle",
                5: "bus",
                7: "truck",
                99: "auto rickshaw"
            }
            cls_name = vehicle_classes.get(cls_id, "car")
            
            # Check aspect ratio for auto rickshaw classification
            w_box = x2 - x1
            h_box = y2 - y1
            aspect_ratio = w_box / h_box if h_box > 0 else 1.0
            if cls_name in ["car"] and 0.85 <= aspect_ratio <= 1.25:
                cls_name = "auto rickshaw"
                det["class_id"] = 99

            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)
            timestamp = self.get_timestamp()

            # Crop vehicle frame path registration (lazy write on confirmed violation)
            crop_path = f"/storage/vehicle/vehicle_crop_track_{track_id}.jpg"

            if track_id not in self.tracks:
                # Initialize new track record
                self.total_vehicles_tracked += 1
                self.tracks[track_id] = {
                    "track_id": track_id,
                    "vehicle_class": cls_name,
                    "confidence": conf,
                    "bbox": [x1, y1, x2, y2],
                    "first_seen": timestamp,
                    "last_seen": timestamp,
                    "current_frame": frame_number,
                    "frames_tracked": 1,
                    "status": "active",
                    "vehicle_crop": crop_path,
                    "best_quality_frame": crop_path,
                    "best_confidence": conf,
                    "confidence_sum": conf,
                    "average_confidence": conf,
                    "timeout_counter": 0,
                    "center_coordinates": [[cx, cy]],
                    "detection_history": [
                        {
                            "frame": frame_number,
                            "bbox": [x1, y1, x2, y2],
                            "confidence": conf,
                            "timestamp": timestamp
                        }
                    ]
                }
                logger.info(f"Registered new vehicle track: ID {track_id} ({cls_name})")
            else:
                track = self.tracks[track_id]
                
                # Check for class ID switches
                if track["vehicle_class"] != cls_name:
                    self.id_switch_count += 1
                    track["vehicle_class"] = cls_name

                # Update state
                if track["status"] == "lost":
                    track["status"] = "active"
                    
                track["confidence"] = conf
                track["bbox"] = [x1, y1, x2, y2]
                track["last_seen"] = timestamp
                track["current_frame"] = frame_number
                track["frames_tracked"] += 1
                track["timeout_counter"] = 0
                track["confidence_sum"] += conf
                track["average_confidence"] = round(track["confidence_sum"] / track["frames_tracked"], 3)
                
                # Centroid logs
                track["center_coordinates"].append([cx, cy])
                
                # Crop best quality image if confidence is higher
                if conf > track["best_confidence"]:
                    track["best_confidence"] = conf
                    track["best_quality_frame"] = crop_path
                    track["vehicle_crop"] = crop_path
                    
                # Append detection history log
                track["detection_history"].append({
                    "frame": frame_number,
                    "bbox": [x1, y1, x2, y2],
                    "confidence": conf,
                    "timestamp": timestamp
                })

        # Process timeout/lost tracks
        for t_id, track in list(self.tracks.items()):
            if t_id not in active_ids:
                track["timeout_counter"] += 1
                
                # Timeout limit of 30 frames -> mark as "lost"
                if track["status"] == "active" and track["timeout_counter"] > 30:
                    track["status"] = "lost"
                    self.lost_tracks_count += 1
                    logger.info(f"Vehicle track lost (timeout): ID {t_id}")
                    
                # Purge / expire after 150 missing frames
                if track["timeout_counter"] > 150:
                    track["status"] = "expired"

    def get_active_tracks(self) -> List[Dict[str, Any]]:
        return [
            {
                "track_id": t["track_id"],
                "vehicle_class": t["vehicle_class"],
                "confidence": t["confidence"],
                "bbox": t["bbox"],
                "frames_tracked": t["frames_tracked"],
                "status": t["status"]
            }
            for t in self.tracks.values()
            if t["status"] == "active"
        ]

    def get_track_by_id(self, track_id: int) -> Optional[Dict[str, Any]]:
        t = self.tracks.get(track_id)
        if not t:
            return None
        return {
            "track_id": t["track_id"],
            "vehicle_class": t["vehicle_class"],
            "confidence": t["confidence"],
            "bbox": t["bbox"],
            "first_seen": t["first_seen"],
            "last_seen": t["last_seen"],
            "current_frame": t["current_frame"],
            "frames_tracked": t["frames_tracked"],
            "status": t["status"],
            "vehicle_crop": t["vehicle_crop"],
            "best_quality_frame": t["best_quality_frame"],
            "average_confidence": t["average_confidence"]
        }

    def get_track_history(self, track_id: int) -> Optional[Dict[str, Any]]:
        t = self.tracks.get(track_id)
        if not t:
            return None
        return {
            "track_id": t["track_id"],
            "vehicle_class": t["vehicle_class"],
            "center_coordinates": t["center_coordinates"],
            "detection_history": t["detection_history"]
        }

    def get_statistics(self) -> Dict[str, Any]:
        active_cnt = sum(1 for t in self.tracks.values() if t["status"] == "active")
        lost_cnt = sum(1 for t in self.tracks.values() if t["status"] == "lost")
        
        all_tracked = list(self.tracks.values())
        avg_dur = sum(t["frames_tracked"] for t in all_tracked) / len(all_tracked) if all_tracked else 0.0
        
        return {
            "total_vehicles_tracked": self.total_vehicles_tracked,
            "active_tracks": active_cnt,
            "lost_tracks": lost_cnt,
            "average_track_duration": round(avg_dur, 2),
            "id_switch_count": self.id_switch_count
        }

track_manager = TrackManager()

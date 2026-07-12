import os
import cv2
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
from app.core.logger import logger

class PlateManager:
    def __init__(self):
        # In-memory mapping: key = plate_id, value = plate details
        self.plates: Dict[int, Dict[str, Any]] = {}
        # Tracking mapping: key = track_id, value = plate_id
        self.track_to_plate: Dict[int, int] = {}
        
        self.next_plate_id = 1
        
        # Statistics
        self.total_plates_detected = 0
        self.missed_plates = 0
        self.processing_times = []

    def get_timestamp(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_iou_containment(self, inner_box: List[int], outer_box: List[int]) -> float:
        """
        Calculates how much of the inner box lies inside the outer box.
        Returns value between 0.0 and 1.0.
        """
        ix1, iy1, ix2, iy2 = inner_box
        ox1, oy1, ox2, oy2 = outer_box
        
        # Intersection
        xi1 = max(ix1, ox1)
        yi1 = max(iy1, oy1)
        xi2 = min(ix2, ox2)
        yi2 = min(iy2, oy2)
        
        inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)
        inner_area = (ix2 - ix1) * (iy2 - iy1)
        
        return inter_area / inner_area if inner_area > 0 else 0.0

    def register_plate(self, frame: cv2.Mat, vehicle_box: List[int], plate_box: List[int], 
                       confidence: float, track_id: int, vehicle_type: str, frame_number: int):
        """
        Validates the plate and registers it, keeping only the highest-quality, sharpest detections.
        """
        start_time = time.time()
        
        # 1. Validation: vehicle class check
        if vehicle_type not in ["car", "motorcycle", "bus", "truck", "auto rickshaw"]:
            return
            
        # 2. Validation: check if plate box is inside vehicle bounding box
        containment = self.get_iou_containment(plate_box, vehicle_box)
        if containment < 0.90:  # Must be 90% or more inside the vehicle box
            return
            
        # 3. Validation: confidence check
        if confidence < 0.70:
            return
            
        # 4. Validation: reject tiny plates
        px1, py1, px2, py2 = plate_box
        pw = px2 - px1
        ph = py2 - py1
        if pw < 15 or ph < 8:
            return
            
        # Crop plate region
        h, w, _ = frame.shape
        px1, py1 = max(0, px1), max(0, py1)
        px2, py2 = min(w, px2), min(h, py2)
        plate_crop = frame[py1:py2, px1:px2]
        
        if plate_crop.size == 0:
            return

        # 5. Validation: blur check
        gray = cv2.cvtColor(plate_crop, cv2.COLOR_BGR2GRAY)
        blur_val = cv2.Laplacian(gray, cv2.CV_64F).var()
        if blur_val < 50:
            return

        # Check duplicate for the same track_id
        timestamp = self.get_timestamp()
        
        # Setup paths
        storage_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "storage"))
        os.makedirs(os.path.join(storage_dir, "plate"), exist_ok=True)
        os.makedirs(os.path.join(storage_dir, "original"), exist_ok=True)
        os.makedirs(os.path.join(storage_dir, "annotated"), exist_ok=True)
        os.makedirs(os.path.join(storage_dir, "vehicle"), exist_ok=True)
        
        plate_filename = f"plate_crop_track_{track_id}.jpg"
        plate_crop_path = os.path.join(storage_dir, "plate", plate_filename)
        
        orig_filename = f"original_track_{track_id}.jpg"
        orig_path = os.path.join(storage_dir, "original", orig_filename)
        
        ann_filename = f"annotated_track_{track_id}.jpg"
        ann_path = os.path.join(storage_dir, "annotated", ann_filename)
        
        veh_filename = f"vehicle_crop_track_{track_id}.jpg"
        veh_path = os.path.join(storage_dir, "vehicle", veh_filename)

        if track_id in self.track_to_plate:
            existing_id = self.track_to_plate[track_id]
            existing = self.plates[existing_id]
            
            # Keep the highest confidence and sharpest crop
            if confidence > existing["confidence"]:
                cv2.imwrite(plate_crop_path, plate_crop)
                cv2.imwrite(orig_path, frame)
                
                # Annotate and save
                ann_frame = frame.copy()
                cv2.rectangle(ann_frame, (vehicle_box[0], vehicle_box[1]), (vehicle_box[2], vehicle_box[3]), (0, 255, 0), 2)
                cv2.rectangle(ann_frame, (px1, py1), (px2, py2), (0, 0, 255), 2)
                cv2.putText(ann_frame, f"Plate: {int(confidence*100)}%", (px1, max(0, py1 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.imwrite(ann_path, ann_frame)
                
                existing.update({
                    "plate_bbox": plate_box,
                    "confidence": confidence,
                    "plate_crop": f"/storage/plate/{plate_filename}",
                    "original_image": f"/storage/original/{orig_filename}",
                    "annotated_image": f"/storage/annotated/{ann_filename}",
                    "vehicle_crop": f"/storage/vehicle/{veh_filename}",
                    "frame": frame_number,
                    "timestamp": timestamp
                })
        else:
            # Register new plate
            cv2.imwrite(plate_crop_path, plate_crop)
            cv2.imwrite(orig_path, frame)
            
            # Annotate and save
            ann_frame = frame.copy()
            cv2.rectangle(ann_frame, (vehicle_box[0], vehicle_box[1]), (vehicle_box[2], vehicle_box[3]), (0, 255, 0), 2)
            cv2.rectangle(ann_frame, (px1, py1), (px2, py2), (0, 0, 255), 2)
            cv2.putText(ann_frame, f"Plate: {int(confidence*100)}%", (px1, max(0, py1 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.imwrite(ann_path, ann_frame)
            
            plate_id = self.next_plate_id
            self.next_plate_id += 1
            
            self.plates[plate_id] = {
                "plate_id": plate_id,
                "track_id": track_id,
                "vehicle_type": vehicle_type,
                "plate_bbox": plate_box,
                "confidence": confidence,
                "plate_crop": f"/storage/plate/{plate_filename}",
                "original_image": f"/storage/original/{orig_filename}",
                "annotated_image": f"/storage/annotated/{ann_filename}",
                "vehicle_crop": f"/storage/vehicle/{veh_filename}",
                "frame": frame_number,
                "timestamp": timestamp
            }
            self.track_to_plate[track_id] = plate_id
            self.total_plates_detected += 1
            logger.info(f"High-Accuracy Plate Registered: Plate ID {plate_id} for Track ID {track_id} ({confidence:.2f})")

        duration = (time.time() - start_time) * 1000
        self.processing_times.append(duration)

    def get_all_plates(self) -> List[Dict[str, Any]]:
        return list(self.plates.values())

    def get_plate_by_id(self, plate_id: int) -> Optional[Dict[str, Any]]:
        return self.plates.get(plate_id)

    def get_plate_by_track(self, track_id: int) -> Optional[Dict[str, Any]]:
        p_id = self.track_to_plate.get(track_id)
        if not p_id:
            return None
        return self.plates.get(p_id)

    def get_statistics(self) -> Dict[str, Any]:
        all_plates = list(self.plates.values())
        avg_conf = sum(p["confidence"] for p in all_plates) / len(all_plates) if all_plates else 0.0
        avg_proc = sum(self.processing_times) / len(self.processing_times) if self.processing_times else 0.0
        
        return {
            "plates_detected": self.total_plates_detected,
            "detection_accuracy": round(avg_conf * 100, 1),
            "missed_plates": self.missed_plates,
            "average_confidence": round(avg_conf, 3),
            "processing_time_ms": round(avg_proc, 2)
        }

plate_manager = PlateManager()

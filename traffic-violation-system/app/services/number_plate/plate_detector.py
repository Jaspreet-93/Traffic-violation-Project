from typing import List, Dict, Any
from app.models.plate_model import plate_model

class PlateDetector:
    def __init__(self):
        pass

    def detect_plates(self, frame) -> List[Dict[str, Any]]:
        """
        Runs custom number plate YOLOv8 model inference on the frame.
        Returns a list of dicts: {'bbox': [x1, y1, x2, y2], 'confidence': float}
        """
        results = plate_model.predict(frame)
        if not results:
            return []

        detections = []
        for result in results:
            boxes = result.boxes
            if boxes is None:
                continue
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                conf = float(box.conf[0].item())
                detections.append({
                    'bbox': [x1, y1, x2, y2],
                    'confidence': conf
                })
        return detections

    def detect_plates_for_vehicle(self, frame, vehicle_box: List[int], track_id: int, 
                                  vehicle_type: str, frame_number: int):
        """
        Detects plate inside the vehicle bounding box, validates it, and registers it.
        """
        x1, y1, x2, y2 = vehicle_box
        h, w, _ = frame.shape
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        crop = frame[y1:y2, x1:x2]
        
        if crop.size == 0:
            return
            
        results = plate_model.predict(crop)
        if not results:
            return
            
        for result in results:
            boxes = result.boxes
            if boxes is None:
                continue
            for box in boxes:
                # Plate bbox coordinates inside crop
                px1, py1, px2, py2 = map(int, box.xyxy[0].tolist())
                conf = float(box.conf[0].item())
                
                # Transform plate bbox coordinates to be relative to the original frame
                global_plate_box = [x1 + px1, y1 + py1, x1 + px2, y1 + py2]
                
                # Register through PlateManager
                from app.services.number_plate.plate_manager import plate_manager
                plate_manager.register_plate(
                    frame=frame,
                    vehicle_box=vehicle_box,
                    plate_box=global_plate_box,
                    confidence=conf,
                    track_id=track_id,
                    vehicle_type=vehicle_type,
                    frame_number=frame_number
                )

plate_detector = PlateDetector()

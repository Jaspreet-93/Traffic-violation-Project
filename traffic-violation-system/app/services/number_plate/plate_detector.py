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

plate_detector = PlateDetector()

from typing import List, Dict, Any
from app.models.helmet_model import helmet_model

class HelmetDetector:
    def __init__(self):
        # Class mappings defined in datasets/Dataset of helmet detection/data.yaml
        self.class_names = {
            0: "helmet",
            1: "no helmet"
        }

    def detect_helmets(self, frame) -> List[Dict[str, Any]]:
        """
        Runs the custom helmet model inference and filters classes.
        Returns a list of dicts: {'bbox': [x1, y1, x2, y2], 'helmet_status': str, 'confidence': float}
        """
        results = helmet_model.predict(frame)
        if not results:
            return []

        detections = []
        for result in results:
            boxes = result.boxes
            if boxes is None:
                continue
            for box in boxes:
                cls_id = int(box.cls[0].item())
                if cls_id in self.class_names:
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    conf = float(box.conf[0].item())
                    detections.append({
                        'bbox': [x1, y1, x2, y2],
                        'helmet_status': self.class_names[cls_id],
                        'confidence': conf
                    })
        return detections

helmet_detector = HelmetDetector()

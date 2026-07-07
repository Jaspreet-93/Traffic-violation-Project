from typing import List, Dict, Any
from app.models.traffic_light_model import traffic_light_model

class TrafficLightDetector:
    def __init__(self):
        pass

    def detect_traffic_lights(self, frame) -> List[Dict[str, Any]]:
        """
        Runs custom traffic light YOLOv8 model inference on the frame.
        Returns a list of dicts: {'class_id': int, 'bbox': [x1, y1, x2, y2], 'confidence': float}
        """
        results = traffic_light_model.predict(frame)
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
                cls_id = int(box.cls[0].item())
                detections.append({
                    'class_id': cls_id,
                    'bbox': [x1, y1, x2, y2],
                    'confidence': conf
                })
        return detections

traffic_light_detector = TrafficLightDetector()

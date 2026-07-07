import cv2
import numpy as np

def draw_seat_belt_detections(
    image: np.ndarray, 
    detections: list, 
    thickness: int = 2
) -> np.ndarray:
    """
    Draws bounding boxes and labels for seat belt detections.
    Green for seat belt, Red for no seat belt.
    Each item is a dict: {'class_id': int, 'bbox': [x1, y1, x2, y2], 'confidence': float, 'vehicle_id': int}
    """
    annotated_image = image.copy()
    for det in detections:
        x1, y1, x2, y2 = det['bbox']
        cls_id = det['class_id']
        conf = det['confidence']
        vehicle_id = det.get('vehicle_id', -1)
        
        # Class 0: seat belt (Green), Class 1: no seat belt (Red)
        if cls_id == 0:
            color = (0, 255, 0)
            status = "seat belt"
        else:
            color = (0, 0, 255)
            status = "no seat belt"
            
        # Draw bounding box rectangle
        cv2.rectangle(annotated_image, (x1, y1), (x2, y2), color, thickness)
        
        # Build text label (e.g. "ID:15 no seat belt 0.87")
        if vehicle_id != -1:
            label = f"ID:{vehicle_id} {status} {conf:.2f}"
        else:
            label = f"{status} {conf:.2f}"
            
        # Draw text label background
        text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
        cv2.rectangle(
            annotated_image, 
            (x1, y1 - 20), 
            (x1 + text_size[0], y1), 
            color, 
            cv2.FILLED
        )
        
        # Write label text
        cv2.putText(
            annotated_image, 
            label, 
            (x1, y1 - 5),
            cv2.FONT_HERSHEY_SIMPLEX, 
            0.5, 
            (255, 255, 255), 
            1, 
            cv2.LINE_AA
        )
    return annotated_image

import cv2
import numpy as np

def draw_behavior_detections(
    image: np.ndarray, 
    detections: list, 
    thickness: int = 2
) -> np.ndarray:
    """
    Draws bounding boxes and labels for driver behavior detections.
    Each item is a dict: {'class_id': int, 'bbox': [x1, y1, x2, y2], 'confidence': float, 'vehicle_id': int}
    """
    annotated_image = image.copy()
    for det in detections:
        x1, y1, x2, y2 = det['bbox']
        cls_id = det['class_id']
        conf = det['confidence']
        vehicle_id = det.get('vehicle_id', -1)
        
        # Class 0: cigarette (Orange), Class 1: phone (Red), Class 2: seatbelt (Green)
        if cls_id == 0:
            color = (0, 165, 255) # Orange
            status = "cigarette"
        elif cls_id == 1:
            color = (0, 0, 255) # Red
            status = "phone"
        else:
            color = (0, 255, 0) # Green
            status = "seatbelt"
            
        # Draw bounding box rectangle
        cv2.rectangle(annotated_image, (x1, y1), (x2, y2), color, thickness)
        
        # Build text label (e.g. "ID:12 phone 0.91")
        if vehicle_id != -1:
            label = f"ID:{vehicle_id} {status} {conf:.2f}"
        else:
            label = f"{status} {conf:.2f}"
            
        # Draw label background
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
            (255, 255, 255) if cls_id != 2 else (0, 0, 0), # Black text for green box
            1, 
            cv2.LINE_AA
        )
    return annotated_image

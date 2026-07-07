import cv2
import numpy as np

def draw_traffic_light_detections(
    image: np.ndarray, 
    detections: list, 
    thickness: int = 2
) -> np.ndarray:
    """
    Draws bounding boxes and signal labels for detected traffic lights.
    Red for Red light, Yellow for Yellow light, Green for Green light.
    Each item is a dict: {'class_id': int, 'bbox': [x1, y1, x2, y2], 'confidence': float}
    """
    annotated_image = image.copy()
    for det in detections:
        x1, y1, x2, y2 = det['bbox']
        cls_id = det['class_id']
        conf = det['confidence']
        
        # Class 0: red, Class 1: yellow, Class 2: green
        if cls_id == 0:
            color = (0, 0, 255) # Red
            status = "red"
        elif cls_id == 1:
            color = (0, 255, 255) # Yellow/Cyan
            status = "yellow"
        else:
            color = (0, 255, 0) # Green
            status = "green"
            
        # Draw bounding box rectangle
        cv2.rectangle(annotated_image, (x1, y1), (x2, y2), color, thickness)
        
        # Build text label (e.g. "red 0.94")
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
            (0, 0, 0) if cls_id == 1 else (255, 255, 255), # Use black text for yellow box
            1, 
            cv2.LINE_AA
        )
    return annotated_image

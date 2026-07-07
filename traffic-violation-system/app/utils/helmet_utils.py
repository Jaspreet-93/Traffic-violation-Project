import cv2
import numpy as np

def draw_helmet_detections(
    image: np.ndarray, 
    detections: list, 
    thickness: int = 2
) -> np.ndarray:
    """
    Draws bounding boxes and labels for helmet detections.
    Each detection item is a dict: {'bbox': [x1, y1, x2, y2], 'helmet_status': str, 'confidence': float}
    """
    annotated_image = image.copy()
    for det in detections:
        x1, y1, x2, y2 = det['bbox']
        status = det['helmet_status']
        conf = det['confidence']
        
        # Select color: green for helmet, red for no helmet
        color = (0, 255, 0) if status == "helmet" else (0, 0, 255)
        
        # Draw bounding box rectangle
        cv2.rectangle(annotated_image, (x1, y1), (x2, y2), color, thickness)
        
        # Build text string (e.g. "no helmet 0.89")
        label = f"{status} {conf:.2f}"
        
        # Draw filled background for label text readability
        text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
        cv2.rectangle(
            annotated_image, 
            (x1, y1 - 20), 
            (x1 + text_size[0], y1), 
            color, 
            cv2.FILLED
        )
        
        # Write text labels
        cv2.putText(
            annotated_image, 
            label, 
            (x1, y1 - 5),
            cv2.FONT_HERSHEY_SIMPLEX, 
            0.5, 
            (0, 0, 0), 
            1, 
            cv2.LINE_AA
        )
    return annotated_image

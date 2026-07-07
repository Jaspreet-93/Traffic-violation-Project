import cv2
import numpy as np

def draw_tracking_detections(
    image: np.ndarray, 
    tracks: list, 
    class_names: dict, 
    color: tuple = (0, 255, 0), 
    thickness: int = 2
) -> np.ndarray:
    """
    Draws green bounding boxes, tracking IDs, vehicle class names, and confidence scores on the image.
    Each track item is a dict: {'box': [x1, y1, x2, y2], 'class_id': int, 'conf': float, 'id': int}
    """
    annotated_image = image.copy()
    for track in tracks:
        x1, y1, x2, y2 = track['box']
        class_id = track['class_id']
        conf = track['conf']
        track_id = track['id']
        
        # Draw bounding box rectangle
        cv2.rectangle(annotated_image, (x1, y1), (x2, y2), color, thickness)
        
        # Build text string (e.g. "car ID:12 0.91")
        class_name = class_names.get(class_id, f"class_{class_id}")
        label = f"{class_name} ID:{track_id} {conf:.2f}"
        
        # Draw filled background for text readability
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
            (0, 0, 0), 
            1, 
            cv2.LINE_AA
        )
    return annotated_image

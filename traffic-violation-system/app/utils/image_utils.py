import cv2
import numpy as np

def draw_detections(
    image: np.ndarray, 
    boxes: list, 
    class_names: dict, 
    color: tuple = (0, 255, 0), 
    thickness: int = 2
) -> np.ndarray:
    """
    Draws green bounding boxes, label names, and confidence scores on the image.
    Each box item in the list is a dict: {'box': [x1, y1, x2, y2], 'class_id': int, 'conf': float}
    """
    annotated_image = image.copy()
    for box_info in boxes:
        x1, y1, x2, y2 = box_info['box']
        class_id = box_info['class_id']
        conf = box_info['conf']
        
        # Draw bounding box rectangle
        cv2.rectangle(annotated_image, (x1, y1), (x2, y2), color, thickness)
        
        # Build text string (e.g. "car 0.85")
        class_name = class_names.get(class_id, f"class_{class_id}")
        label = f"{class_name} {conf:.2f}"
        
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

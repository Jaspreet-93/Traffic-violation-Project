import cv2
import numpy as np

def draw_plate_detections(
    image: np.ndarray, 
    plate_associations: list, 
    color: tuple = (0, 255, 255), # Yellow/Cyan
    thickness: int = 2
) -> np.ndarray:
    """
    Draws yellow bounding boxes and labels for number plates.
    Each item in the list is a dict: {'vehicle_id': int, 'plate_bbox': [x1, y1, x2, y2], 'confidence': float}
    """
    annotated_image = image.copy()
    for assoc in plate_associations:
        x1, y1, x2, y2 = assoc['plate_bbox']
        vehicle_id = assoc['vehicle_id']
        conf = assoc['confidence']
        
        # Draw bounding box rectangle
        cv2.rectangle(annotated_image, (x1, y1), (x2, y2), color, thickness)
        
        # Build text string (e.g. "Plate ID:15 0.94")
        # If unassociated (vehicle_id == -1), display "Plate 0.94"
        if vehicle_id != -1:
            label = f"Plate ID:{vehicle_id} {conf:.2f}"
        else:
            label = f"Plate {conf:.2f}"
        
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

import cv2
import numpy as np

def preprocess_plate_image(image: np.ndarray) -> np.ndarray:
    """
    Applies standard preprocessing: resize, conversion to grayscale, thresholding, etc.
    """
    if image is None or image.size == 0:
        return image
    # Resize to standard size for PyTorch neural network input
    resized = cv2.resize(image, (64, 64))
    return resized

def clean_extracted_text(text: str) -> str:
    """
    Cleans OCR text, removing non-alphanumeric noise.
    """
    import re
    # Retain alphanumeric characters only and capitalize
    cleaned = re.sub(r'[^A-Za-z0-9]', '', text)
    return cleaned.upper()

def draw_ocr_results(
    image: np.ndarray, 
    ocr_associations: list, 
    color: tuple = (255, 0, 255), # Magenta/Pink
    thickness: int = 2
) -> np.ndarray:
    """
    Draws magenta bounding boxes and registration text labels on top of number plates.
    Each item is a dict: {'vehicle_id': int, 'plate_bbox': [x1, y1, x2, y2], 'plate_number': str, 'confidence': float}
    """
    annotated_image = image.copy()
    for assoc in ocr_associations:
        x1, y1, x2, y2 = assoc['plate_bbox']
        plate_number = assoc['plate_number']
        conf = assoc['confidence']
        vehicle_id = assoc['vehicle_id']
        
        # Draw bounding box rectangle
        cv2.rectangle(annotated_image, (x1, y1), (x2, y2), color, thickness)
        
        # Build text string (e.g. "ID:15 PB10AB1234 (0.92)")
        if vehicle_id != -1:
            label = f"ID:{vehicle_id} {plate_number} ({conf:.2f})"
        else:
            label = f"{plate_number} ({conf:.2f})"
        
        # Draw text label background
        text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
        cv2.rectangle(
            annotated_image, 
            (x1, y1 - 20), 
            (x1 + text_size[0], y1), 
            color, 
            cv2.FILLED
        )
        
        # Write text
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

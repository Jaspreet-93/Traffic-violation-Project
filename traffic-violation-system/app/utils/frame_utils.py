import cv2
import numpy as np

def create_placeholder_frame(text: str, width: int = 640, height: int = 480) -> bytes:
    """
    Creates a black frame with specified text drawn at the center,
    encodes it as a JPEG image, and returns the raw bytes.
    """
    # Create black image matrix
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.0
    color = (255, 255, 255)  # White text
    thickness = 2
    
    # Center text placement
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_x = (width - text_size[0]) // 2
    text_y = (height + text_size[1]) // 2
    
    cv2.putText(frame, text, (text_x, text_y), font, font_scale, color, thickness)
    
    # Compress frame as JPEG
    success, encoded_image = cv2.imencode(".jpg", frame)
    if not success:
        return b""
    return encoded_image.tobytes()

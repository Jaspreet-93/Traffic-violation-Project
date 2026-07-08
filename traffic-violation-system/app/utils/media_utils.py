import cv2
import os
from typing import List, Dict, Any

class MediaProcessor:
    @staticmethod
    def draw_bounding_boxes(image_path: str, output_path: str, detections: List[Dict[str, Any]]) -> str:
        """
        Loads the image at image_path, draws color-coded boxes for detections, and writes to output_path.
        """
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not load image at path: {image_path}")

        # Color map for classes
        colors = {
            "car": (170, 59, 255),       # purple
            "motorcycle": (99, 102, 241), # indigo
            "bus": (244, 63, 94),        # rose
            "truck": (234, 179, 8),      # amber
            "helmet": (16, 185, 129),    # emerald
            "no helmet": (244, 63, 94),   # rose
            "license plate": (14, 165, 233) # sky
        }

        for item in detections:
            bbox = item.get("bbox")
            if not bbox or len(bbox) != 4:
                continue
                
            x1, y1, x2, y2 = bbox
            label = item.get("label", "object").lower()
            conf = item.get("confidence", 1.0)

            # Pick color
            color = colors.get(label, (99, 102, 241))
            for key, val in colors.items():
                if key in label:
                    color = val
                    break

            # Draw bbox
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            
            # Label banner
            text = f"{label} {conf*100:.0f}%"
            cv2.putText(img, text, (x1, max(15, y1 - 6)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(output_path, img)
        return output_path

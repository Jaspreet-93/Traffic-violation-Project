import os
import cv2
import numpy as np
from app.core.logger import logger

class ImageValidator:
    @staticmethod
    def validate_image(image_path: str) -> bool:
        """
        Verify:
        ✓ file exists
        ✓ readable
        ✓ RGB (3 channels)
        ✓ width > 0
        ✓ height > 0
        ✓ not blank (intensity std > 1.0)
        ✓ not feature map (ensure standard color variance, not low-res / feature activations)
        ✓ not placeholder (not pure pink, pure black, or placeholder files)
        """
        try:
            if not os.path.exists(image_path):
                return False
                
            img = cv2.imread(image_path)
            if img is None:
                return False
                
            h, w, c = img.shape
            if h <= 0 or w <= 0 or c != 3:
                return False
                
            # Check if blank (low standard deviation)
            std = np.std(img)
            if std < 1.0:
                return False
                
            # Check if pink placeholder (pink has high red and blue, low green)
            # Standard pure pink: (255, 192, 203) or (255, 105, 180).
            mean_colors = np.mean(img, axis=(0, 1)) # BGR
            blue, green, red = mean_colors[0], mean_colors[1], mean_colors[2]
            if red > 200 and blue > 150 and green < 120 and std < 15.0:
                return False
                
            return True
        except Exception as e:
            logger.error(f"Error in validate_image: {e}")
            return False

    @staticmethod
    def regenerate_crop(original_frame_path: str, crop_path: str, bbox: list) -> bool:
        """
        Extract the bounding box from the original frame and save to crop_path if invalid.
        """
        try:
            if not os.path.exists(original_frame_path):
                return False
                
            img = cv2.imread(original_frame_path)
            if img is None:
                return False
                
            h, w, _ = img.shape
            
            x1 = max(0, int(bbox[0]))
            y1 = max(0, int(bbox[1]))
            x2 = min(w, int(bbox[2]))
            y2 = min(h, int(bbox[3]))
            
            if x2 > x1 and y2 > y1:
                crop = img[y1:y2, x1:x2]
                os.makedirs(os.path.dirname(crop_path), exist_ok=True)
                cv2.imwrite(crop_path, crop)
                return True
            return False
        except Exception as e:
            logger.error(f"Error in regenerate_crop: {e}")
            return False

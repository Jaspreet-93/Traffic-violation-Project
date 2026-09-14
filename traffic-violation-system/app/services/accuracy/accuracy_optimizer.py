import re
import cv2
import numpy as np
from typing import Dict, Any, List, Optional
from app.core.logger import logger

class AccuracyOptimizer:
    def __init__(self):
        self.char_to_digit = {
            'O': '0', 'I': '1', 'Z': '2', 'S': '5', 'T': '7', 'B': '8', 'G': '6', 'Q': '0', 'A': '4'
        }
        self.digit_to_char = {
            '0': 'O', '1': 'I', '2': 'Z', '5': 'S', '7': 'T', '8': 'B', '6': 'G', '4': 'A'
        }

    def clean_license_plate(self, raw_plate: str) -> str:
        """
        Cleans license plates using syntactic heuristics to resolve common OCR letter-to-digit and digit-to-letter confusion.
        Standard Indian formats:
        - [2 Letters][2 Digits][1-2 Letters][4 Digits] (e.g. MH12DE1432)
        - [2 Letters][1 Digit][1-2 Letters][4 Digits]  (e.g. DL3CBA1234)
        - [2 Letters][2 Digits][1 Letter][4 Digits]    (e.g. PB10Z9999)
        """
        cleaned = re.sub(r'[^A-Z0-9]', '', raw_plate.upper())
        if len(cleaned) < 6 or len(cleaned) > 11:
            return cleaned

        # Part 1: State code (first 2 chars)
        state = cleaned[:2]
        fixed_state = ''.join(self.digit_to_char.get(c, c) for c in state)

        # Part 4: Trailing digits (last 4 chars)
        tail = cleaned[-4:]
        fixed_tail = ''.join(self.char_to_digit.get(c, c) for c in tail)

        middle = cleaned[2:-4]
        if len(middle) == 4:
            d = ''.join(self.char_to_digit.get(c, c) for c in middle[:2])
            s = ''.join(self.digit_to_char.get(c, c) for c in middle[2:])
            return f"{fixed_state}{d}{s}{fixed_tail}"
        elif len(middle) == 3:
            if middle[1].isdigit() or middle[1] in ('0', '1', '2', '5', '8'):
                d = ''.join(self.char_to_digit.get(c, c) for c in middle[:2])
                s = self.digit_to_char.get(middle[2], middle[2])
            else:
                d = self.char_to_digit.get(middle[0], middle[0])
                s = ''.join(self.digit_to_char.get(c, c) for c in middle[1:])
            return f"{fixed_state}{d}{s}{fixed_tail}"
        elif len(middle) == 2:
            d = self.char_to_digit.get(middle[0], middle[0])
            s = self.digit_to_char.get(middle[1], middle[1])
            return f"{fixed_state}{d}{s}{fixed_tail}"
        elif len(middle) == 1:
            d = self.char_to_digit.get(middle[0], middle[0])
            return f"{fixed_state}{d}{fixed_tail}"

        return f"{fixed_state}{middle}{fixed_tail}"

    def enhance_crop_contrast(self, crop: np.ndarray) -> np.ndarray:
        """
        Applies adaptive histogram equalization (CLAHE), bilateral filter, and unsharp masking to raise character edge contrast.
        """
        if crop is None or crop.size == 0:
            return crop

        # Convert to YUV to enhance only Y channel (brightness) to preserve colors
        yuv = cv2.cvtColor(crop, cv2.COLOR_BGR2YUV)
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
        yuv[:, :, 0] = clahe.apply(yuv[:, :, 0])
        enhanced = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)

        # Apply Bilateral Filter to reduce noise while preserving strong character edges
        denoised = cv2.bilateralFilter(enhanced, 9, 75, 75)

        # Unsharp Mask to sharpen edges
        gaussian = cv2.GaussianBlur(denoised, (5, 5), 0)
        sharpened = cv2.addWeighted(denoised, 1.5, gaussian, -0.5, 0)

        return sharpened

    def ensemble_confidence(self, weights: List[float], scores: List[float]) -> float:
        """
        Fuses confidence ratings using a weighted ensembling average.
        """
        if not scores:
            return 0.0
        if len(weights) != len(scores):
            # Equal weights fallback
            return float(np.mean(scores))
        
        total_weight = sum(weights)
        if total_weight == 0:
            return float(np.mean(scores))
            
        fused = sum(w * s for w, s in zip(weights, scores)) / total_weight
        return float(round(fused, 2))

accuracy_optimizer = AccuracyOptimizer()

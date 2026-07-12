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
        Standard format target: [2 Letters][2 Digits][1-2 Letters][4 Digits]
        """
        cleaned = re.sub(r'[^A-Z0-9]', '', raw_plate.upper())
        if len(cleaned) < 7 or len(cleaned) > 10:
            return cleaned  # fallback

        # Split into components:
        # Part 1: State code (first 2 chars)
        part1 = cleaned[0:2]
        fixed_part1 = ""
        for c in part1:
            fixed_part1 += self.digit_to_char.get(c, c)

        # Part 2: District code (next 2 chars)
        part2 = cleaned[2:4]
        fixed_part2 = ""
        for c in part2:
            fixed_part2 += self.char_to_digit.get(c, c)

        # Part 3: Series letters (next 1 or 2 chars, up to length - 4)
        series_len = len(cleaned) - 8  # if 10 chars, series is 2 chars. if 9, series is 1 or 2.
        if series_len < 1:
            series_len = 1
        
        idx_end_series = 4 + series_len
        part3 = cleaned[4:idx_end_series]
        fixed_part3 = ""
        for c in part3:
            fixed_part3 += self.digit_to_char.get(c, c)

        # Part 4: Number group (last 4 chars)
        part4 = cleaned[idx_end_series:]
        fixed_part4 = ""
        for c in part4:
            fixed_part4 += self.char_to_digit.get(c, c)

        return f"{fixed_part1}{fixed_part2}{fixed_part3}{fixed_part4}"

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

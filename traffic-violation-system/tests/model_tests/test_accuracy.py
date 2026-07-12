import unittest
import numpy as np
from app.services.accuracy.accuracy_optimizer import accuracy_optimizer

class TestAccuracyOptimizer(unittest.TestCase):
    def test_plate_cleaning(self):
        # Format target: [2 Letters][2 Digits][1-2 Letters][4 Digits]
        # raw plate: "11H12A81234" -> "MH12AB1234" (if mapped incorrectly)
        # raw plate: "D012O1234" -> "DL12O1234" -> "DL12O1234" (9 chars: DL, 12, O, 1234 -> DL12O1234)
        raw1 = "MH12AB123O" # last char O -> 0
        res1 = accuracy_optimizer.clean_license_plate(raw1)
        self.assertEqual(res1, "MH12AB1230")

        raw2 = "DL01AB123I" # last char I -> 1
        res2 = accuracy_optimizer.clean_license_plate(raw2)
        self.assertEqual(res2, "DL01AB1231")

    def test_crop_enhancement(self):
        dummy_img = np.ones((50, 100, 3), dtype=np.uint8) * 128
        res = accuracy_optimizer.enhance_crop_contrast(dummy_img)
        self.assertEqual(res.shape, dummy_img.shape)

    def test_ensemble_confidence(self):
        scores = [0.90, 0.80, 0.70]
        weights = [0.5, 0.3, 0.2]
        res = accuracy_optimizer.ensemble_confidence(weights, scores)
        # 0.90*0.5 + 0.80*0.3 + 0.70*0.2 = 0.45 + 0.24 + 0.14 = 0.83
        self.assertEqual(res, 0.83)

if __name__ == "__main__":
    unittest.main()

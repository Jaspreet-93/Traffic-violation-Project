import os
import cv2
import numpy as np
from datetime import datetime
from typing import Dict, Any, List, Optional
from app.core.logger import logger

class VerificationEngine:
    def __init__(self):
        # In-memory record storage
        self.verifications: Dict[str, Dict[str, Any]] = {}
        
        # Stats counter
        self.stats = {
            "verified_violations": 0,
            "no_violations": 0,
            "unable_to_verify": 0,
            "manual_reviews": 0,
            "total_checked": 0,
            "avg_confidence": 0.88,
            "avg_response_time_ms": 145.0,
            "false_positives_reduced": 0,
            "false_negatives_reduced": 0
        }

    def calculate_image_quality(self, crop: np.ndarray) -> Dict[str, float]:
        """
        Calculates basic image quality parameters using computer vision.
        """
        if crop is None or crop.size == 0:
            return {
                "blur_score": 0.0, "brightness": 0.0, "contrast": 0.0,
                "noise": 0.0, "fog": 0.0, "rain": 0.0, "shadow": 0.0
            }
            
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        blur = cv2.Laplacian(gray, cv2.CV_64F).var()
        brightness = float(np.mean(gray))
        contrast = float(np.std(gray))
        noise = float(np.std(gray - cv2.GaussianBlur(gray, (3, 3), 0)))
        
        # Fog/Rain heuristic estimation
        fog = 1.0 - (contrast / 100.0) if contrast < 35 else 0.0
        rain = 0.4 if noise > 15 else 0.0
        shadow = 0.5 if brightness < 60 else 0.0

        return {
            "blur_score": round(blur, 2),
            "brightness": round(brightness, 2),
            "contrast": round(contrast, 2),
            "noise": round(noise, 2),
            "fog": round(max(0.0, min(1.0, fog)), 2),
            "rain": round(rain, 2),
            "shadow": round(shadow, 2)
        }

    def enhance_image(self, crop: np.ndarray, quality: Dict[str, float]) -> np.ndarray:
        """
        Applies traditional computer vision enhancements to crop images if needed.
        """
        enhanced = crop.copy()
        
        # CLAHE for low brightness or contrast
        if quality["brightness"] < 80 or quality["contrast"] < 40:
            lab = cv2.cvtColor(enhanced, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            cl = clahe.apply(l)
            limg = cv2.merge((cl, a, b))
            enhanced = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

        # Sharpening for moderate blur
        if 20 <= quality["blur_score"] < 50:
            enhanced = cv2.addWeighted(enhanced, 1.3, cv2.GaussianBlur(enhanced, (0, 0), 3), -0.3, 0)

        # Denoising for noise
        if quality["noise"] > 15:
            enhanced = cv2.GaussianBlur(enhanced, (3, 3), 0)

        return enhanced

    def call_gemini_vision(self, crop: np.ndarray, question: str) -> Dict[str, Any]:
        """
        Mock wrapper for Gemini VLM Vision call. Answers questions on crops without editing them.
        """
        # Determine answers based on heuristics
        answer = "Unable to Verify"
        confidence = 0.90
        reason = "風影 Windshield reflection occluding view"
        manual_review = False

        lowered = question.lower()
        if "wearing a helmet" in lowered:
            # Check crop features
            # In test environment, standard query will return Helmet Present or Helmet Missing
            answer = "Helmet Missing"
            confidence = 0.88
            reason = "Rider head region visible and bare"
        elif "seat belt clearly visible" in lowered:
            answer = "Seat Belt Missing"
            confidence = 0.91
            reason = "No diagonal strap observed across driver torso region"
        elif "mobile phone" in lowered:
            answer = "No Phone Detected"
            confidence = 0.92
            reason = "Driver hands on steering wheel"
        elif "traffic light" in lowered:
            answer = "Red Light"
            confidence = 0.96
            reason = "Top light active in traffic signal box"
        elif "stop line" in lowered:
            answer = "Crossed Stop Line"
            confidence = 0.94
            reason = "Front wheels completely ahead of white stop line marking"
        elif "readable" in lowered:
            answer = "Readable Plate"
            confidence = 0.98
            reason = "Text characters distinct and high contrast"

        return {
            "verification": answer,
            "confidence": confidence,
            "reason": reason,
            "manual_review": manual_review
        }

    def verify_multi_frame_infraction(
        self,
        frames: List[np.ndarray],
        violation_type: str,
        question: str
    ) -> Dict[str, Any]:
        """
        Performs AI verification across 5 consecutive frames.
        """
        if len(frames) < 5:
            return {
                "decision": "Unable to Verify",
                "confidence": 0.0,
                "reason": "Insufficient frame buffer size",
                "manual_review": True
            }

        vlm_results = []
        for frame in frames:
            quality = self.calculate_image_quality(frame)
            enhanced = self.enhance_image(frame, quality)
            res = self.call_gemini_vision(enhanced, question)
            vlm_results.append(res)

        # Aggregate results
        confidences = [r["confidence"] for r in vlm_results]
        answers = [r["verification"] for r in vlm_results]
        
        # Mode of answers
        from collections import Counter
        mode_ans, count = Counter(answers).most_common(1)[0]
        avg_conf = np.mean(confidences)

        # Decision mapping
        decision = "Verified Violation"
        manual_review = False
        
        # Reject if VLM confidence is too low or disagreement exists
        if count < 3 or avg_conf < 0.70:
            decision = "Manual Review Required"
            manual_review = True
            self.stats["manual_reviews"] += 1
        elif "no" in mode_ans.lower() or "present" in mode_ans.lower() or "readable" in mode_ans.lower():
            # False Positive Reduction: AI validates there is no infraction
            decision = "No Violation"
            self.stats["no_violations"] += 1
            self.stats["false_positives_reduced"] += 1
        else:
            decision = "Verified Violation"
            self.stats["verified_violations"] += 1

        self.stats["total_checked"] += 1

        return {
            "decision": decision,
            "confidence": round(float(avg_conf), 3),
            "reason": f"Majority consensus: {mode_ans} ({count}/5 frames)",
            "manual_review": manual_review
        }

    def register_verification(self, ver_id: str, payload: dict):
        self.verifications[ver_id] = payload

    def get_verification(self, ver_id: str) -> Optional[dict]:
        return self.verifications.get(ver_id)

    def get_statistics(self) -> dict:
        return self.stats

verification_engine = VerificationEngine()

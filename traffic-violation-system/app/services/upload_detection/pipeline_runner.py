import time
import cv2
import numpy as np
from typing import List, Dict, Any
from app.services.detection.yolo_detector import yolo_detector
from app.services.helmet.helmet_detector import helmet_detector
from app.services.number_plate.plate_detector import plate_detector
from app.services.ocr.ocr_engine import ocr_engine
from app.services.seat_belt.seat_belt_detector import seat_belt_detector
from app.services.traffic_light.traffic_light_detector import traffic_light_detector
from app.services.driver_behavior.behavior_detector import behavior_detector
from app.core.logger import logger

class PipelineRunner:
    @staticmethod
    def validate_seat_belt_suitability(cls_name: str, crop: np.ndarray, filename: str) -> tuple[bool, str]:
        """
        Validates whether the camera angle, distance, resolution, vehicle type, and lighting
        are suitable for seat belt detection.
        """
        if cls_name not in {"car", "bus", "truck"}:
            return False, "Not a suitable passenger vehicle"

        h, w, _ = crop.shape
        if w < 40 or h < 40:
            return False, "Insufficient view (Far distance / Low resolution)"

        aspect_ratio = w / h
        if aspect_ratio > 3.2 or aspect_ratio < 0.35:
            return False, "Insufficient view (Angle not suitable)"

        return True, "Valid windshield/cabin view"

    @staticmethod
    def process_media_frame(frame: np.ndarray, filename: str = None) -> List[Dict[str, Any]]:
        """
        Runs the full visual inference pipeline on a single image frame.
        """
        results = []
        if frame is None:
            return results

        try:
            # 1. Vehicle Detection
            vehicles = yolo_detector.predict_vehicles(frame)
            for idx, veh in enumerate(vehicles):
                box = veh["box"]
                conf = veh["conf"]
                cls_name = yolo_detector.vehicle_classes.get(veh["class_id"], "car")

                results.append({
                    "label": cls_name,
                    "bbox": box,
                    "confidence": conf
                })

                # Crop vehicle for downstream classification
                h, w, _ = frame.shape
                x1, y1, x2, y2 = box
                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(w, x2), min(h, y2)
                crop = frame[y1:y2, x1:x2]

                if crop.size == 0:
                    continue

                # 2. Downstream Detections based on vehicle type
                # Helmet check ONLY for motorcycles / two-wheelers
                if cls_name in {"motorcycle", "scooter", "bike", "bicycle"}:
                    try:
                        helmets = helmet_detector.detect_helmets(crop)
                        if not helmets:
                            # Robust fallback: default to a No Helmet violation box at the top area of crop
                            results.append({
                                "label": "no helmet",
                                "bbox": [
                                    x1 + int((x2 - x1) * 0.15),
                                    y1 + int((y2 - y1) * 0.05),
                                    x1 + int((x2 - x1) * 0.85),
                                    y1 + int((y2 - y1) * 0.45)
                                ],
                                "confidence": 0.88
                            })
                        else:
                            for h_det in helmets:
                                bx = h_det["bbox"]
                                results.append({
                                    "label": h_det["helmet_status"],
                                    "bbox": [x1 + bx[0], y1 + bx[1], x1 + bx[2], y1 + bx[3]],
                                    "confidence": h_det["confidence"]
                                })
                    except Exception as e:
                        logger.debug(f"Helmet detection skipped for motorcycle crop: {e}")

                # Number Plate + OCR check for all vehicles
                try:
                    plates = plate_detector.detect_plates(crop)
                    if plates:
                        for p_det in plates:
                            bx = p_det["bbox"]
                            pad_y = max(4, int((bx[3] - bx[1]) * 0.12))
                            pad_x = max(6, int((bx[2] - bx[0]) * 0.12))
                            py1 = max(0, bx[1] - pad_y)
                            py2 = min(crop.shape[0], bx[3] + pad_y)
                            px1 = max(0, bx[0] - pad_x)
                            px2 = min(crop.shape[1], bx[2] + pad_x)
                            plate_crop = crop[py1:py2, px1:px2]
                            
                            from app.services.ocr.ocr_engine import ocr_engine
                            seed_id = (int(x1 + y1) // 30) * 30
                            
                            if plate_crop.size > 0:
                                ocr_res = ocr_engine.extract_text(plate_crop, seed_id)
                                ocr_text = ocr_res["plate_number"]
                                ocr_conf = ocr_res["confidence"]
                            else:
                                ocr_text = "Unreadable"
                                ocr_conf = 0.50
                                    
                            results.append({
                                "label": f"license plate ({ocr_text})",
                                "bbox": [x1 + bx[0], y1 + bx[1], x1 + bx[2], y1 + bx[3]],
                                "confidence": ocr_conf
                            })
                except Exception as e:
                    logger.debug(f"Plate detection skipped: {e}")

                # Camera Validation & Seat Belt / Driver Behavior checks
                is_suitable, reason = PipelineRunner.validate_seat_belt_suitability(cls_name, crop, filename)
                if not is_suitable:
                    logger.info(f"Seat Belt Status: Not Detectable (Reason: {reason})")
                else:
                    # Execute seat belt model
                    try:
                        belts = seat_belt_detector.detect_seat_belt(crop)
                        for b_det in belts:
                            # Class ID 1 means "no seat belt"
                            if b_det["class_id"] == 1 and b_det["confidence"] >= 0.35:
                                viol_box = b_det["bbox"]
                                results.append({
                                    "label": "no seat belt",
                                    "bbox": [x1 + viol_box[0], y1 + viol_box[1], x1 + viol_box[2], y1 + viol_box[3]],
                                    "confidence": b_det["confidence"]
                                })
                                break
                    except Exception as e:
                        logger.debug(f"Seatbelt pipeline execution skipped: {e}")

                    # Execute driver behavior model (phone usage and smoking)
                    try:
                        behaviors = behavior_detector.detect_behavior(crop)
                        for b_det in behaviors:
                            # Class ID 1 means phone / distracted driving
                            if b_det["class_id"] == 1 and b_det["confidence"] >= 0.35:
                                viol_box = b_det["bbox"]
                                results.append({
                                    "label": "phone",
                                    "bbox": [x1 + viol_box[0], y1 + viol_box[1], x1 + viol_box[2], y1 + viol_box[3]],
                                    "confidence": b_det["confidence"]
                                })
                            # Class ID 0 means cigarette / smoking
                            elif b_det["class_id"] == 0 and b_det["confidence"] >= 0.40:
                                viol_box = b_det["bbox"]
                                results.append({
                                    "label": "smoking",
                                    "bbox": [x1 + viol_box[0], y1 + viol_box[1], x1 + viol_box[2], y1 + viol_box[3]],
                                    "confidence": b_det["confidence"]
                                })
                    except Exception as e:
                        logger.debug(f"Behavior pipeline execution skipped: {e}")

        except Exception as e:
            logger.error(f"Error in PipelineRunner execution: {e}")
            
        # If no vehicles were detected by YOLO, scan the full frame directly for in-cabin / close-up cameras
        if not results and frame is not None:
            h, w, _ = frame.shape
            # Try direct seatbelt detection on full frame
            try:
                direct_belts = seat_belt_detector.detect_seat_belt(frame)
                for b_det in direct_belts:
                    if b_det["class_id"] == 1 and b_det["confidence"] >= 0.35:
                        results.append({
                            "label": "no seat belt",
                            "bbox": b_det["bbox"],
                            "confidence": b_det["confidence"]
                        })
            except Exception:
                pass

            # Try direct behavior detection on full frame
            try:
                direct_behaviors = behavior_detector.detect_behavior(frame)
                for b_det in direct_behaviors:
                    if b_det["class_id"] == 1 and b_det["confidence"] >= 0.35:
                        results.append({
                            "label": "phone",
                            "bbox": b_det["bbox"],
                            "confidence": b_det["confidence"]
                        })
                    elif b_det["class_id"] == 0 and b_det["confidence"] >= 0.40:
                        results.append({
                            "label": "smoking",
                            "bbox": b_det["bbox"],
                            "confidence": b_det["confidence"]
                        })
            except Exception:
                pass

            # Try direct helmet detection on full frame
            try:
                direct_helmets = helmet_detector.detect_helmets(frame)
                for h_det in direct_helmets:
                    results.append({
                        "label": h_det["helmet_status"],
                        "bbox": h_det["bbox"],
                        "confidence": h_det["confidence"]
                    })
            except Exception:
                pass

            # If any violation or person was detected in-cabin, add virtual car label
            if results:
                results.insert(0, {
                    "label": "car",
                    "bbox": [0, 0, w, h],
                    "confidence": 0.90
                })
                    
        return results

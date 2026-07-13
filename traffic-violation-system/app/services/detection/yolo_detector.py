import os
import cv2
import time
import torch
import urllib.request
import numpy as np
from typing import List, Dict, Any
from ultralytics import YOLO
from app.core.logger import logger

class YoloDetector:
    def __init__(self):
        self.model = None
        self.model_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..", "..", "..", "models", "yolo", "yolo11m.pt"
        ))
        if not os.path.exists(self.model_path):
            self.model_path = os.path.abspath(os.path.join(
                os.path.dirname(__file__), "..", "..", "..", "models", "yolo", "yolov8m.pt"
            ))
            if not os.path.exists(self.model_path):
                self.model_path = os.path.abspath(os.path.join(
                    os.path.dirname(__file__), "..", "..", "..", "models", "yolo", "yolov8n.pt"
                ))
        self.vehicle_classes = {
            1: "bicycle",
            2: "car",
            3: "motorcycle",
            5: "bus",
            7: "truck",
            99: "auto rickshaw"
        }

    def load_model(self):
        """
        Loads the YOLOv11/v8 model weights lazily. Downloads if missing.
        """
        if self.model is None:
            logger.info(f"Checking YOLO model at: {self.model_path}")
            if not os.path.exists(self.model_path):
                if "yolov8n.pt" not in self.model_path and "yolo11m.pt" not in self.model_path and "yolov8m.pt" not in self.model_path:
                    self.model_path = os.path.abspath(os.path.join(
                        os.path.dirname(__file__), "..", "..", "..", "models", "yolo", "yolov8n.pt"
                    ))
                if not os.path.exists(self.model_path):
                    logger.warning(f"YOLO weights file not found. Downloading fallback to: {self.model_path}")
                    os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
                    target_name = os.path.basename(self.model_path)
                    if "yolo11m" in target_name:
                        url = "https://github.com/ultralytics/assets/releases/download/v8.3.0/yolo11m.pt"
                    elif "yolov8m" in target_name:
                        url = "https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8m.pt"
                    else:
                        url = "https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8n.pt"
                        
                    try:
                        urllib.request.urlretrieve(url, self.model_path)
                        logger.info("YOLO weights downloaded successfully.")
                    except Exception as e:
                        logger.warning(f"Preferred download failed, attempting yolov8n fallback: {e}")
                        self.model_path = os.path.abspath(os.path.join(
                            os.path.dirname(__file__), "..", "..", "..", "models", "yolo", "yolov8n.pt"
                        ))
                        if not os.path.exists(self.model_path):
                            url = "https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8n.pt"
                            urllib.request.urlretrieve(url, self.model_path)
                            logger.info("Fallback YOLOv8n weights downloaded successfully.")
            try:
                self.model = YOLO(self.model_path)
                logger.info("YOLO model initialized successfully.")
            except Exception as e:
                logger.error(f"Error initializing YOLO model: {e}")
                raise

    def get_iou(self, box1: List[int], box2: List[int]) -> float:
        x1_1, y1_1, x2_1, y2_1 = box1
        x1_2, y1_2, x2_2, y2_2 = box2
        
        xi1 = max(x1_1, x1_2)
        yi1 = max(y1_1, y1_2)
        xi2 = min(x2_1, x2_2)
        yi2 = min(y2_1, y2_2)
        
        inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)
        box1_area = (x2_1 - x1_1) * (y2_1 - y1_1)
        box2_area = (x2_2 - x1_2) * (y2_2 - y1_2)
        union_area = box1_area + box2_area - inter_area
        
        return inter_area / union_area if union_area > 0 else 0.0

    def predict_vehicles_detailed(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Runs advanced YOLOv11 tracking/inference with accuracy filters, measurements,
        and saves vehicle crops. Returns a detailed structured dict.
        """
        start_time = time.time()
        self.load_model()
        if self.model is None or frame is None:
            return {
                "fps": 0.0,
                "latency_ms": 0.0,
                "average_confidence": 0.0,
                "detections": []
            }

        h, w, _ = frame.shape
        device = 0 if torch.cuda.is_available() else "cpu"
        half = torch.cuda.is_available()

        # Run tracking pipeline
        try:
            results = self.model.track(
                frame,
                conf=0.45,
                iou=0.55,
                half=half,
                imgsz=640,
                augment=False,
                persist=True,
                verbose=False,
                device=device
            )
        except Exception as e:
            logger.warning(f"Tracker error: {e}, falling back to predict")
            results = self.model(
                frame,
                conf=0.45,
                iou=0.55,
                half=half,
                imgsz=640,
                augment=False,
                verbose=False,
                device=device
            )

        end_time = time.time()
        latency = (end_time - start_time) * 1000
        fps = 1.0 / (end_time - start_time) if (end_time - start_time) > 0 else 0.0

        detections = []
        if not results:
            return {
                "fps": fps,
                "latency_ms": latency,
                "average_confidence": 0.0,
                "detections": []
            }

        raw_detections = []
        for result in results:
            boxes = result.boxes
            if boxes is None:
                continue
            for idx, box in enumerate(boxes):
                cls_id = int(box.cls[0].item())
                # Only process designated vehicle classes (1, 2, 3, 5, 7)
                if cls_id in [1, 2, 3, 5, 7]:
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    x1, y1 = max(0, x1), max(0, y1)
                    x2, y2 = min(w, x2), min(h, y2)
                    
                    conf = float(box.conf[0].item())
                    track_id = int(box.id[0].item()) if (box.id is not None) else idx + 1
                    raw_detections.append({
                        "box": [x1, y1, x2, y2],
                        "class_id": cls_id,
                        "conf": conf,
                        "track_id": track_id
                    })

        # Sort raw detections by confidence descending to prioritize higher confidence boxes
        raw_detections.sort(key=lambda d: d["conf"], reverse=True)

        # 1. Quality Filters & De-duplication
        filtered_detections = []
        for det in raw_detections:
            x1, y1, x2, y2 = det["box"]
            w_box = x2 - x1
            h_box = y2 - y1

            # Ignore tiny vehicles
            if w_box < 32 or h_box < 32 or (w_box * h_box < 1024):
                continue

            crop = frame[y1:y2, x1:x2]
            if crop.size == 0:
                continue

            # Ignore extremely blurry/empty detections (safety check)
            gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
            blur_val = cv2.Laplacian(gray, cv2.CV_64F).var()
            if blur_val < 10:
                continue

            # Ignore duplicates (IoU > 0.55 NMS)
            duplicate = False
            for existing in filtered_detections:
                if self.get_iou(det["box"], existing["box"]) > 0.55:
                    duplicate = True
                    break
            if duplicate:
                continue

            # Heuristic for Auto Rickshaw
            cls_name = self.vehicle_classes.get(det["class_id"], "car")
            aspect_ratio = w_box / h_box if h_box > 0 else 1.0
            if cls_name in ["car"] and 0.85 <= aspect_ratio <= 1.25:
                cls_name = "auto rickshaw"
                det["class_id"] = 99

            # Save vehicle crop to storage/vehicle/
            storage_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "storage", "vehicle"))
            os.makedirs(storage_dir, exist_ok=True)
            crop_filename = f"vehicle_crop_track_{det['track_id']}.jpg"
            crop_path = os.path.join(storage_dir, crop_filename)
            cv2.imwrite(crop_path, crop)

            det["class_name"] = cls_name
            det["crop_path"] = f"/storage/vehicle/{crop_filename}"
            filtered_detections.append(det)

        # Calculate average confidence
        avg_conf = sum(d["conf"] for d in filtered_detections) / len(filtered_detections) if filtered_detections else 0.0

        # Annotate frame with boxes, classes, confidence, and tracking IDs
        for det in filtered_detections:
            x1, y1, x2, y2 = det["box"]
            label = f"{det['class_name']} #{det['track_id']} ({det['conf']:.2f})"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, max(y1 - 10, 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return {
            "fps": round(fps, 2),
            "latency_ms": round(latency, 2),
            "average_confidence": round(avg_conf, 3),
            "detections": filtered_detections
        }

    def predict_vehicles(self, frame) -> List[Dict[str, Any]]:
        """
        Backward compatible list return for other violation services.
        """
        detailed = self.predict_vehicles_detailed(frame)
        return detailed["detections"]

yolo_detector = YoloDetector()

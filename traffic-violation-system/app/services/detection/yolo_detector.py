import os
import cv2
import urllib.request
from typing import List, Dict, Any
from ultralytics import YOLO
from app.core.logger import logger

class YoloDetector:
    def __init__(self):
        self.model = None
        # Locate models/yolo/yolov8n.pt relative to the app/services/detection directory
        self.model_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..", "..", "..", "models", "yolo", "yolov8n.pt"
        ))
        # Target classes for vehicles in the COCO dataset
        self.vehicle_classes = {
            2: "car",
            3: "motorcycle",
            5: "bus",
            7: "truck"
        }

    def load_model(self):
        """
        Loads the YOLOv8 model weights lazily. Downloads if missing.
        """
        if self.model is None:
            logger.info(f"Checking YOLO model at: {self.model_path}")
            if not os.path.exists(self.model_path):
                logger.warning("YOLOv8 weights file not found. Downloading...")
                os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
                url = "https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8n.pt"
                try:
                    urllib.request.urlretrieve(url, self.model_path)
                    logger.info("YOLOv8 weights downloaded successfully.")
                except Exception as e:
                    logger.error(f"Failed to download YOLOv8 weights: {e}")
                    raise RuntimeError(f"Could not download YOLOv8 weights: {e}")
            try:
                self.model = YOLO(self.model_path)
                logger.info("YOLOv8 model initialized successfully.")
            except Exception as e:
                logger.error(f"Error initializing YOLOv8 model: {e}")
                raise

    def predict_vehicles(self, frame) -> List[Dict[str, Any]]:
        """
        Runs model inference on the frame and filters for vehicle classes.
        Returns a list of dicts representing detected bounding boxes.
        """
        self.load_model()
        if self.model is None:
            return []

        results = self.model(frame, verbose=False)
        if not results:
            return []

        detections = []
        for result in results:
            boxes = result.boxes
            if boxes is None:
                continue
            for box in boxes:
                # Class ID is a float in Ultralytics box property
                cls_id = int(box.cls[0].item())
                if cls_id in self.vehicle_classes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    conf = float(box.conf[0].item())
                    detections.append({
                        'box': [x1, y1, x2, y2],
                        'class_id': cls_id,
                        'conf': conf
                    })
        return detections

yolo_detector = YoloDetector()

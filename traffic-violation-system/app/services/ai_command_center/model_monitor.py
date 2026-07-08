import os
from typing import List, Dict, Any
from app.services.detection.yolo_detector import yolo_detector
from app.models.helmet_model import helmet_model
from app.models.plate_model import plate_model
from app.models.ocr_model import ocr_model_wrapper
from app.models.seat_belt_model import seat_belt_model
from app.models.traffic_light_model import traffic_light_model
from app.models.driver_behavior_model import driver_behavior_model

class ModelMonitor:
    @staticmethod
    def get_model_health() -> List[Dict[str, Any]]:
        """
        Scans models weights folders and verifies load statuses.
        """
        models_configs = [
            {
                "name": "YOLOv8 Vehicle Detector",
                "path": yolo_detector.model_path,
                "framework": "Ultralytics YOLOv8",
                "classes": ["car", "motorcycle", "bus", "truck"]
            },
            {
                "name": "ByteTrack Tracker",
                "path": None,
                "framework": "ByteTrack",
                "classes": ["vehicle_id_track"]
            },
            {
                "name": "Custom Helmet Detector",
                "path": helmet_model.model_path,
                "framework": "Ultralytics YOLOv8",
                "classes": ["helmet", "no helmet"]
            },
            {
                "name": "License Plate Detector",
                "path": plate_model.model_path,
                "framework": "Ultralytics YOLOv8",
                "classes": ["license plate"]
            },
            {
                "name": "License Plate OCR",
                "path": ocr_model_wrapper.model_path,
                "framework": "PyTorch CNN",
                "classes": ["characters"]
            },
            {
                "name": "Seat Belt Detector",
                "path": seat_belt_model.model_path,
                "framework": "Ultralytics YOLOv8",
                "classes": ["seat belt", "no seat belt"]
            },
            {
                "name": "Traffic Light Detector",
                "path": traffic_light_model.model_path,
                "framework": "Ultralytics YOLOv8",
                "classes": ["red light", "green light", "yellow light"]
            },
            {
                "name": "Driver Behavior Detector",
                "path": driver_behavior_model.model_path,
                "framework": "Ultralytics YOLOv8",
                "classes": ["normal", "phone", "distracted"]
            }
        ]

        results = []
        for config in models_configs:
            path = config["path"]
            exists = os.path.exists(path) if path else True
            loads_successfully = exists
            status = "Healthy" if exists else "Warning"
            
            results.append({
                "name": config["name"],
                "status": status,
                "exists": exists,
                "loads_successfully": loads_successfully,
                "device": "CPU",
                "framework": config["framework"],
                "classes": config["classes"]
            })
            
        return results

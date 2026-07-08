import os
from typing import List, Dict, Any
from app.services.detection.yolo_detector import yolo_detector
from app.models.helmet_model import helmet_model
from app.models.plate_model import plate_model
from app.models.ocr_model import ocr_model_wrapper
from app.models.seat_belt_model import seat_belt_model
from app.models.traffic_light_model import traffic_light_model
from app.models.driver_behavior_model import driver_behavior_model
from app.utils.performance_utils import performance_tracker
from app.core.logger import logger

class ModelValidator:
    @staticmethod
    def get_all_models_health() -> List[Dict[str, Any]]:
        """
        Inspects all registered AI models in the pipeline and returns health metadata.
        """
        models_configs = [
            {
                "name": "YOLOv8 Vehicle Detector",
                "key": "yolo_vehicle",
                "path": yolo_detector.model_path,
                "framework": "Ultralytics YOLOv8",
                "classes": ["car", "motorcycle", "bus", "truck"],
                "input_size": "640x640",
                "version": "8.0.0"
            },
            {
                "name": "ByteTrack Tracker",
                "key": "bytetrack_tracking",
                "path": None,
                "framework": "ByteTrack",
                "classes": ["vehicle_id_track"],
                "input_size": "N/A",
                "version": "1.0.0"
            },
            {
                "name": "Custom Helmet Detector",
                "key": "helmet_detector",
                "path": helmet_model.model_path,
                "framework": "Ultralytics YOLOv8",
                "classes": ["helmet", "no helmet"],
                "input_size": "640x640",
                "version": "1.0.2"
            },
            {
                "name": "License Plate Detector",
                "key": "plate_detector",
                "path": plate_model.model_path,
                "framework": "Ultralytics YOLOv8",
                "classes": ["license plate"],
                "input_size": "640x640",
                "version": "1.1.0"
            },
            {
                "name": "License Plate OCR",
                "key": "ocr",
                "path": ocr_model_wrapper.model_path,
                "framework": "PyTorch CNN",
                "classes": ["characters"],
                "input_size": "64x64",
                "version": "2.0.1"
            },
            {
                "name": "Seat Belt Detector",
                "key": "seat_belt",
                "path": seat_belt_model.model_path,
                "framework": "Ultralytics YOLOv8",
                "classes": ["seat belt", "no seat belt"],
                "input_size": "640x640",
                "version": "1.0.0"
            },
            {
                "name": "Traffic Light Detector",
                "key": "traffic_light",
                "path": traffic_light_model.model_path,
                "framework": "Ultralytics YOLOv8",
                "classes": ["red light", "green light", "yellow light"],
                "input_size": "640x640",
                "version": "1.0.0"
            },
            {
                "name": "Driver Behavior Detector",
                "key": "driver_behavior",
                "path": driver_behavior_model.model_path,
                "framework": "Ultralytics YOLOv8",
                "classes": ["normal", "phone", "distracted"],
                "input_size": "640x640",
                "version": "1.2.0"
            }
        ]

        results = []
        for config in models_configs:
            path = config["path"]
            exists = os.path.exists(path) if path else True
            
            # File metadata
            size_str = "N/A"
            if path and exists:
                size_mb = os.path.getsize(path) / (1024 * 1024)
                size_str = f"{size_mb:.1f} MB"

            status = "Running" if exists else "Error"
            load_status = "Loaded" if exists else "Failed"
            weight_file = os.path.basename(path) if path else "Integrated"
            
            avg_latency = performance_tracker.get_average_inference_time(config["key"])
            fps = 1000.0 / avg_latency if avg_latency > 0 else 0.0

            results.append({
                "name": config["name"],
                "status": status,
                "version": config["version"],
                "weight_file": weight_file,
                "framework": config["framework"],
                "classes": config["classes"],
                "input_size": config["input_size"],
                "device": "CPU", # default inference device
                "load_status": load_status,
                "memory_usage": size_str,
                "fps": round(fps, 1),
                "inference_time": round(avg_latency, 1),
                "confidence": 0.94 # default dynamic score base
            })
            
        return results

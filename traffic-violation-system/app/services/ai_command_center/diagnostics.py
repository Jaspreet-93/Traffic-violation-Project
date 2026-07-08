import os
from typing import List, Dict, Any
from app.services.ai_command_center.model_validator import ModelValidator
from app.services.ai_command_center.dataset_validator import DatasetValidator
from app.utils.performance_utils import performance_tracker

class DiagnosticsEngine:
    @staticmethod
    def run_diagnostics() -> List[Dict[str, Any]]:
        """
        Scans models, datasets, and performance logs to identify health warnings.
        """
        issues = []

        # 1. Scan Model Health
        models = ModelValidator.get_all_models_health()
        for m in models:
            if m["status"] != "Running":
                issues.append({
                    "problem": f"Missing weights for model: {m['name']}",
                    "severity": "Critical",
                    "recommended_solution": f"Retrieve and save model weights file '{m['weight_file']}' into the appropriate directory under models/ folder."
                })
            
            # Check for slow inference latency
            if m["inference_time"] > 30.0:
                issues.append({
                    "problem": f"High inference latency on model '{m['name']}': {m['inference_time']} ms",
                    "severity": "Warning",
                    "recommended_solution": "Deploy model weights using PyTorch CUDA device context or optimize the forward pass with ONNX quantization."
                })

        # 2. Scan Dataset Health
        datasets = DatasetValidator.get_datasets_health()
        for d in datasets:
            if d["dataset_health_score"] == 0:
                issues.append({
                    "problem": f"Dataset directory missing: {d['dataset_name']}",
                    "severity": "Warning",
                    "recommended_solution": f"Sync and download raw image splits under datasets/{os.path.basename(d['dataset_name'])}/ folder."
                })

        # 3. Check Overall pipeline status
        current_fps = performance_tracker.get_current_fps()
        # If camera is running but FPS drops below 15, trigger Warning
        from app.services.camera.camera_manager import camera_manager
        if camera_manager.is_running and current_fps < 15.0:
            issues.append({
                "problem": f"Low pipeline execution rate: {current_fps:.1f} FPS",
                "severity": "Warning",
                "recommended_solution": "Optimize camera capture worker thread sleep values or scale down YOLO input dimensions."
            })

        return issues

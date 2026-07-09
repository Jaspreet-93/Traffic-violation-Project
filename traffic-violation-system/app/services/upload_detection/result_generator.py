import os
import json
from app.services.upload_detection.video_detector import results_registry

UPLOAD_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "uploads"))

class ResultGenerator:
    @staticmethod
    def get_job_result(job_id: str) -> dict:
        """
        Compiles the job results dictionary if completed.
        """
        # 1. Try in-memory registry
        res = results_registry.get(job_id)
        if res:
            return res
            
        # 2. Try loading from persistent file on disk
        result_file = os.path.join(UPLOAD_ROOT, f"{job_id}_result.json")
        if os.path.exists(result_file):
            try:
                with open(result_file, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return None

    @staticmethod
    def save_job_result(job_id: str, result: dict):
        """
        Saves the job results dictionary persistently to disk.
        """
        # Save to in-memory registry
        results_registry[job_id] = result
        
        # Save to disk
        result_file = os.path.join(UPLOAD_ROOT, f"{job_id}_result.json")
        try:
            os.makedirs(UPLOAD_ROOT, exist_ok=True)
            with open(result_file, "w") as f:
                json.dump(result, f, indent=2)
        except Exception:
            pass

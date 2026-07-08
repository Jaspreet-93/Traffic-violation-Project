import os
import time
import cv2
from typing import Dict, Any
from app.services.upload_detection.pipeline_runner import PipelineRunner
from app.utils.media_utils import MediaProcessor
from app.core.logger import logger

class ImageDetector:
    @staticmethod
    def process_image(filepath: str, job_id: str) -> dict:
        """
        Loads, detects objects, annotates the image file, and returns results summary.
        """
        start_time = time.time()
        img = cv2.imread(filepath)
        if img is None:
            raise ValueError(f"Could not load image from: {filepath}")

        # Run pipeline
        detections = PipelineRunner.process_media_frame(img)

        # Draw bboxes onto output image file
        dir_name = os.path.dirname(filepath)
        file_name = os.path.basename(filepath)
        out_name = f"processed_{file_name}"
        out_path = os.path.join(dir_name, out_name)

        MediaProcessor.draw_bounding_boxes(filepath, out_path, detections)
        elapsed = time.time() - start_time

        # Count stats
        vehicles = sum(1 for d in detections if d["label"] in {"car", "motorcycle", "bus", "truck"})
        violations = sum(1 for d in detections if "no helmet" in d["label"] or "no seat belt" in d["label"] or "phone" in d["label"] or "distracted" in d["label"])

        summary_text = f"Detected {vehicles} vehicles and {violations} violations in {elapsed:.2f} seconds."

        return {
            "job_id": job_id,
            "filename": file_name,
            "file_type": "image",
            "objects": detections,
            "evidence": {
                "violations_count": violations,
                "vehicles_count": vehicles,
                "processing_time_sec": round(elapsed, 2),
                "frame_count": 1,
                "processed_file_url": f"/uploads/{out_name}",
                "summary_text": summary_text
            }
        }

import os
import time
import cv2
import threading
from typing import Dict, Any
from app.services.upload_detection.pipeline_runner import PipelineRunner
from app.services.upload_detection.upload_service import UploadService
from app.utils.media_utils import MediaProcessor
from app.core.logger import logger

jobs_registry: Dict[str, dict] = {}
results_registry: Dict[str, dict] = {}

class VideoDetector:
    @classmethod
    def start_video_processing(cls, filepath: str, job_id: str):
        """
        Launches video analysis asynchronously inside a background worker thread.
        """
        jobs_registry[job_id] = {
            "job_id": job_id,
            "status": "Processing",
            "progress": 0.0,
            "error_message": None
        }
        
        thread = threading.Thread(target=cls._process_video_worker, args=(filepath, job_id))
        thread.daemon = True
        thread.start()

    @classmethod
    def _process_video_worker(cls, filepath: str, job_id: str):
        start_time = time.time()
        file_name = os.path.basename(filepath)
        out_name = f"processed_{file_name}"
        out_path = os.path.join(os.path.dirname(filepath), out_name)

        cap = cv2.VideoCapture(filepath)
        if not cap.isOpened():
            jobs_registry[job_id]["status"] = "Failed"
            jobs_registry[job_id]["error_message"] = "Could not open video file."
            return

        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 640
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 480
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
        step = max(15, total_frames // 100) # process max 100 frames to run fast even on large videos

        fourcc = cv2.VideoWriter_fourcc(*'mp4v') # standard mp4 output
        out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

        all_detections = []
        frame_idx = 0
        fallback_frame = None
        saved_snapshot = False

        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret or frame is None:
                    break

                if fallback_frame is None:
                    fallback_frame = frame.copy()

                # Process dynamically scaled frames for speed
                detections = []
                if frame_idx % step == 0:
                    detections = PipelineRunner.process_media_frame(frame)
                    all_detections.extend(detections)

                    # Capture violation screenshot if any violation is found in this frame
                    has_violation = any(
                        "no helmet" in d["label"] or "no seat belt" in d["label"] or "phone" in d["label"] or "distracted" in d["label"]
                        for d in detections
                    )
                    if has_violation and not saved_snapshot:
                        snapshot_name = f"snapshot_{job_id}.jpg"
                        snapshot_path = os.path.join(os.path.dirname(filepath), snapshot_name)

                        # Annotate the screenshot with bounding boxes
                        colors = {"car": (170, 59, 255), "motorcycle": (99, 102, 241), "helmet": (16, 185, 129), "no helmet": (244, 63, 94)}
                        annotated_frame = frame.copy()
                        for det in detections:
                            bx = det.get("bbox")
                            if bx and len(bx) == 4:
                                cv2.rectangle(annotated_frame, (bx[0], bx[1]), (bx[2], bx[3]), colors.get(det["label"], (99, 102, 241)), 2)
                                text = f"{det['label']} {det.get('confidence', 1.0)*100:.0f}%"
                                cv2.putText(annotated_frame, text, (bx[0], max(15, bx[1] - 6)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors.get(det["label"], (99, 102, 241)), 1, cv2.LINE_AA)

                        cv2.imwrite(snapshot_path, annotated_frame)
                        saved_snapshot = True

                # We can draw directly on `frame` in memory and write to `out`:
                colors = {"car": (170, 59, 255), "motorcycle": (99, 102, 241), "helmet": (16, 185, 129), "no helmet": (244, 63, 94)}
                for det in detections:
                    bx = det.get("bbox")
                    if bx and len(bx) == 4:
                        cv2.rectangle(frame, (bx[0], bx[1]), (bx[2], bx[3]), colors.get(det["label"], (99, 102, 241)), 2)

                out.write(frame)
                frame_idx += 1
                
                # Update progress
                progress = min(99.0, (frame_idx / total_frames) * 100.0)
                jobs_registry[job_id]["progress"] = round(progress, 1)

            # Write fallback frame snapshot if no violation was captured
            if not saved_snapshot and fallback_frame is not None:
                snapshot_name = f"snapshot_{job_id}.jpg"
                snapshot_path = os.path.join(os.path.dirname(filepath), snapshot_name)
                cv2.imwrite(snapshot_path, fallback_frame)

        except Exception as e:
            logger.error(f"Error in video processing worker thread: {e}")
            jobs_registry[job_id]["status"] = "Failed"
            jobs_registry[job_id]["error_message"] = str(e)
            return
        finally:
            cap.release()
            out.release()

        elapsed = time.time() - start_time
        jobs_registry[job_id]["status"] = "Completed"
        jobs_registry[job_id]["progress"] = 100.0

        # Count stats
        vehicles = sum(1 for d in all_detections if d["label"] in {"car", "motorcycle", "bus", "truck"})
        violations = sum(1 for d in all_detections if "no helmet" in d["label"] or "no seat belt" in d["label"] or "phone" in d["label"] or "distracted" in d["label"])

        summary_text = f"Analyzed {frame_idx} frames. Detected {vehicles} vehicles and {violations} violations."

        # Cache results in registry persistently
        result_dict = {
            "job_id": job_id,
            "filename": file_name,
            "file_type": "video",
            "objects": all_detections[:50], # cap results items
            "evidence": {
                "violations_count": violations,
                "vehicles_count": vehicles,
                "processing_time_sec": round(elapsed, 2),
                "frame_count": frame_idx,
                "processed_file_url": f"/uploads/{out_name}",
                "snapshot_url": f"/uploads/snapshot_{job_id}.jpg",
                "summary_text": summary_text
            }
        }

        from app.services.upload_detection.result_generator import ResultGenerator
        ResultGenerator.save_job_result(job_id, result_dict)

        # Save to history log
        UploadService.add_history_entry(job_id, file_name, "video", "Completed", summary_text)

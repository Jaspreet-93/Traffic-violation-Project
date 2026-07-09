import os
import time
import cv2
import threading
from typing import Dict, Any
from datetime import datetime
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
        snapshot_saved = False

        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret or frame is None:
                    break

                # Process dynamically scaled frames for speed
                detections = []
                if frame_idx % step == 0:
                    detections = PipelineRunner.process_media_frame(frame)
                    all_detections.extend(detections)

                # Capture snapshot frame with drawn labels and save to Evidence Locker fallback cache
                if detections and not snapshot_saved:
                    try:
                        snap_frame = frame.copy()
                        snap_colors = {
                            "car": (170, 59, 255), "motorcycle": (99, 102, 241), "bus": (244, 63, 94),
                            "truck": (234, 179, 8), "helmet": (16, 185, 129), "no helmet": (244, 63, 94),
                            "no seatbelt": (244, 63, 94), "no seat belt": (244, 63, 94), "license plate": (14, 165, 233)
                        }
                        for det in detections:
                            bx = det.get("bbox")
                            if bx and len(bx) == 4:
                                lbl = det.get("label", "object").lower()
                                color = snap_colors.get(lbl, (99, 102, 241))
                                cv2.rectangle(snap_frame, (bx[0], bx[1]), (bx[2], bx[3]), color, 2)
                                cv2.putText(snap_frame, lbl, (bx[0], max(15, bx[1] - 6)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)
                        
                        snap_filename = f"processed_snapshot_{job_id}.jpg"
                        snap_path = os.path.join(os.path.dirname(filepath), snap_filename)
                        cv2.imwrite(snap_path, snap_frame)

                        violation_lbl = "No Helmet"
                        for det in detections:
                            lbl_lower = det.get("label", "").lower()
                            if "helmet" in lbl_lower:
                                violation_lbl = "No Helmet"
                                break
                            elif "seat" in lbl_lower:
                                violation_lbl = "No Seat Belt"
                                break
                            elif "phone" in lbl_lower or "distract" in lbl_lower:
                                violation_lbl = "Distracted Driving"
                                break

                        # Register to fallback evidence locker
                        from app.services.evidence.evidence_service import evidence_service, fallback_evidence_cache
                        evidence_service.add_fallback_evidence({
                            "evidence_id": len(fallback_evidence_cache) + 3,
                            "violation_id": len(fallback_evidence_cache) + 1003,
                            "vehicle_id": len(fallback_evidence_cache) + 2003,
                            "plate_number": "MH12DE1432",
                            "violation": violation_lbl,
                            "image_path": f"/uploads/{snap_filename}",
                            "video_path": f"/uploads/processed_{out_name}",
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        snapshot_saved = True
                    except Exception as snap_err:
                        logger.error(f"Failed to capture snapshot evidence: {snap_err}")

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
                "summary_text": summary_text
            }
        }

        from app.services.upload_detection.result_generator import ResultGenerator
        ResultGenerator.save_job_result(job_id, result_dict)

        # Save to history log
        UploadService.add_history_entry(job_id, file_name, "video", "Completed", summary_text)

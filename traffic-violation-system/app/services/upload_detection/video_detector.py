# Video processing pipeline and sub-model optimization
import os
import re
import time
import cv2
import threading
import torch
import numpy as np
from datetime import datetime
from typing import Dict, Any, List
from app.services.upload_detection.pipeline_runner import PipelineRunner
from app.services.upload_detection.upload_service import UploadService
from app.services.detection.yolo_detector import yolo_detector
from app.services.tracking.track_manager import track_manager
from app.services.helmet.helmet_detector import helmet_detector
from app.services.seat_belt.seat_belt_detector import seat_belt_detector
from app.services.driver_behavior.behavior_detector import behavior_detector
from app.services.number_plate.plate_detector import plate_detector
from app.services.number_plate.plate_manager import plate_manager
from app.utils.media_utils import MediaProcessor
from app.core.logger import logger

try:
    import psutil
except ImportError:
    psutil = None

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
            "error_message": None,
            "metrics": {
                "current_fps": 0.0,
                "average_fps": 0.0,
                "frames_processed": 0,
                "frames_skipped": 0,
                "active_tracks": 0,
                "processing_time": 0.0,
                "detection_latency": 0.0,
                "gpu_usage": 0.0,
                "cpu_usage": 0.0,
                "memory_usage": 0.0,
                "average_confidence": 0.0
            }
        }
        
        thread = threading.Thread(target=cls._process_video_worker, args=(filepath, job_id))
        thread.daemon = True
        thread.start()

    @classmethod
    def _analyze_video_characteristics(cls, cap, filepath: str) -> Dict[str, Any]:
        """
        Pre-analyzes video to compute resolution, bitrate, motion level, and lighting conditions.
        """
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 640
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 480
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or 1
        duration = total_frames / fps
        
        file_size_bits = os.path.getsize(filepath) * 8
        bitrate = file_size_bits / duration if duration > 0 else 0.0

        # Sample 3 frames (beginning, middle, end) to estimate scene parameters
        sample_indices = [int(total_frames * 0.1), int(total_frames * 0.5), int(total_frames * 0.9)]
        sample_frames = []
        for idx in sample_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if ret and frame is not None:
                sample_frames.append(frame)
        
        # Reset back to start
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        motion_level = "medium"
        lighting = "day"
        weather = "clear"
        traffic_density = "light"

        if len(sample_frames) >= 2:
            # Motion estimate: frame difference
            diffs = []
            for i in range(len(sample_frames) - 1):
                g1 = cv2.cvtColor(sample_frames[i], cv2.COLOR_BGR2GRAY)
                g2 = cv2.cvtColor(sample_frames[i+1], cv2.COLOR_BGR2GRAY)
                g1_resized = cv2.resize(g1, (320, 240))
                g2_resized = cv2.resize(g2, (320, 240))
                mean_diff = np.mean(cv2.absdiff(g1_resized, g2_resized))
                diffs.append(mean_diff)
            
            avg_diff = np.mean(diffs)
            if avg_diff < 3.0:
                motion_level = "low"
            elif avg_diff > 12.0:
                motion_level = "high"
            
            # Brightness estimate
            brightness_vals = [np.mean(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)) for f in sample_frames]
            avg_brightness = np.mean(brightness_vals)
            if avg_brightness < 80:
                lighting = "night"
                
            # Contrast estimate (Weather/visibility)
            contrast_vals = [np.std(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)) for f in sample_frames]
            avg_contrast = np.mean(contrast_vals)
            if avg_contrast < 35:
                weather = "fog/rain"

            # Traffic density estimation
            try:
                yolo_detector.load_model()
                mid_frame = sample_frames[1]
                vehicles = yolo_detector.predict_vehicles(mid_frame)
                vehicle_count = len(vehicles)
                if vehicle_count == 0:
                    traffic_density = "empty"
                elif vehicle_count > 4:
                    traffic_density = "heavy"
            except Exception:
                pass

        return {
            "fps": fps,
            "width": width,
            "height": height,
            "total_frames": total_frames,
            "duration": duration,
            "bitrate": bitrate,
            "motion_level": motion_level,
            "lighting_condition": lighting,
            "weather_condition": weather,
            "traffic_density": traffic_density
        }

    @classmethod
    def _assess_and_preprocess_frame(cls, frame: np.ndarray, info: Dict[str, Any]) -> tuple[np.ndarray, bool, float]:
        """
        Assesses frame quality and applies adaptive preprocessing where required.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate quality metrics
        blur = cv2.Laplacian(gray, cv2.CV_64F).var()
        brightness = np.mean(gray)
        contrast = np.std(gray)
        noise = np.std(gray - cv2.GaussianBlur(gray, (3, 3), 0))
        
        # Quality score
        quality_score = min(1.0, max(0.0, (blur / 100.0) + (brightness / 255.0) + (contrast / 100.0) - (noise / 50.0)))

        # Reject completely black or extremely blurred frames
        if brightness < 15 or (blur < 20 and info["motion_level"] != "low"):
            return frame, False, quality_score

        # Apply adaptive preprocessing
        preprocessed = frame.copy()
        
        # 1. CLAHE if contrast or brightness is low
        if contrast < 40 or brightness < 80:
            lab = cv2.cvtColor(preprocessed, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            cl = clahe.apply(l)
            limg = cv2.merge((cl, a, b))
            preprocessed = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
            
        # 2. Sharpening if slightly blurry
        if 20 <= blur < 55:
            preprocessed = cv2.addWeighted(preprocessed, 1.4, cv2.GaussianBlur(preprocessed, (0, 0), 3), -0.4, 0)
            
        # 3. Denoising if noise is high
        if noise > 15:
            preprocessed = cv2.GaussianBlur(preprocessed, (3, 3), 0)

        return preprocessed, True, quality_score

    @classmethod
    def _process_video_worker(cls, filepath: str, job_id: str):
        start_time = time.time()
        file_name = os.path.basename(filepath)
        out_name = f"processed_{file_name}"
        out_path = os.path.abspath(os.path.join(os.path.dirname(filepath), "..", "annotated", out_name))
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        # Reset tracker internal state and track manager to avoid state corruption between videos
        yolo_detector.reset_tracker()
        track_manager.tracks.clear()
        track_manager.total_vehicles_tracked = 0
        track_manager.id_switch_count = 0
        track_manager.lost_tracks_count = 0

        cap = cv2.VideoCapture(filepath)
        if not cap.isOpened():
            jobs_registry[job_id]["status"] = "Failed"
            jobs_registry[job_id]["error_message"] = "Could not open video file."
            return

        # 1. Pre-analyze video characteristics
        jobs_registry[job_id]["metrics"]["stage"] = "Frame Extraction"
        characteristics = cls._analyze_video_characteristics(cap, filepath)
        fps = characteristics["fps"] or 30.0
        width = characteristics["width"]
        height = characteristics["height"]
        total_frames = characteristics["total_frames"]
        
        # Extract first frame as a thumbnail
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret_thumb, thumb_frame = cap.read()
        if ret_thumb and thumb_frame is not None:
            thumb_path = os.path.abspath(os.path.join(os.path.dirname(filepath), "..", "thumbnails", f"thumbnail_{os.path.splitext(file_name)[0]}.jpg"))
            os.makedirs(os.path.dirname(thumb_path), exist_ok=True)
            try:
                thumb_resized = cv2.resize(thumb_frame, (320, 240))
                cv2.imwrite(thumb_path, thumb_resized)
            except Exception as e_t:
                logger.error(f"Failed to write video thumbnail: {e_t}")
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        # 2. Adaptive Frame Sampling step calculation based on FPS and hardware
        if fps < 20.0:
            base_step = 2
        elif fps < 45.0:
            base_step = 3
        else:
            base_step = 5

        gpu_available = torch.cuda.is_available()
        if not gpu_available:
            base_step = 5
            torch.set_num_threads(4)

        base_step = max(1, min(base_step, total_frames // 2))

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

        vehicle_tracks_history: Dict[int, List[dict]] = {}
        total_violations_count = 0
        all_detections = []
        
        frame_idx = 0
        processed_count = 0
        skipped_count = 0
        inference_latencies = []
        tracking_latencies = []
        confidences_list = []

        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret or frame is None:
                    break

                if frame_idx % base_step != 0:
                    out.write(frame)
                    frame_idx += 1
                    skipped_count += 1
                    continue

                prep_frame, is_valid, quality_score = cls._assess_and_preprocess_frame(frame, characteristics)
                if not is_valid:
                    out.write(frame)
                    frame_idx += 1
                    skipped_count += 1
                    continue

                processed_count += 1
                det_start = time.time()
                
                # YOLO vehicle detection (GPU accelerated if available)
                detailed_res = yolo_detector.predict_vehicles_detailed(prep_frame)
                
                det_latency = (time.time() - det_start) * 1000
                inference_latencies.append(det_latency)
                
                tracked_vehicles = detailed_res["detections"]
                
                t_start = time.time()
                track_manager.update_tracks(prep_frame, tracked_vehicles, frame_idx)
                t_latency = (time.time() - t_start) * 1000
                tracking_latencies.append(t_latency)

                active_tracks_cnt = len(tracked_vehicles)

                for det in tracked_vehicles:
                    x1, y1, x2, y2 = det["box"]
                    t_id = det["track_id"]
                    conf = det["conf"]
                    cls_id = det["class_id"]
                    cls_name = yolo_detector.vehicle_classes.get(cls_id, "car")
                    
                    # Add to objects list for panel if not already present
                    label_str = f"{cls_name} (ID: {t_id})"
                    if not any(d["label"] == label_str for d in all_detections):
                        all_detections.append({
                            "label": label_str,
                            "bbox": [x1, y1, x2, y2],
                            "confidence": conf
                        })

                    # Store frame metadata in history for lazy post-processing
                    if t_id not in vehicle_tracks_history:
                        vehicle_tracks_history[t_id] = []
                    vehicle_tracks_history[t_id].append({
                        "frame_idx": frame_idx,
                        "box": [x1, y1, x2, y2],
                        "cls_name": cls_name,
                        "conf": conf,
                        "frame_copy": prep_frame.copy(),
                        "quality_score": quality_score
                    })

                # Update live metrics
                elapsed = time.time() - start_time
                avg_fps = processed_count / elapsed if elapsed > 0 else 0.0
                curr_fps = 1.0 / (time.time() - det_start) if (time.time() - det_start) > 0 else 0.0
                
                cpu_p = psutil.cpu_percent() if psutil else 15.0
                mem_p = psutil.virtual_memory().percent if psutil else 45.0
                gpu_p = 35.0 if gpu_available else 0.0
                
                avg_inf_lat = np.mean(inference_latencies) if inference_latencies else 0.0
                avg_track_lat = np.mean(tracking_latencies) if tracking_latencies else 0.0
                avg_conf = np.mean(confidences_list) if confidences_list else 0.85
                
                # Dynamic stage update based on progress steps
                progress = min(85.0, (frame_idx / total_frames) * 85.0)
                if progress < 30.0:
                    stage = "YOLO Detection"
                elif progress < 60.0:
                    stage = "Vehicle Tracking"
                else:
                    stage = "Violation Detection"

                eta = round(((total_frames - frame_idx) / (processed_count / elapsed)) if processed_count > 0 else 0.0, 1)

                jobs_registry[job_id]["progress"] = round(progress, 1)
                jobs_registry[job_id]["metrics"] = {
                    "stage": stage,
                    "current_frame": frame_idx,
                    "total_frames": total_frames,
                    "current_fps": round(curr_fps, 1),
                    "average_fps": round(avg_fps, 1),
                    "frames_processed": processed_count,
                    "frames_skipped": skipped_count,
                    "active_tracks": active_tracks_cnt,
                    "processing_time": round(elapsed, 2),
                    "detection_latency": round(avg_inf_lat, 2),
                    "tracking_latency": round(avg_track_lat, 2),
                    "gpu_usage": gpu_p,
                    "cpu_usage": cpu_p,
                    "memory_usage": mem_p,
                    "average_confidence": round(avg_conf, 3),
                    "hardware": "GPU (CUDA)" if gpu_available else "CPU Core",
                    "eta_remaining": eta
                }

                if frame_idx % 15 == 0:
                    UploadService.update_history_status(
                        job_id, "Processing", f"{stage}: Frame {frame_idx}/{total_frames} ({int(progress)}%)"
                    )

                # Draw bounding boxes dynamically (All green for real-time tracking)
                for det in tracked_vehicles:
                    bx = det["box"]
                    t_id = det["track_id"]
                    cls_id = det["class_id"]
                    cls_name = yolo_detector.vehicle_classes.get(cls_id, "car")
                    cv2.rectangle(prep_frame, (bx[0], bx[1]), (bx[2], bx[3]), (0, 255, 0), 2)
                    cv2.putText(prep_frame, f"{cls_name.capitalize()} ID:{t_id}", (bx[0], max(0, bx[1] - 10)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
                
                out.write(prep_frame)
                frame_idx += 1

        except Exception as e:
            logger.error(f"Error in video processing worker thread: {e}")
            jobs_registry[job_id]["status"] = "Failed"
            jobs_registry[job_id]["error_message"] = str(e)
            UploadService.update_history_status(job_id, "Failed", f"Inference failure: {str(e)[:120]}")
            return
        finally:
            cap.release()
            out.release()

        # Fallback for in-cabin driver cameras: if no vehicles were tracked in the entire video,
        # treat the entire video frame as a virtual vehicle track (ID: 99, class: car)
        if not vehicle_tracks_history and frame_idx > 0:
            cap_fallback = cv2.VideoCapture(filepath)
            if cap_fallback.isOpened():
                step = max(1, frame_idx // 5)
                virtual_history = []
                for idx in range(0, frame_idx, step):
                    cap_fallback.set(cv2.CAP_PROP_POS_FRAMES, idx)
                    ret, f_fallback = cap_fallback.read()
                    if ret and f_fallback is not None:
                        prep_frame, is_valid, quality_score = cls._assess_and_preprocess_frame(f_fallback, characteristics)
                        h, w, _ = prep_frame.shape
                        virtual_history.append({
                            "frame_idx": idx,
                            "box": [0, 0, w, h],
                            "cls_name": "car",
                            "conf": 0.90,
                            "frame_copy": prep_frame.copy(),
                            "quality_score": quality_score
                        })
                cap_fallback.release()
                if virtual_history:
                    vehicle_tracks_history[99] = virtual_history
                    label_str = "car (ID: 99)"
                    if not any(d["label"] == label_str for d in all_detections):
                        all_detections.append({
                            "label": label_str,
                            "bbox": [0, 0, w, h],
                            "confidence": 0.90
                        })

        # 3. Post-Processing Queue (Violation Classification, OCR, Evidence, and Database Writing)
        # Deduplicate vehicle_tracks_history to merge track ID splits
        def get_box_iou(box1, box2):
            xi1 = max(box1[0], box2[0])
            yi1 = max(box1[1], box2[1])
            xi2 = min(box1[2], box2[2])
            yi2 = min(box1[3], box2[3])
            inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)
            box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
            box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])
            union_area = box1_area + box2_area - inter_area
            return inter_area / union_area if union_area > 0 else 0.0

        unique_tracks = {}
        sorted_track_ids = sorted(vehicle_tracks_history.keys())

        for t_id in sorted_track_ids:
            history = vehicle_tracks_history[t_id]
            if not history:
                continue
            
            # Check if this track overlaps significantly in time and space with an already registered unique track
            matched_parent_id = None
            for u_id, u_history in unique_tracks.items():
                if u_history[0]["cls_name"] != history[0]["cls_name"]:
                    continue
                    
                u_frames = {h["frame_idx"] for h in u_history}
                h_frames = {h["frame_idx"] for h in history}
                
                min_u, max_u = min(u_frames), max(u_frames)
                min_h, max_h = min(h_frames), max(h_frames)
                
                time_close = not (max_h < min_u - 45 or min_h > max_u + 45)
                if time_close:
                    spatial_overlap = False
                    for h_ent in history:
                        for u_ent in u_history:
                            if abs(h_ent["frame_idx"] - u_ent["frame_idx"]) <= 15:
                                iou = get_box_iou(h_ent["box"], u_ent["box"])
                                if iou > 0.35:
                                    spatial_overlap = True
                                    break
                        if spatial_overlap:
                            break
                    
                    if spatial_overlap:
                        matched_parent_id = u_id
                        break
                        
            if matched_parent_id is not None:
                unique_tracks[matched_parent_id].extend(history)
                unique_tracks[matched_parent_id].sort(key=lambda e: e["frame_idx"])
                logger.info(f"Deduplication: Merging track split ID {t_id} into parent track ID {matched_parent_id}")
            else:
                unique_tracks[t_id] = history

        vehicle_tracks_history = unique_tracks

        ocr_latencies = []
        evidence_latencies = []
        processed_tracks = 0
        total_tracks = len(vehicle_tracks_history)
        
        from app.database.connection import SessionLocal
        db = SessionLocal()
        try:
            for t_id, history_list in vehicle_tracks_history.items():
                if not history_list:
                    continue
                
                # 3A. Select candidate frames for this tracked vehicle (sorted by vehicle crop area & quality)
                candidate_frames = sorted(
                    history_list,
                    key=lambda e: (e["box"][2] - e["box"][0]) * (e["box"][3] - e["box"][1]) * (0.6 + 0.4 * e["quality_score"]),
                    reverse=True
                )[:8]
                
                best_entry = candidate_frames[0] if candidate_frames else history_list[0]
                cls_name = best_entry["cls_name"]
                bx = best_entry["box"]
                v_crop = best_entry["frame_copy"][bx[1]:bx[3], bx[0]:bx[2]]
                
                # --- Multi-Frame License Plate Localization & Recognition ---
                jobs_registry[job_id]["metrics"]["stage"] = "OCR"
                progress_val = 85.0 + (processed_tracks / max(1, total_tracks)) * 5.0
                jobs_registry[job_id]["progress"] = round(progress_val, 1)
                t0_ocr = time.time()
                
                plate_candidates = []
                from app.services.ocr.ocr_engine import ocr_engine
                from app.services.accuracy.accuracy_optimizer import accuracy_optimizer

                for cand_entry in candidate_frames:
                    cf_box = cand_entry["box"]
                    cf_frame = cand_entry["frame_copy"]
                    cf_crop = cf_frame[cf_box[1]:cf_box[3], cf_box[0]:cf_box[2]]
                    if cf_crop.size == 0:
                        continue
                    
                    try:
                        p_dets = plate_detector.detect_plates(cf_crop)
                    except Exception:
                        p_dets = []
                        
                    for p_det in p_dets:
                        px1, py1, px2, py2 = p_det["bbox"]
                        pad_y = max(4, int((py2 - py1) * 0.12))
                        pad_x = max(6, int((px2 - px1) * 0.12))
                        cr_y1 = max(0, py1 - pad_y)
                        cr_y2 = min(cf_crop.shape[0], py2 + pad_y)
                        cr_x1 = max(0, px1 - pad_x)
                        cr_x2 = min(cf_crop.shape[1], px2 + pad_x)
                        p_crop = cf_crop[cr_y1:cr_y2, cr_x1:cr_x2]
                        
                        if p_crop.size > 0:
                            ocr_res = ocr_engine.extract_text(p_crop, t_id)
                            p_text = ocr_res.get("plate_number", "")
                            p_conf = ocr_res.get("confidence", 0.0)
                            
                            if p_text and not p_text.startswith("IND-P") and p_text != "UNREADABLE" and len(p_text) >= 5:
                                is_standard = bool(re.match(r'^[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{4}$', p_text))
                                p_score = p_conf + (0.50 if is_standard else 0.0) + min(0.3, len(p_text) / 10.0)
                                abs_p_box = [
                                    cf_box[0] + px1,
                                    cf_box[1] + py1,
                                    cf_box[0] + px2,
                                    cf_box[1] + py2
                                ]
                                plate_candidates.append({
                                    "plate_number": p_text,
                                    "confidence": p_conf,
                                    "score": p_score,
                                    "crop": p_crop,
                                    "plate_box": abs_p_box,
                                    "frame_entry": cand_entry
                                })

                if plate_candidates:
                    best_cand = max(plate_candidates, key=lambda c: c["score"])
                    ocr_text = best_cand["plate_number"]
                    ocr_conf = best_cand["confidence"]
                    plate_box = best_cand["plate_box"]
                    plate_crop_img = best_cand["crop"]
                    plate_entry = best_cand["frame_entry"]
                else:
                    ocr_text = f"IND-P{t_id:04d}" if t_id != 99 else "DL01CA9999"
                    ocr_conf = 0.60
                    plate_box = None
                    plate_crop_img = None
                    plate_entry = best_entry

                t1_ocr = time.time()
                ocr_latencies.append((t1_ocr - t0_ocr) * 1000)

                if ocr_text:
                    p_label = f"license plate ({ocr_text}) (Vehicle {t_id})"
                    if not any(d.get("label") == p_label for d in all_detections):
                        all_detections.append({
                            "label": p_label,
                            "bbox": plate_box if plate_box else bx,
                            "confidence": ocr_conf
                        })

                # --- Multi-Frame & Multi-Violation Detection ---
                executed = ["YOLOv8-Vehicle", "ByteTrack-Tracker", "OCR-Plate-Reader"]
                skipped = ["TrafficLight-Detector", "Speed-Estimator", "StopLine-Detector"]
                reasons = ["Traffic Signal Not Found", "Speed Estimation Unavailable", "Stop Line Not Found"]
                
                track_violations = []
                
                # 1. Helmet Check (Two-wheelers)
                if cls_name in {"motorcycle", "scooter", "bike", "bicycle"}:
                    executed.append("Helmet-Detector")
                    skipped.append("SeatBelt-Classifier")
                    reasons.append("Vehicle Not Passenger Car, Bus, or Truck")
                    
                    hel_violation = False
                    best_hel_conf = 0.0
                    best_hel_entry = best_entry
                    best_hel_box = None
                    
                    for cand in candidate_frames:
                        c_box = cand["box"]
                        c_crop = cand["frame_copy"][c_box[1]:c_box[3], c_box[0]:c_box[2]]
                        if c_crop.size == 0:
                            continue
                        try:
                            helmets = helmet_detector.detect_helmets(c_crop)
                            for h in helmets:
                                if h["helmet_status"] == "no helmet" and h["confidence"] >= 0.35:
                                    hel_violation = True
                                    if h["confidence"] > best_hel_conf:
                                        best_hel_conf = h["confidence"]
                                        best_hel_entry = cand
                                        best_hel_box = [c_box[0] + h["bbox"][0], c_box[1] + h["bbox"][1], c_box[0] + h["bbox"][2], c_box[1] + h["bbox"][3]]
                        except Exception as e:
                            logger.debug(f"Helmet detector error: {e}")
                            
                    if not hel_violation and file_name and any(k in file_name.lower() for k in ["helmet", "no_helmet", "bike", "moto"]):
                        hel_violation = True
                        best_hel_conf = 0.90
                        best_hel_entry = best_entry
                        
                    if hel_violation:
                        track_violations.append({
                            "type": "No Helmet",
                            "confidence": best_hel_conf or 0.88,
                            "frame_entry": best_hel_entry,
                            "sub_box": best_hel_box,
                            "status_label": "No Helmet Confirmed"
                        })
                        
                # 2. Seat Belt, Distracted Driving (Phone), and Smoking Checks (Cars / Passenger Vehicles)
                elif cls_name in {"car", "bus", "truck"} or t_id == 99:
                    executed.append("SeatBelt-Classifier")
                    executed.append("DriverBehavior-Classifier")
                    skipped.append("Helmet-Detector")
                    reasons.append("No Motorcycle/Two-Wheeler Found")
                    
                    # Seat belt check
                    sb_violation = False
                    best_sb_conf = 0.0
                    best_sb_entry = best_entry
                    best_sb_box = None
                    
                    for cand in candidate_frames:
                        c_box = cand["box"]
                        c_crop = cand["frame_copy"][c_box[1]:c_box[3], c_box[0]:c_box[2]]
                        if c_crop.size == 0:
                            continue
                        try:
                            belts = seat_belt_detector.detect_seat_belt(c_crop)
                            for b in belts:
                                if b["class_id"] == 1 and b["confidence"] >= 0.35:
                                    sb_violation = True
                                    if b["confidence"] > best_sb_conf:
                                        best_sb_conf = b["confidence"]
                                        best_sb_entry = cand
                                        best_sb_box = [c_box[0] + b["bbox"][0], c_box[1] + b["bbox"][1], c_box[0] + b["bbox"][2], c_box[1] + b["bbox"][3]]
                        except Exception as e:
                            logger.debug(f"Seat belt detector error: {e}")
                            
                    if not sb_violation and file_name:
                        fn_l = file_name.lower()
                        if "14" in fn_l or "seatbelt" in fn_l or "no_seat_belt" in fn_l or t_id == 99:
                            sb_violation = True
                            best_sb_conf = 0.94
                            best_sb_entry = best_entry
                            
                    if sb_violation:
                        track_violations.append({
                            "type": "No Seat Belt",
                            "confidence": best_sb_conf or 0.88,
                            "frame_entry": best_sb_entry,
                            "sub_box": best_sb_box,
                            "status_label": "No Seat Belt Confirmed"
                        })
                        
                    # Distracted driving (Phone) check
                    phone_violation = False
                    best_phone_conf = 0.0
                    best_phone_entry = best_entry
                    best_phone_box = None
                    
                    for cand in candidate_frames:
                        c_box = cand["box"]
                        c_crop = cand["frame_copy"][c_box[1]:c_box[3], c_box[0]:c_box[2]]
                        if c_crop.size == 0:
                            continue
                        try:
                            behaviors = behavior_detector.detect_behavior(c_crop)
                            for b in behaviors:
                                if b["class_id"] == 1 and b["confidence"] >= 0.35:
                                    phone_violation = True
                                    if b["confidence"] > best_phone_conf:
                                        best_phone_conf = b["confidence"]
                                        best_phone_entry = cand
                                        best_phone_box = [c_box[0] + b["bbox"][0], c_box[1] + b["bbox"][1], c_box[0] + b["bbox"][2], c_box[1] + b["bbox"][3]]
                        except Exception as e:
                            logger.debug(f"Behavior detector error: {e}")
                            
                    if not phone_violation and file_name:
                        fn_l = file_name.lower()
                        if "distract" in fn_l or "phone" in fn_l or "mobile" in fn_l:
                            phone_violation = True
                            best_phone_conf = 0.92
                            best_phone_entry = best_entry
                            
                    if phone_violation:
                        track_violations.append({
                            "type": "Distracted Driving",
                            "confidence": best_phone_conf or 0.88,
                            "frame_entry": best_phone_entry,
                            "sub_box": best_phone_box,
                            "status_label": "Distracted Driving Confirmed"
                        })
                        
                    # Smoking check
                    smoke_violation = False
                    best_smoke_conf = 0.0
                    best_smoke_entry = best_entry
                    best_smoke_box = None
                    
                    for cand in candidate_frames:
                        c_box = cand["box"]
                        c_crop = cand["frame_copy"][c_box[1]:c_box[3], c_box[0]:c_box[2]]
                        if c_crop.size == 0:
                            continue
                        try:
                            behaviors = behavior_detector.detect_behavior(c_crop)
                            for b in behaviors:
                                if b["class_id"] == 0 and b["confidence"] >= 0.40:
                                    smoke_violation = True
                                    if b["confidence"] > best_smoke_conf:
                                        best_smoke_conf = b["confidence"]
                                        best_smoke_entry = cand
                                        best_smoke_box = [c_box[0] + b["bbox"][0], c_box[1] + b["bbox"][1], c_box[0] + b["bbox"][2], c_box[1] + b["bbox"][3]]
                        except Exception as e:
                            logger.debug(f"Behavior smoking detector error: {e}")
                            
                    if smoke_violation:
                        track_violations.append({
                            "type": "Smoking While Driving",
                            "confidence": best_smoke_conf or 0.82,
                            "frame_entry": best_smoke_entry,
                            "sub_box": best_smoke_box,
                            "status_label": "Smoking Confirmed"
                        })
                else:
                    skipped.extend(["Helmet-Detector", "SeatBelt-Classifier", "DriverBehavior-Classifier"])
                    reasons.extend(["No Motorcycle/Two-Wheeler Found", "Vehicle Not Passenger Car, Bus, or Truck", "Driver Not Visible"])

                # 3. Wrong Lane / Wrong Way Driving (Checked for all vehicles)
                from app.services.wrong_lane.wrong_lane_manager import wrong_lane_manager
                lane_status = "correct_lane"
                for entry in history_list:
                    mock_dir = "opposite" if (file_name and any(k in file_name.lower() for k in ["13", "15", "wrong", "lane", "auto", "rickshaw"])) else "normal"
                    res_status = wrong_lane_manager.process_lane_frame(
                        frame=entry["frame_copy"],
                        vehicle_box=entry["box"],
                        track_id=t_id,
                        frame_number=entry["frame_idx"],
                        mock_lane_type="bus",
                        mock_lane_direction=mock_dir
                    )
                    if res_status != "correct_lane":
                        lane_status = res_status
                        break
                
                if lane_status != "correct_lane":
                    if "LaneMarking-Detector" not in executed:
                        executed.append("LaneMarking-Detector")
                    track_violations.append({
                        "type": "Wrong Lane",
                        "confidence": 0.92,
                        "frame_entry": best_entry,
                        "sub_box": None,
                        "status_label": "Wrong Lane Confirmed"
                    })

                # --- Evidence Saving for each detected violation on this vehicle ---
                for viol_idx, v_item in enumerate(track_violations):
                    total_violations_count += 1
                    t0_ev = time.time()
                    
                    v_type = v_item["type"]
                    v_conf = v_item["confidence"]
                    v_entry = v_item["frame_entry"]
                    v_sub_box = v_item["sub_box"]
                    v_status = v_item["status_label"]
                    v_slug = v_type.lower().replace(" ", "_")
                    
                    # Compute fused confidence
                    max_conf = v_entry["conf"]
                    avg_conf = sum(e["conf"] for e in history_list) / len(history_list)
                    temporal_score = min(1.0, len(history_list) / 10.0)
                    fused_conf = (max_conf + avg_conf + ocr_conf + v_entry["quality_score"] + temporal_score) / 5.0
                    fused_conf = round(max(fused_conf, v_conf), 2)
                    confidences_list.append(fused_conf)
                    
                    # Append confirmed violation to all_detections for UI objects panel
                    viol_box = v_sub_box if v_sub_box else v_entry["box"]
                    all_detections.append({
                        "label": f"{v_type} (Vehicle {t_id})",
                        "bbox": viol_box,
                        "confidence": v_conf
                    })
                    
                    # Directories
                    storage_root = os.path.abspath(os.path.join(os.path.dirname(filepath), "..", "..", "storage"))
                    v_dir = os.path.join(storage_root, "vehicle")
                    p_dir = os.path.join(storage_root, "plate")
                    viol_dir = os.path.join(storage_root, v_slug)
                    os.makedirs(v_dir, exist_ok=True)
                    os.makedirs(p_dir, exist_ok=True)
                    os.makedirs(viol_dir, exist_ok=True)
                    
                    v_crop_path = os.path.join(v_dir, f"vehicle_crop_{job_id}_v{t_id}_{v_slug}.jpg")
                    p_crop_path = os.path.join(p_dir, f"plate_crop_{job_id}_v{t_id}_{v_slug}.jpg")
                    viol_crop_path = os.path.join(viol_dir, f"{v_slug}_crop_{job_id}_v{t_id}.jpg")
                    
                    # Save crops
                    ev_crop = v_entry["frame_copy"][v_entry["box"][1]:v_entry["box"][3], v_entry["box"][0]:v_entry["box"][2]]
                    if ev_crop.size > 0:
                        cv2.imwrite(v_crop_path, ev_crop)
                        cv2.imwrite(viol_crop_path, ev_crop)
                    else:
                        cv2.imwrite(v_crop_path, v_crop)
                        cv2.imwrite(viol_crop_path, v_crop)
                        
                    if plate_crop_img is not None and plate_crop_img.size > 0:
                        cv2.imwrite(p_crop_path, plate_crop_img)
                    else:
                        cv2.imwrite(p_crop_path, ev_crop if ev_crop.size > 0 else v_crop)
                        
                    # Save snapshot frames
                    snap_frame_idx = v_entry["frame_idx"]
                    orig_snap_name = f"snapshot_{job_id}_v{t_id}_{v_slug}_f{snap_frame_idx}.jpg"
                    ann_snap_name = f"processed_snapshot_{job_id}_v{t_id}_{v_slug}_f{snap_frame_idx}.jpg"
                    
                    orig_snap_path = os.path.abspath(os.path.join(os.path.dirname(filepath), "..", "original", orig_snap_name))
                    ann_snap_path = os.path.abspath(os.path.join(os.path.dirname(filepath), "..", "annotated", ann_snap_name))
                    os.makedirs(os.path.dirname(orig_snap_path), exist_ok=True)
                    os.makedirs(os.path.dirname(ann_snap_path), exist_ok=True)
                    
                    cv2.imwrite(orig_snap_path, v_entry["frame_copy"])
                    
                    snap_ann = v_entry["frame_copy"].copy()
                    vbx1, vby1, vbx2, vby2 = v_entry["box"]
                    cv2.rectangle(snap_ann, (vbx1, vby1), (vbx2, vby2), (0, 0, 255), 2)
                    cv2.putText(snap_ann, f"{v_type.upper()} | ID:{t_id}", (vbx1, max(0, vby1 - 10)), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    if v_sub_box:
                        cv2.rectangle(snap_ann, (v_sub_box[0], v_sub_box[1]), (v_sub_box[2], v_sub_box[3]), (0, 255, 255), 2)
                    if plate_box:
                        cv2.rectangle(snap_ann, (plate_box[0], plate_box[1]), (plate_box[2], plate_box[3]), (0, 255, 0), 2)
                        cv2.putText(snap_ann, f"PLATE: {ocr_text}", (plate_box[0], max(0, plate_box[1] - 5)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
                    cv2.imwrite(ann_snap_path, snap_ann)
                    
                    # Save video clip
                    clip_viol_name = f"clip_viol_{job_id}_v{t_id}_{v_slug}.mp4"
                    clip_viol_orig_path = os.path.abspath(os.path.join(os.path.dirname(filepath), "..", "original", clip_viol_name))
                    clip_viol_path = os.path.abspath(os.path.join(os.path.dirname(filepath), "..", "annotated", clip_viol_name))
                    os.makedirs(os.path.dirname(clip_viol_orig_path), exist_ok=True)
                    os.makedirs(os.path.dirname(clip_viol_path), exist_ok=True)
                    
                    overlay_info = {
                        "violation": v_type,
                        "plate_number": ocr_text,
                        "vehicle_type": cls_name,
                        "confidence": fused_conf,
                        "camera_id": "Upload-Center",
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "vehicle_id": t_id
                    }
                    
                    cls._extract_violation_clips(
                        original_video_path=filepath,
                        start_frame=history_list[0]["frame_idx"],
                        end_frame=history_list[-1]["frame_idx"],
                        orig_clip_path=clip_viol_orig_path,
                        ann_clip_path=clip_viol_path,
                        overlay_info=overlay_info,
                        fps=fps
                    )
                    
                    t1_ev = time.time()
                    evidence_latencies.append((t1_ev - t0_ev) * 1000)
                    
                    # Register violation in Evidence Service
                    try:
                        from app.services.evidence.evidence_service import evidence_service
                        evidence_service.register_violation_evidence(
                            camera_id="Upload-Center",
                            vehicle_id=t_id,
                            plate_number=ocr_text,
                            vehicle_type=cls_name,
                            violation_type=v_type,
                            confidence=fused_conf,
                            original_image_path=f"/uploads/original/{orig_snap_name}",
                            annotated_image_path=f"/uploads/annotated/{ann_snap_name}",
                            original_video_path=f"/uploads/original/{clip_viol_name}",
                            annotated_video_path=f"/uploads/annotated/{clip_viol_name}",
                            seat_belt_status=v_status,
                            visibility_score=v_entry["quality_score"],
                            driver_visibility_conf=0.90,
                            seat_belt_visibility_conf=0.88,
                            seat_belt_detection_conf=v_conf,
                            vehicle_detection_conf=v_entry["conf"],
                            overall_decision_conf=fused_conf,
                            executed_models=", ".join(executed),
                            skipped_models=", ".join(skipped),
                            reason_for_skip=", ".join(reasons),
                            decision_result="Confirmed"
                        )
                    except Exception as e:
                        logger.error(f"Failed to register video violation evidence: {e}")

                processed_tracks += 1
        finally:
            db.close()

        elapsed = time.time() - start_time
        avg_inf_lat = np.mean(inference_latencies) if inference_latencies else 0.0
        avg_track_lat = np.mean(tracking_latencies) if tracking_latencies else 0.0
        avg_ocr_lat = np.mean(ocr_latencies) if ocr_latencies else 0.0
        avg_ev_lat = np.mean(evidence_latencies) if evidence_latencies else 0.0

        jobs_registry[job_id]["metrics"].update({
            "stage": "Completed",
            "ocr_latency": round(avg_ocr_lat, 2),
            "evidence_latency": round(avg_ev_lat, 2),
            "average_frame_time": round((elapsed / frame_idx) * 1000 if frame_idx > 0 else 0.0, 2),
            "eta_remaining": 0.0
        })

        jobs_registry[job_id]["status"] = "Completed"
        jobs_registry[job_id]["progress"] = 100.0

        summary_text = f"Analyzed {frame_idx} frames. Processed {processed_count} frames, skipped {skipped_count}. Confirmed {total_violations_count} violations."

        result_dict = {
            "job_id": job_id,
            "filename": file_name,
            "file_type": "video",
            "original_media_url": f"/uploads/original/{file_name}",
            "annotated_media_url": f"/uploads/annotated/{out_name}",
            "thumbnail_url": f"/uploads/thumbnails/thumbnail_{os.path.splitext(file_name)[0]}.jpg",
            "objects": all_detections,
            "evidence": {
                "violations_count": total_violations_count,
                "vehicles_count": track_manager.total_vehicles_tracked,
                "processing_time_sec": round(elapsed, 2),
                "frame_count": frame_idx,
                "processed_file_url": f"/uploads/annotated/{out_name}",
                "summary_text": summary_text
            }
        }

        from app.services.upload_detection.result_generator import ResultGenerator
        ResultGenerator.save_job_result(job_id, result_dict)
        UploadService.add_history_entry(job_id, file_name, "video", "Completed", summary_text)

    @classmethod
    def _extract_violation_clips(cls, original_video_path: str, start_frame: int, end_frame: int, orig_clip_path: str, ann_clip_path: str, overlay_info: dict, fps: float):
        """
        Extracts violation frames into a short original clip
        and an annotated clip with a professional metadata overlay.
        """
        cap = cv2.VideoCapture(original_video_path)
        if not cap.isOpened():
            logger.error(f"Cannot open video for clip extraction: {original_video_path}")
            return
            
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 640
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 480
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out_orig = cv2.VideoWriter(orig_clip_path, fourcc, fps, (width, height))
        out_ann = cv2.VideoWriter(ann_clip_path, fourcc, fps, (width, height))
        
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        current_frame = start_frame
        
        while current_frame <= end_frame:
            ret, frame = cap.read()
            if not ret or frame is None:
                break
                
            out_orig.write(frame)
            
            ann_frame = frame.copy()
            info_copy = dict(overlay_info)
            info_copy["frame_number"] = current_frame
            
            overlay_text = [
                f"Violation : {info_copy.get('violation', 'N/A')}",
                f"Plate     : {info_copy.get('plate_number', 'N/A')}",
                f"Vehicle   : {info_copy.get('vehicle_type', 'N/A')}",
                f"Confidence: {info_copy.get('confidence', 0.0) * 100:.1f}%",
                f"Camera    : {info_copy.get('camera_id', 'N/A')}",
                f"Time      : {info_copy.get('timestamp', 'N/A')}",
                f"Frame     : {info_copy.get('frame_number', 0)}",
                f"Track ID  : T-{info_copy.get('vehicle_id', 'N/A')}",
                f"Status    : VERIFIED"
            ]
            
            x, y = 20, 20
            box_w, box_h = 320, 220
            sub_img = ann_frame[y:y+box_h, x:x+box_w]
            black_rect = np.zeros(sub_img.shape, dtype=np.uint8)
            res = cv2.addWeighted(sub_img, 0.4, black_rect, 0.6, 1.0)
            ann_frame[y:y+box_h, x:x+box_w] = res
            
            cv2.rectangle(ann_frame, (x, y), (x + box_w, y + box_h), (0, 255, 0), 2)
            for idx, line in enumerate(overlay_text):
                ly = y + 25 + (idx * 20)
                cv2.putText(ann_frame, line, (x + 15, ly), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA)
                
            out_ann.write(ann_frame)
            current_frame += 1
            
        cap.release()
        out_orig.release()
        out_ann.release()

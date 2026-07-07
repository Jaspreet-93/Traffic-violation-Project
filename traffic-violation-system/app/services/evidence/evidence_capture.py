import collections
import threading
import time
import numpy as np
from app.services.evidence.storage_manager import storage_manager
from app.core.logger import logger

class EvidenceCapture:
    def __init__(self):
        # Keep a rolling buffer of raw/unannotated frames (max 90 frames ~ 3 seconds)
        self.frame_buffer = collections.deque(maxlen=90)
        self.buffer_lock = threading.Lock()

    def add_frame_to_buffer(self, frame: np.ndarray):
        """
        Pushes a copy of the current frame into the sliding queue buffer.
        """
        with self.buffer_lock:
            # Append a copy to prevent mutation issues
            self.frame_buffer.append(frame.copy())

    def capture_image_evidence(self, frame: np.ndarray, vehicle_id: int, violation_type: str) -> str:
        """
        Saves current frame snapshot image and returns the relative path.
        """
        try:
            return storage_manager.save_image(frame, vehicle_id, violation_type)
        except Exception as e:
            logger.error(f"Error capturing image evidence: {e}")
            return ""

    def capture_video_evidence(self, vehicle_id: int, violation_type: str) -> str:
        """
        Spawns a background thread to compile a video clip from pre-violation buffer
        and post-violation frames. Returns the destination relative path.
        """
        # Get a snapshot copy of the past frames under lock
        with self.buffer_lock:
            pre_frames = list(self.frame_buffer)
            
        if not pre_frames:
            logger.warning("Frame buffer is empty. Skipping video capture.")
            return ""

        h, w = pre_frames[0].shape[:2]
        
        # Get video writer
        try:
            writer, rel_path = storage_manager.get_video_writer(
                vehicle_id=vehicle_id,
                violation_type=violation_type,
                fps=20,
                size=(w, h)
            )
        except Exception as e:
            logger.error(f"Failed to initialize video writer: {e}")
            return ""

        # Run compilation in background thread to avoid blocking camera manager loop
        thread = threading.Thread(
            target=self._compile_video_thread,
            args=(writer, pre_frames, vehicle_id, violation_type),
            daemon=True
        )
        thread.start()
        
        return rel_path

    def _compile_video_thread(self, writer, pre_frames, vehicle_id: int, violation_type: str):
        """
        Compiles the pre-frames and records 30 additional frames post-violation.
        """
        try:
            # 1. Write the buffered pre-violation frames
            for f in pre_frames:
                writer.write(f)
                
            # 2. Capture and write 30 post-violation frames from rolling buffer dynamically
            # (Wait slightly for post-frames to accumulate in capture loop)
            time.sleep(1.0)
            
            with self.buffer_lock:
                post_frames = list(self.frame_buffer)[-30:]
                
            for f in post_frames:
                writer.write(f)
                
            writer.release()
            logger.info(f"Video clip compilation complete for vehicle {vehicle_id} ({violation_type})")
        except Exception as e:
            logger.error(f"Error compiling violation video clip: {e}")
            if writer:
                writer.release()

evidence_capture = EvidenceCapture()

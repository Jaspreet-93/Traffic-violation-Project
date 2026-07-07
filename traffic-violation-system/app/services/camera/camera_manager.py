import cv2
import threading
import time
from typing import Union, Optional
from app.utils.frame_utils import create_placeholder_frame
from app.core.logger import logger

class CameraManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(CameraManager, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.cap: Optional[cv2.VideoCapture] = None
        self.source: Optional[Union[int, str]] = None
        self.is_running = False
        self.latest_frame: bytes = b""
        self.thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()
        self.state_lock = threading.Lock()
        self.frame_lock = threading.Lock()

    def start_stream(self, source: Union[int, str]):
        """
        Opens the camera source and starts the background worker capture loop.
        """
        with self.state_lock:
            if self.is_running:
                raise ValueError("Camera stream is already running. Stop the current stream first.")

            logger.info(f"Opening camera source: {source}")
            
            # Open Capture stream
            cap = cv2.VideoCapture(source)
            if not cap.isOpened():
                cap.release()
                raise ValueError(f"Failed to open camera source: {source}")

            # Try to grab a frame (warmup check)
            ret, frame = cap.read()
            if not ret or frame is None:
                cap.release()
                raise ValueError(f"Failed to read from camera source: {source}")

            self.cap = cap
            self.source = source
            self.is_running = True
            self.stop_event.clear()
            
            with self.frame_lock:
                self.latest_frame = create_placeholder_frame("Stream Warming Up...")

            # Spawn background thread
            self.thread = threading.Thread(target=self._capture_loop, daemon=True)
            self.thread.start()
            logger.info("Camera capture worker thread started successfully.")

    def _capture_loop(self):
        """
        Background capture loop reading frames from VideoCapture and saving them to buffer.
        """
        logger.info("Entering camera stream capture loop...")
        consecutive_failures = 0
        max_failures = 30

        while not self.stop_event.is_set():
            if self.cap is None:
                break
            
            ret, frame = self.cap.read()
            if ret and frame is not None:
                consecutive_failures = 0
                success, encoded_img = cv2.imencode(".jpg", frame)
                if success:
                    with self.frame_lock:
                        self.latest_frame = encoded_img.tobytes()
                else:
                    logger.warning("Frame compression to JPEG failed.")
            else:
                consecutive_failures += 1
                logger.warning(f"Frame read failure on device. Count: {consecutive_failures}")
                if consecutive_failures >= max_failures:
                    logger.error("Maximum consecutive frame read failures reached. Stopping capture.")
                    with self.frame_lock:
                        self.latest_frame = create_placeholder_frame("Camera Feed Lost")
                    break
            
            time.sleep(0.03)  # limit capture to ~30 FPS

        self._cleanup()

    def stop_stream(self):
        """
        Stops worker thread and safely releases all OpenCV video resources.
        """
        with self.state_lock:
            if not self.is_running:
                return
            
            logger.info("Requesting camera stream shutdown...")
            self.stop_event.set()
            if self.thread is not None:
                self.thread.join(timeout=3.0)
                self.thread = None

            self._cleanup()
            logger.info("Camera stream release complete.")

    def _cleanup(self):
        """
        Internal cleanup method to reset stream status variables and release capture handlers.
        """
        with self.frame_lock:
            self.latest_frame = b""
        
        if self.cap is not None:
            self.cap.release()
            self.cap = None
        
        self.source = None
        self.is_running = False

    def get_latest_frame(self) -> bytes:
        """
        Returns the latest JPEG frame. Returns placeholder if offline.
        """
        with self.frame_lock:
            if not self.is_running or not self.latest_frame:
                return create_placeholder_frame("Camera Offline")
            return self.latest_frame

    def get_status(self) -> dict:
        """
        Returns current camera status and source index/link.
        """
        with self.state_lock:
            return {
                "running": self.is_running,
                "source": self.source
            }

camera_manager = CameraManager()

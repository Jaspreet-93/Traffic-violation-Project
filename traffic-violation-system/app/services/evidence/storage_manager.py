import os
import cv2
import numpy as np
from app.utils.file_utils import ensure_dir, generate_evidence_filename
from app.core.logger import logger

class StorageManager:
    def __init__(self):
        self.root_dir = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..", "..", ".."
        ))
        self.images_dir = os.path.join(self.root_dir, "outputs", "violations", "images")
        self.videos_dir = os.path.join(self.root_dir, "outputs", "violations", "videos")
        
        # Verify folders exist
        os.makedirs(self.images_dir, exist_ok=True)
        os.makedirs(self.videos_dir, exist_ok=True)

    def save_image(self, frame: np.ndarray, vehicle_id: int, violation_type: str) -> str:
        """
        Saves frame to outputs/violations/images/ and returns the relative path.
        """
        filename = generate_evidence_filename(vehicle_id, violation_type, "jpg")
        dest_path = os.path.join(self.images_dir, filename)
        ensure_dir(dest_path)
        
        success = cv2.imwrite(dest_path, frame)
        if not success:
            raise IOError(f"Failed to write image evidence file: {dest_path}")
            
        # Return relative path for database registry
        rel_path = os.path.relpath(dest_path, self.root_dir).replace(os.sep, '/')
        logger.info(f"Saved image evidence: {rel_path}")
        return rel_path

    def get_video_writer(self, vehicle_id: int, violation_type: str, fps: int = 20, size: tuple = (640, 480)) -> tuple:
        """
        Initializes cv2.VideoWriter and returns (writer, relative_path).
        """
        filename = generate_evidence_filename(vehicle_id, violation_type, "mp4")
        dest_path = os.path.join(self.videos_dir, filename)
        ensure_dir(dest_path)
        
        fourcc = cv2.VideoWriter_fourcc(*'avc1') # H.264 browser-playable codec
        writer = cv2.VideoWriter(dest_path, fourcc, fps, size)
        rel_path = os.path.relpath(dest_path, self.root_dir).replace(os.sep, '/')
        return writer, rel_path

storage_manager = StorageManager()

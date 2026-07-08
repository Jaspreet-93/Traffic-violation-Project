import os
from app.core.logger import logger

EVIDENCE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "evidence"))
SUBDIRS = ["images", "videos", "processed", "thumbnails", "metadata"]

class StorageService:
    @staticmethod
    def initialize_dirs():
        """
        Creates all structured evidence directories.
        """
        os.makedirs(EVIDENCE_ROOT, exist_ok=True)
        for subdir in SUBDIRS:
            path = os.path.join(EVIDENCE_ROOT, subdir)
            os.makedirs(path, exist_ok=True)
        logger.info(f"Initialized Evidence Locker storage tree at: {EVIDENCE_ROOT}")

# Auto-initialize on load
StorageService.initialize_dirs()

import os
from fastapi import HTTPException, status

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv"}

MAX_IMAGE_SIZE_BYTES = 15 * 1024 * 1024  # 15 MB
MAX_VIDEO_SIZE_BYTES = 100 * 1024 * 1024  # 100 MB

class FileValidator:
    @staticmethod
    def validate_image_file(filename: str, size_bytes: int):
        ext = os.path.splitext(filename)[1].lower()
        if ext not in ALLOWED_IMAGE_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported image extension '{ext}'. Allowed: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}"
            )
        if size_bytes > MAX_IMAGE_SIZE_BYTES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Image file size too large ({size_bytes / (1024*1024):.1f} MB). Max allowed is 15 MB."
            )

    @staticmethod
    def validate_video_file(filename: str, size_bytes: int):
        ext = os.path.splitext(filename)[1].lower()
        if ext not in ALLOWED_VIDEO_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported video extension '{ext}'. Allowed: {', '.join(ALLOWED_VIDEO_EXTENSIONS)}"
            )
        if size_bytes > MAX_VIDEO_SIZE_BYTES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Video file size too large ({size_bytes / (1024*1024):.1f} MB). Max allowed is 100 MB."
            )

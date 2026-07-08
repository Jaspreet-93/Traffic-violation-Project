import os

class PreviewService:
    @staticmethod
    def get_preview_url(evidence_id: int, image_path: str) -> str:
        """
        Builds relative preview path.
        """
        if not image_path:
            return f"/uploads/preview_placeholder.jpg"
        return f"/uploads/{os.path.basename(image_path)}"

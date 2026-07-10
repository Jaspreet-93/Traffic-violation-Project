import os

class DownloadService:
    @staticmethod
    def get_download_path(image_path: str) -> str:
        """
        Retrieves the exact absolute path to download.
        """
        if not image_path:
            return ""
        clean_path = image_path.lstrip('/')
        if clean_path.startswith("uploads"):
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "uploads"))
            filename = clean_path.replace("uploads", "").lstrip('/')
            return os.path.join(base_dir, filename)
        elif clean_path.startswith("outputs"):
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "outputs"))
            filename = clean_path.replace("outputs", "").lstrip('/')
            return os.path.join(base_dir, filename)
            
        return os.path.abspath(image_path)

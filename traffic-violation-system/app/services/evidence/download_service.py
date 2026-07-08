import os

class DownloadService:
    @staticmethod
    def get_download_path(image_path: str) -> str:
        """
        Retrieves the exact absolute path to download.
        """
        if not image_path:
            return ""
        return os.path.abspath(image_path)

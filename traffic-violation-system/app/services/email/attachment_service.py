import os
from email.mime.base import MIMEBase
from email import encoders
from app.core.logger import logger

class AttachmentService:
    @staticmethod
    def create_attachment(relative_path: str) -> MIMEBase:
        """
        Locates a file locally and wraps it in a MIMEBase attachment package.
        """
        if not relative_path:
            return None

        # Convert relative output paths to absolute paths
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        abs_path = os.path.abspath(os.path.join(base_dir, relative_path.lstrip("/")))

        if not os.path.exists(abs_path):
            logger.warning(f"Attachment file not found at: {abs_path}")
            return None

        filename = os.path.basename(abs_path)
        try:
            with open(abs_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {filename}",
                )
                logger.info(f"Created attachment for file: {filename}")
                return part
        except Exception as e:
            logger.error(f"Error creating email attachment for {abs_path}: {e}")
            return None

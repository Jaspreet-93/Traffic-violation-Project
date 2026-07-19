import smtplib
import os
import json
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from app.core.logger import logger

load_dotenv()


SETTINGS_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "email_settings.json"))

def load_email_settings() -> dict:
    """
    Loads email settings from the local JSON config file, falling back to environment variables.
    """
    defaults = {
        "station_name": os.getenv("STATION_NAME", "Central Police Station"),
        "station_email": os.getenv("STATION_EMAIL", ""),
        "smtp_email": os.getenv("SMTP_USERNAME", ""),
        "smtp_password": os.getenv("SMTP_PASSWORD", ""),
        "enabled": os.getenv("EMAIL_NOTIFICATIONS_ENABLED", "true").lower() == "true"
    }
    
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
                # Ensure all required keys exist
                for k, v in defaults.items():
                    if k not in data:
                        data[k] = v
                return data
        except Exception as e:
            logger.error(f"Error reading settings file: {e}")
            
    return defaults

def save_email_settings(settings: dict):
    """
    Saves updated settings to the local JSON configuration file.
    """
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)
        logger.info("Email settings updated successfully.")
    except Exception as e:
        logger.error(f"Error saving settings file: {e}")
        raise e

class SMTPService:
    @staticmethod
    def check_connection() -> bool:
        """
        Validates SMTP server connection status with active credentials.
        """
        settings = load_email_settings()
        host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        port = int(os.getenv("SMTP_PORT", "587"))
        username = settings.get("smtp_email")
        password = settings.get("smtp_password")

        if not username or not password:
            logger.warning("SMTP credentials not configured.")
            return False

        try:
            server = smtplib.SMTP(host, port, timeout=5)
            server.starttls()
            server.login(username, password)
            server.quit()
            return True
        except Exception as e:
            logger.error(f"SMTP connection test failed: {e}")
            return False

    @staticmethod
    def send_email(to_email: str, message: MIMEMultipart) -> bool:
        """
        Sends an email message via SMTP.
        """
        settings = load_email_settings()
        if not settings.get("enabled"):
            logger.info("Email notifications are disabled. Skipping send.")
            return False

        host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        port = int(os.getenv("SMTP_PORT", "587"))
        username = settings.get("smtp_email")
        password = settings.get("smtp_password")

        if not username or not password:
            logger.error("SMTP username/password is missing.")
            raise ValueError("SMTP credentials missing.")

        server = smtplib.SMTP(host, port)
        server.starttls()
        server.login(username, password)
        recipients_list = [email.strip() for email in to_email.split(",") if email.strip()]
        server.sendmail(username, recipients_list, message.as_string())
        server.quit()
        return True

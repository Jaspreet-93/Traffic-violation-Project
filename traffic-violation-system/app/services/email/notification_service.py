import threading
from app.database.connection import SessionLocal
from app.services.email.email_service import EmailService
from app.core.logger import logger

class NotificationService:
    @staticmethod
    def trigger_violation_notification(violation_id: int):
        """
        Asynchronously triggers the email sending workflow in a background thread.
        """
        thread = threading.Thread(
            target=NotificationService._send_notification_worker,
            args=(violation_id,),
            daemon=True
        )
        thread.start()
        logger.info(f"Background email notification task dispatched for violation {violation_id}.")

    @staticmethod
    def _send_notification_worker(violation_id: int):
        """
        Background worker thread processing database queries andSMTP delivery.
        """
        db = SessionLocal()
        try:
            EmailService.send_violation_email(violation_id, db)
            logger.info(f"Notification alert email processed for violation {violation_id}.")
        except Exception as e:
            logger.error(f"Error in background notification task for violation {violation_id}: {e}")
        finally:
            db.close()

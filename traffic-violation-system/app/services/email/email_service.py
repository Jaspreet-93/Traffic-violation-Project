from sqlalchemy.orm import Session
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

from app.database.models.email_log import EmailLog
from app.database.models.violation import Violation
from app.services.email.smtp_service import SMTPService, load_email_settings
from app.services.email.email_templates import EmailTemplates
from app.services.email.attachment_service import AttachmentService
from app.core.logger import logger

class EmailService:
    @staticmethod
    def send_test_email(recipient_email: str) -> dict:
        """
        Compiles and sends a test SMTP connectivity verification email.
        """
        settings = load_email_settings()
        subject = f"[TEST] SMTP Connection Check - {settings.get('station_name')}"
        
        context = {
            "station_name": settings.get("station_name"),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        body_html = EmailTemplates.render_template("test_email.html", context)
        
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = settings.get("smtp_email")
        msg["To"] = recipient_email
        msg.attach(MIMEText(body_html, "html"))
        
        try:
            success = SMTPService.send_email(recipient_email, msg)
            if success:
                return {"status": "success", "message": f"Test email sent successfully to {recipient_email}"}
            else:
                return {"status": "failed", "message": "Notifications disabled in settings."}
        except Exception as e:
            logger.error(f"Test email failed: {e}")
            return {"status": "failed", "message": str(e)}

    @staticmethod
    def send_violation_email(violation_id: int, db: Session) -> EmailLog:
        """
        Generates and sends an HTML report with proof attachments for a violation.
        """
        # Create initial pending log
        settings = load_email_settings()
        from app.services.officer_email.officer_email_service import OfficerEmailService
        recipients = OfficerEmailService.get_active_recipients()
        if not recipients:
            recipients = [settings.get("station_email")]
        recipient = ", ".join(recipients)
        
        if not recipient:
            logger.error("Destination recipient is not configured.")
            raise ValueError("Destination recipient email missing.")
            
        violation = db.query(Violation).filter(Violation.id == violation_id).first()
        if not violation:
            logger.error(f"Violation ID {violation_id} not found in database.")
            raise ValueError(f"Violation ID {violation_id} not found.")

        subject = f"[ALERT] Traffic Violation Detected: {violation.violation_type} - ID: #{violation.vehicle_id}"
        
        from app.database.models.evidence import Evidence
        evidence_rec = db.query(Evidence).filter(Evidence.violation_id == violation_id).first()

        context = {
            "vehicle_id": violation.vehicle_id,
            "vehicle_type": violation.vehicle_type or "Vehicle",
            "plate_number": violation.plate_number or violation.vehicle_number or "UNKNOWN",
            "violation_type": violation.violation_type or "Infraction",
            "seat_belt_status": violation.seat_belt_status or (evidence_rec.seat_belt_status if evidence_rec else "N/A"),
            "camera_id": violation.camera_id or 1,
            "executed_models": violation.executed_models or "YOLOv8-Vehicle, ByteTrack-Tracker, SeatBelt-Classifier",
            "decision_result": violation.decision_result or "Confirmed",
            "confidence": f"{(violation.confidence * 100):.0f}%" if violation.confidence else "95%",
            "timestamp": violation.timestamp.strftime("%Y-%m-%d %H:%M:%S") if violation.timestamp else datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "station_name": settings.get("station_name", "Central Police Station")
        }
        
        body_html = EmailTemplates.render_template("violation_alert.html", context)
        
        msg = MIMEMultipart("related")
        msg["Subject"] = subject
        msg["From"] = settings.get("smtp_email")
        msg["To"] = recipient
        msg.attach(MIMEText(body_html, "html"))
        
        # Attach snapshot image
        snapshot_file = violation.snapshot_path or (evidence_rec.annotated_image_path if evidence_rec else None) or (evidence_rec.image_path if evidence_rec else None)
        abs_snapshot = None
        if snapshot_file:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
            abs_snapshot = os.path.abspath(os.path.join(base_dir, snapshot_file.lstrip("/")))
            
        if abs_snapshot and os.path.exists(abs_snapshot):
            img_part = AttachmentService.create_attachment(snapshot_file)
            if img_part:
                img_part.add_header('Content-ID', '<evidence_image>')
                try:
                    img_part.replace_header('Content-Disposition', f'inline; filename="{os.path.basename(snapshot_file)}"')
                except KeyError:
                    img_part.add_header('Content-Disposition', f'inline; filename="{os.path.basename(snapshot_file)}"')
                msg.attach(img_part)
                
        # Attach video proof clip if distinct
        video_file = (evidence_rec.annotated_video_path if evidence_rec else None) or (evidence_rec.video_path if evidence_rec else None)
        abs_video = None
        if video_file:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
            abs_video = os.path.abspath(os.path.join(base_dir, video_file.lstrip("/")))
            
        if abs_video and os.path.exists(abs_video) and video_file != snapshot_file:
            vid_part = AttachmentService.create_attachment(video_file)
            if vid_part:
                msg.attach(vid_part)
                
        # Insert log
        db_log = EmailLog(
            violation_id=violation_id,
            recipient_email=recipient,
            subject=subject,
            body=body_html,
            status="PENDING",
            sent_at=None,
            error_message=None
        )
        db.add(db_log)
        db.commit()
        db.refresh(db_log)
        
        try:
            success = SMTPService.send_email(recipient, msg)
            if success:
                db_log.status = "SENT"
                db_log.sent_at = datetime.now(timezone.utc)
            else:
                db_log.status = "FAILED"
                db_log.error_message = "Email alerts disabled in settings."
        except Exception as e:
            logger.error(f"Failed to deliver violation email {violation_id}: {e}")
            db_log.status = "FAILED"
            db_log.error_message = str(e)
            
        db.commit()
        db.refresh(db_log)
        return db_log

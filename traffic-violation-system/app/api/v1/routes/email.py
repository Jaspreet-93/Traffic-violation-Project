from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.connection import get_db
from app.database.models.email_log import EmailLog
from app.schemas.email import (
    EmailSettingsUpdate,
    EmailSettingsResponse,
    SendTestEmailRequest,
    EmailLogResponse
)
from app.services.email.smtp_service import SMTPService, load_email_settings, save_email_settings
from app.services.email.email_service import EmailService

router = APIRouter(prefix="/email", tags=["Email Alerts"])

@router.post("/send-test", status_code=status.HTTP_200_OK)
def send_test_email(payload: SendTestEmailRequest):
    """
    Sends a test email to verify SMTP configuration credentials.
    """
    result = EmailService.send_test_email(payload.recipient_email)
    if result["status"] == "failed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["message"]
        )
    return result

@router.post("/send-violation/{violation_id}", response_model=EmailLogResponse, status_code=status.HTTP_200_OK)
def send_violation_email(violation_id: int, db: Session = Depends(get_db)):
    """
    Manually triggers sending an infraction report email to the station address.
    """
    try:
        db_log = EmailService.send_violation_email(violation_id=violation_id, db=db)
        return db_log
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/status")
def get_email_status():
    """
    Checks the active SMTP configuration connection status.
    """
    settings = load_email_settings()
    connected = SMTPService.check_connection()
    return {
        "connected": connected,
        "enabled": settings.get("enabled", True),
        "station_name": settings.get("station_name"),
        "station_email": settings.get("station_email")
    }

@router.get("/logs", response_model=List[EmailLogResponse])
def get_email_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieves all past email dispatch log entries.
    """
    try:
        return db.query(EmailLog).order_by(EmailLog.id.desc()).offset(skip).limit(limit).all()
    except Exception as e:
        from app.core.logger import logger
        logger.error(f"Error querying email logs: {e}")
        return []

@router.get("/settings", response_model=EmailSettingsResponse)
def get_email_settings():
    """
    Retrieves current local email configurations.
    """
    return load_email_settings()

@router.put("/settings", response_model=EmailSettingsResponse)
def update_email_settings(payload: EmailSettingsUpdate):
    """
    Saves and updates local email configurations.
    """
    save_email_settings(payload.model_dump())
    return payload

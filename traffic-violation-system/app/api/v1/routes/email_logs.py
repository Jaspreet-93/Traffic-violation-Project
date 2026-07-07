from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.email_log import EmailLogResponse
from app.services.email_log_service import EmailLogService
from typing import List

router = APIRouter(prefix="/email-logs", tags=["Email Logs"])

@router.get("", response_model=List[EmailLogResponse])
def list_email_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieves a list of all logged email notifications.
    """
    return EmailLogService.get_email_logs(db=db, skip=skip, limit=limit)

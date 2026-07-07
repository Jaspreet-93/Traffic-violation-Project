from sqlalchemy.orm import Session
from app.database.models.email_log import EmailLog
from typing import List

class EmailLogService:
    @staticmethod
    def get_email_logs(db: Session, skip: int = 0, limit: int = 100) -> List[EmailLog]:
        """
        Retrieves a list of email logs from the database.
        """
        return db.query(EmailLog).offset(skip).limit(limit).all()

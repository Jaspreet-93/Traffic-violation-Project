from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.connection import Base

class EmailLog(Base):
    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True, index=True)
    violation_id = Column(Integer, ForeignKey("violations.id", ondelete="CASCADE"), nullable=False)
    recipient_email = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    status = Column(String, default="PENDING")
    sent_at = Column(DateTime, nullable=True)
    error_message = Column(String, nullable=True)

    # Many-to-one relationship with Violation
    violation = relationship("Violation", back_populates="email_logs")

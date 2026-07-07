from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.connection import Base

class Violation(Base):
    __tablename__ = "violations"

    id = Column(Integer, primary_key=True, index=True)
    camera_id = Column(Integer, ForeignKey("cameras.id", ondelete="CASCADE"), nullable=False)
    vehicle_id = Column(Integer, nullable=True)
    plate_number = Column(String, nullable=True)
    vehicle_number = Column(String, nullable=True)
    vehicle_type = Column(String, nullable=False)
    violation_type = Column(String, nullable=False)
    confidence = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    evidence_path = Column(String, nullable=True)
    snapshot_path = Column(String, nullable=True)
    is_processed = Column(Boolean, default=False)

    # Many-to-one relationship with Camera
    camera = relationship("Camera", back_populates="violations")
    
    # One-to-many relationship with EmailLog
    email_logs = relationship("EmailLog", back_populates="violation", cascade="all, delete-orphan")

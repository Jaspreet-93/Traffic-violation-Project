from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.connection import Base

class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(Integer, primary_key=True, index=True)
    violation_id = Column(Integer, ForeignKey("violations.id", ondelete="CASCADE"), nullable=False)
    vehicle_id = Column(Integer, nullable=True)
    plate_number = Column(String, nullable=True)
    violation_type = Column(String, nullable=False)
    image_path = Column(String, nullable=True)
    video_path = Column(String, nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Many-to-one relationship with Violation record
    violation = relationship("Violation")

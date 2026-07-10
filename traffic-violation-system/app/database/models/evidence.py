from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
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
    
    # Original / Annotated media paths
    original_image_path = Column(String, nullable=True)
    annotated_image_path = Column(String, nullable=True)
    original_video_path = Column(String, nullable=True)
    annotated_video_path = Column(String, nullable=True)
    
    # Additional required fields
    confidence = Column(Float, nullable=True)
    camera_id = Column(String, nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Keep compatibility aliases
    image_path = Column(String, nullable=True)
    video_path = Column(String, nullable=True)

    # Many-to-one relationship with Violation record
    violation = relationship("Violation")

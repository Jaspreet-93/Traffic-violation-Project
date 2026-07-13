from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database.connection import Base

class Violation(Base):
    __tablename__ = "violations"

    id = Column(Integer, primary_key=True, index=True)
    camera_id = Column(Integer, ForeignKey("cameras.id", ondelete="CASCADE"), nullable=False, index=True)
    vehicle_id = Column(Integer, nullable=True, index=True)
    plate_number = Column(String, nullable=True, index=True)
    vehicle_number = Column(String, nullable=True)
    vehicle_type = Column(String, nullable=False)
    violation_type = Column(String, nullable=False)
    confidence = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    evidence_path = Column(String, nullable=True)
    snapshot_path = Column(String, nullable=True)
    is_processed = Column(Boolean, default=False)
    executed_models = Column(String, nullable=True)
    skipped_models = Column(String, nullable=True)
    reason_for_skip = Column(String, nullable=True)
    decision_result = Column(String, nullable=True)
    overall_confidence = Column(Float, nullable=True)
    seat_belt_status = Column(String, nullable=True)
    visibility_score = Column(Float, nullable=True)
    driver_visibility_conf = Column(Float, nullable=True)
    seat_belt_visibility_conf = Column(Float, nullable=True)
    seat_belt_detection_conf = Column(Float, nullable=True)
    vehicle_detection_conf = Column(Float, nullable=True)
    overall_decision_conf = Column(Float, nullable=True)
    
    # New columns for dynamic crops
    original_image = Column(String, nullable=True)
    annotated_image = Column(String, nullable=True)
    vehicle_crop = Column(String, nullable=True)
    helmet_crop = Column(String, nullable=True)
    seatbelt_crop = Column(String, nullable=True)
    plate_crop = Column(String, nullable=True)
    trafficlight_crop = Column(String, nullable=True)
    mobile_crop = Column(String, nullable=True)
    lane_crop = Column(String, nullable=True)

    # Many-to-one relationship with Camera
    camera = relationship("Camera", back_populates="violations")
    
    # One-to-many relationship with EmailLog
    email_logs = relationship("EmailLog", back_populates="violation", cascade="all, delete-orphan")

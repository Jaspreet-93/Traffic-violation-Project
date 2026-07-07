import os
import time
import numpy as np
from app.services.evidence.evidence_capture import evidence_capture
from app.services.evidence.evidence_service import evidence_service
from app.services.violation.violation_service import violation_service
from app.database.connection import SessionLocal
from app.database.models.violation import Violation
from app.database.models.evidence import Evidence

def test_evidence_capture_and_save():
    # 1. Create a dummy frame
    dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # 2. Feed frames into rolling buffer to simulate video stream
    print("Feeding dummy frames to buffer...")
    for _ in range(40):
        evidence_capture.add_frame_to_buffer(dummy_frame)
        
    # 3. Insert a mock violation record in database to link evidence to
    db = SessionLocal()
    try:
        mock_violation = Violation(
            camera_id=1,
            vehicle_id=99,
            plate_number="PB10AB1234",
            vehicle_number="PB10AB1234",
            vehicle_type="car",
            violation_type="No Seatbelt",
            confidence=0.92,
            evidence_path="",
            snapshot_path=""
        )
        db.add(mock_violation)
        db.commit()
        db.refresh(mock_violation)
        violation_id = mock_violation.id
    except Exception as e:
        db.rollback()
        print(f"Database insertion failed (normal if Postgres is offline): {e}")
        violation_id = 999
    finally:
        db.close()

    # 4. Trigger evidence capturing
    print(f"Triggering evidence capture...")
    img_path = evidence_capture.capture_image_evidence(dummy_frame, 99, "No Seatbelt")
    vid_path = evidence_capture.capture_video_evidence(99, "No Seatbelt")
    
    # Give background thread a moment to compile video
    time.sleep(1.5)
    
    # 5. Assertions
    assert img_path != "", "Image capture path is empty"
    assert vid_path != "", "Video capture path is empty"
    
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    full_img_path = os.path.join(root_dir, img_path)
    full_vid_path = os.path.join(root_dir, vid_path)
    
    assert os.path.exists(full_img_path), f"Captured snapshot image not found: {full_img_path}"
    assert os.path.exists(full_vid_path), f"Compiled video clip not found: {full_vid_path}"
    
    print("\n--- Evidence Capture Test Passed ---")
    print(f"Image proof saved: {img_path}")
    print(f"Video proof saved: {vid_path}\n")

if __name__ == "__main__":
    test_evidence_capture_and_save()

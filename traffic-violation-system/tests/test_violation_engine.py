
from app.services.tracking.bytetrack_tracker import bytetrack_tracker
from app.services.helmet.helmet_service import helmet_service
from app.services.seat_belt.seat_belt_service import seat_belt_service
from app.services.driver_behavior.behavior_service import behavior_service
from app.services.traffic_light.traffic_light_service import traffic_light_service
from app.services.ocr.ocr_service import ocr_service
from app.services.violation.violation_engine import violation_decision_engine
from app.services.violation.violation_service import violation_service
from app.database.connection import SessionLocal
from app.database.models.violation import Violation

def test_violation_decision_engine():
    # 1. Mock active states
    bytetrack_tracker.latest_tracks = [
        {"id": 10, "class_id": 3, "box": [100, 100, 200, 200], "conf": 0.88}, # Motorcycle
        {"id": 12, "class_id": 2, "box": [300, 300, 450, 450], "conf": 0.91}  # Car
    ]
    
    helmet_service.is_running = True
    helmet_service.latest_helmet_results = {
        10: {"status": "no helmet", "confidence": 0.85}
    }
    
    seat_belt_service.is_running = True
    seat_belt_service.latest_seat_belt_results = {
        12: {"status": "no seatbelt", "confidence": 0.89}
    }
    
    behavior_service.is_running = True
    behavior_service.latest_behavior_results = {
        12: {"status": "phone", "confidence": 0.92}
    }
    
    traffic_light_service.is_running = True
    traffic_light_service.latest_traffic_light_state = "red"
    
    ocr_service.latest_ocr_results = {
        10: {"plate_number": "MH12DE5678", "confidence": 0.94},
        12: {"plate_number": "PB10AB1234", "confidence": 0.96}
    }
    
    # 2. Evaluate violations
    violations = violation_decision_engine.evaluate_frame_violations(camera_id=1)
    
    assert len(violations) > 0, "Should generate violations"
    
    # Verify specific types generated
    violation_types = [v["violation_type"] for v in violations]
    assert "No Helmet" in violation_types
    assert "No Seatbelt" in violation_types
    assert "Phone Usage" in violation_types
    assert "Red Light Violation" in violation_types
    
    # Verify mapping properties
    no_helmet_violation = next(v for v in violations if v["violation_type"] == "No Helmet")
    assert no_helmet_violation["plate_number"] == "MH12DE5678"
    assert no_helmet_violation["vehicle_id"] == 10
    
    # 3. Test Violation Service persistence
    violation_service.clear_session()
    # Mock Camera ID in DB if needed; for tests we assert process loop runs cleanly
    violation_service.process_frame_violations(camera_id=1)
    
    assert len(violation_service.recorded_violations) > 0
    print("Violation engine unit test passed successfully!")

if __name__ == "__main__":
    test_violation_decision_engine()

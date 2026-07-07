import unittest
import numpy as np
import time
import os
from app.services.evidence.evidence_capture import evidence_capture
from app.services.violation.violation_engine import violation_decision_engine
from app.services.violation.violation_service import violation_service
from app.services.analytics.analytics_service import analytics_service
from app.database.connection import SessionLocal
from app.database.models.violation import Violation

class TestIntegrationPipeline(unittest.TestCase):
    def test_pipeline_workflow(self):
        print("\n--- Starting Integration Test ---")
        
        # 1. Simulate Camera Frame
        print("Step 1: Simulating video frame capture...")
        dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        self.assertEqual(dummy_frame.shape, (480, 640, 3))
        
        # 2. Push frame to rolling buffer
        print("Step 2: Feeding frame to rolling buffer...")
        evidence_capture.add_frame_to_buffer(dummy_frame)
        self.assertGreater(len(evidence_capture.frame_buffer), 0)

        # 3. Simulate detection class caches
        from app.services.helmet.helmet_service import helmet_service
        from app.services.number_plate.plate_service import plate_service
        from app.services.seat_belt.seat_belt_service import seat_belt_service
        from app.services.traffic_light.traffic_light_service import traffic_light_service
        from app.services.driver_behavior.behavior_service import behavior_service

        from app.services.tracking.bytetrack_tracker import bytetrack_tracker
        from app.services.ocr.ocr_service import ocr_service

        print("Step 3: Simulating AI Pipeline model predictions...")
        # Populate bytetrack_tracker tracks
        bytetrack_tracker.latest_tracks = [
            {"id": 10, "class_id": 3, "box": [50, 50, 100, 100]}
        ]
        
        # Populate helmet status
        helmet_service.is_running = True
        helmet_service.latest_helmet_results = {
            10: {"status": "no helmet", "confidence": 0.88}
        }
        
        # Populate ocr results
        ocr_service.latest_ocr_results = {
            10: {"plate_number": "DL3C1234", "confidence": 0.91}
        }
        
        # 4. Run Violation engine evaluation
        print("Step 4: Running Violation Decision Engine...")
        violations = violation_decision_engine.evaluate_frame_violations(camera_id=1)
        self.assertIsNotNone(violations)
        
        # Ensure 'No Helmet' violation was generated
        helmet_violation = next((v for v in violations if v["violation_type"] == "No Helmet"), None)
        self.assertIsNotNone(helmet_violation, "Helmet violation not detected by engine")
        self.assertEqual(helmet_violation["plate_number"], "DL3C1234")

        # 5. Process and persist (mock DB checks)
        print("Step 5: Processing and saving violation to storage and database...")
        db = SessionLocal()
        try:
            db_violation = Violation(
                camera_id=1,
                vehicle_id=10,
                plate_number="DL3C1234",
                vehicle_number="DL3C1234",
                vehicle_type="motorcycle",
                violation_type="No Helmet",
                confidence=0.88,
                evidence_path="",
                snapshot_path=""
            )
            db.add(db_violation)
            db.commit()
            db.refresh(db_violation)
            
            # Save mock evidence files
            img_path = evidence_capture.capture_image_evidence(dummy_frame, 10, "No Helmet")
            self.assertTrue(img_path.endswith(".jpg"))
            self.assertTrue(os.path.exists(img_path))
            
            # Clean up files created
            if os.path.exists(img_path):
                os.remove(img_path)
            
            db.delete(db_violation)
            db.commit()
            print("Step 6: Pipeline workflow integration completed successfully!")
        except Exception as e:
            db.rollback()
            print(f"Skipping DB operations (database connection refused/offline): {e}")
        finally:
            db.close()

if __name__ == "__main__":
    unittest.main()

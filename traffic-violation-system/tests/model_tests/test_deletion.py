import unittest
import os
from app.services.camera_management.camera_service import camera_service
from app.services.reports.report_service import report_service
from app.services.violation.violation_service import violation_service, load_deleted_violations, save_deleted_violations

class TestPersistentDeletion(unittest.TestCase):
    def test_camera_deletion_persistence(self):
        cams = camera_service.list_cameras()
        initial_len = len(cams)
        
        # Create
        cam = camera_service.create_camera({"name": "Test Camera", "url": "rtsp://1.1.1.1/live"})
        self.assertEqual(len(camera_service.list_cameras()), initial_len + 1)
        
        # Delete
        camera_service.delete_camera(cam["id"])
        self.assertEqual(len(camera_service.list_cameras()), initial_len)

    def test_report_deletion_persistence(self):
        reports = report_service.list_reports()
        initial_len = len(reports)
        
        # Create
        rep = report_service.generate_report("daily", "csv")
        self.assertEqual(len(report_service.list_reports()), initial_len + 1)
        
        # Delete
        report_service.delete_report(rep["id"])
        self.assertEqual(len(report_service.list_reports()), initial_len)

    def test_violation_deletion_persistence(self):
        # Reset deleted file for clean test run
        save_deleted_violations(set())
        
        # Delete default violation id=1
        violation_service.delete_violation(1)
        
        deleted_set = load_deleted_violations()
        self.assertIn(1, deleted_set)
        
        # Clean up
        save_deleted_violations(set())

if __name__ == "__main__":
    unittest.main()

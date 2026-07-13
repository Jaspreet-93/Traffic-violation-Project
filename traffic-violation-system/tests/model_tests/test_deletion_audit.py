import unittest
import os
import json
import shutil
from app.services.evidence.evidence_service import evidence_service
from app.services.violation.violation_service import violation_service
from app.services.reports.report_service import report_service
from app.services.camera_management.camera_service import camera_service
from app.services.upload_detection.upload_service import UploadService
from app.utils.deletion_registry import load_deleted_ids, record_deleted_id

class TestDeletionAudit(unittest.TestCase):
    def setUp(self):
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        self.uploads_dir = os.path.join(self.project_root, "uploads")
        self.storage_dir = os.path.join(self.project_root, "storage")
        
        # Back up existing files if any
        self.backup_files = {}
        for name in ["evidence", "violations", "reports", "cameras", "uploads"]:
            path = os.path.join(self.uploads_dir, f"deleted_{name}.json")
            if os.path.exists(path):
                with open(path, "r") as f:
                    self.backup_files[name] = json.load(f)
                os.remove(path)
            else:
                self.backup_files[name] = []

    def tearDown(self):
        # Restore backed up registries
        for name, data in self.backup_files.items():
            path = os.path.join(self.uploads_dir, f"deleted_{name}.json")
            if data:
                with open(path, "w") as f:
                    json.dump(data, f)
            elif os.path.exists(path):
                os.remove(path)

    def test_evidence_file_deletion_and_filtering(self):
        # 1. Create a mock crop file on disk
        job_id = "test-job-uuid-1234"
        veh_id = 9999
        crop_dir = os.path.join(self.storage_dir, "vehicle")
        os.makedirs(crop_dir, exist_ok=True)
        crop_path = os.path.join(crop_dir, f"vehicle_crop_{job_id}_v{veh_id}.jpg")
        with open(crop_path, "w") as f:
            f.write("mock_data")
            
        mock_evidence_item = {
            "evidence_id": 99999,
            "violation_id": 99999,
            "vehicle_id": veh_id,
            "image_path": f"/uploads/processed_snapshot_{job_id}.jpg",
            "annotated_image_path": f"/uploads/processed_snapshot_{job_id}.jpg"
        }
        evidence_service.add_fallback_evidence(mock_evidence_item)
        
        # Verify it lists
        all_ev = evidence_service.get_all_evidence()
        self.assertTrue(any(item["evidence_id"] == 99999 for item in all_ev))
        
        # Verify file exists
        self.assertTrue(os.path.exists(crop_path))
        
        # 2. Trigger delete
        evidence_service.delete_evidence(99999)
        
        # Verify filtered out in get_all_evidence
        all_ev_after = evidence_service.get_all_evidence()
        self.assertFalse(any(item["evidence_id"] == 99999 for item in all_ev_after))
        
        # Verify get_evidence_by_id returns None
        self.assertIsNone(evidence_service.get_evidence_by_id(99999))
        
        # Verify file on disk is removed
        self.assertFalse(os.path.exists(crop_path))
        
        # Clean up if not deleted
        if os.path.exists(crop_path):
            os.remove(crop_path)

    def test_violation_filtering(self):
        violation_service.recorded_violations.append({
            "id": 88888,
            "vehicle_id": 7777,
            "violation_type": "No Helmet"
        })
        
        # Verify lists
        all_v = violation_service.get_all_violations()
        mapped_id = None
        for item in all_v:
            if item.get("vehicle_id") == 7777 and item.get("violation_type") == "No Helmet":
                mapped_id = item["id"]
                break
        
        self.assertIsNotNone(mapped_id)
        
        # Trigger delete
        violation_service.delete_violation(mapped_id)
        
        # Verify filtered out
        all_v_after = violation_service.get_all_violations()
        self.assertFalse(any(item["id"] == mapped_id for item in all_v_after))
        self.assertIsNone(violation_service.get_violation_by_id(mapped_id))

    def test_report_file_deletion_and_filtering(self):
        r_item = report_service.generate_report("daily", "pdf")
        report_id = r_item["id"]
        report_name = r_item["name"]
        
        reports_dir = os.path.join(self.project_root, "reports")
        report_path = os.path.join(reports_dir, f"{report_name}.pdf")
        
        # Verify lists
        all_r = report_service.list_reports()
        self.assertTrue(any(item["id"] == report_id for item in all_r))
        self.assertTrue(os.path.exists(report_path))
        
        # Trigger delete
        report_service.delete_report(report_id)
        
        # Verify filtered
        all_r_after = report_service.list_reports()
        self.assertFalse(any(item["id"] == report_id for item in all_r_after))
        self.assertFalse(os.path.exists(report_path))

if __name__ == "__main__":
    unittest.main()

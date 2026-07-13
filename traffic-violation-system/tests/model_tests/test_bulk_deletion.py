import unittest
from fastapi.testclient import TestClient
from app.main import app
from app.services.evidence.evidence_service import evidence_service, bulk_delete_progress
from app.database.connection import SessionLocal
from app.database.models.evidence import Evidence

class TestBulkDeletion(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        
        # Inject mock fallback items
        evidence_service.add_fallback_evidence({
            "evidence_id": 999901,
            "violation_id": 1001,
            "vehicle_id": 2001,
            "violation": "No Helmet",
            "image_path": "/uploads/snapshot_test_1.jpg"
        })
        evidence_service.add_fallback_evidence({
            "evidence_id": 999902,
            "violation_id": 1002,
            "vehicle_id": 2002,
            "violation": "No Seat Belt",
            "image_path": "/uploads/snapshot_test_2.jpg"
        })

    def test_bulk_delete_api(self):
        # 1. Trigger bulk delete
        response = self.client.request(
            "DELETE",
            "/api/v1/evidence/bulk",
            json={"ids": [999901, 999902]}
        )
        self.assertEqual(response.status_code, 200, response.json())
        data = response.json()
        self.assertTrue(data["success"])
        job_id = data["job_id"]
        self.assertTrue(job_id)

        # 2. Check progress
        progress_res = self.client.get(f"/api/v1/evidence/bulk/progress/{job_id}")
        self.assertEqual(progress_res.status_code, 200)
        prog_data = progress_res.json()
        self.assertIn("total", prog_data)
        self.assertIn("current", prog_data)
        self.assertIn("status", prog_data)

    def test_delete_all_api(self):
        # 1. Trigger delete all
        response = self.client.delete("/api/v1/evidence")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        job_id = data["job_id"]
        self.assertTrue(job_id)

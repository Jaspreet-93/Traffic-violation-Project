import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestEnterpriseStage6Endpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import os
        uploads_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "uploads"))
        for name in ["evidence", "violations", "reports", "cameras", "uploads"]:
            deleted_file = os.path.join(uploads_dir, f"deleted_{name}.json")
            if os.path.exists(deleted_file):
                try:
                    os.remove(deleted_file)
                except Exception:
                    pass
        cls.client = TestClient(app)

    def test_get_all_evidence(self):
        print("Testing GET /api/v1/evidence ...")
        response = self.client.get("/api/v1/evidence")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        if len(data) > 0:
            self.assertIn("evidence_id", data[0])
            self.assertIn("violation", data[0])

    def test_get_evidence_by_id(self):
        print("Testing GET /api/v1/evidence/{id} ...")
        response = self.client.get("/api/v1/evidence/1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["evidence_id"], 1)

    def test_get_metadata(self):
        print("Testing GET /api/v1/evidence/metadata/{id} ...")
        response = self.client.get("/api/v1/evidence/metadata/1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("detection_time", data)
        self.assertIn("resolution", data)

    def test_get_integrity(self):
        print("Testing GET /api/v1/evidence/integrity/{id} ...")
        response = self.client.get("/api/v1/evidence/integrity/1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("checksum_sha256", data)
        self.assertTrue(data["integrity_verified"])

    def test_preview(self):
        print("Testing GET /api/v1/evidence/preview/{id} ...")
        response = self.client.get("/api/v1/evidence/preview/1")
        # Should return file preview placeholder or binary response
        self.assertIn(response.status_code, [200, 404])

    def test_download(self):
        print("Testing GET /api/v1/evidence/download/{id} ...")
        response = self.client.get("/api/v1/evidence/download/1")
        self.assertIn(response.status_code, [200, 404])

    def test_z_delete_evidence(self):
        print("Testing DELETE /api/v1/evidence/{id} ...")
        response = self.client.delete("/api/v1/evidence/1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])

if __name__ == "__main__":
    import unittest
    unittest.main()

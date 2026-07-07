import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestAPIEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_system_status(self):
        print("Testing GET / ...")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_camera_status(self):
        print("Testing GET /api/v1/camera/status ...")
        response = self.client.get("/api/v1/camera/status")
        self.assertEqual(response.status_code, 200)
        self.assertIn("running", response.json())

    def test_tracking_status(self):
        print("Testing GET /api/v1/tracking/status ...")
        response = self.client.get("/api/v1/tracking/status")
        self.assertEqual(response.status_code, 200)

    def test_helmet_status(self):
        print("Testing GET /api/v1/helmet/status ...")
        response = self.client.get("/api/v1/helmet/status")
        self.assertEqual(response.status_code, 200)

    def test_ocr_status(self):
        print("Testing GET /api/v1/ocr/status ...")
        response = self.client.get("/api/v1/ocr/status")
        self.assertEqual(response.status_code, 200)

    def test_violations_endpoints(self):
        print("Testing GET /api/v1/violations ...")
        response = self.client.get("/api/v1/violations")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_evidence_endpoints(self):
        print("Testing GET /api/v1/evidence ...")
        response = self.client.get("/api/v1/evidence")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_analytics_endpoints(self):
        print("Testing GET /api/v1/analytics/summary ...")
        response = self.client.get("/api/v1/analytics/summary")
        self.assertEqual(response.status_code, 200)
        self.assertIn("total_violations", response.json())

if __name__ == "__main__":
    unittest.main()

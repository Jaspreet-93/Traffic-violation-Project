import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestEnterpriseEnhancementEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    # 1. Camera Management Tests
    def test_get_all_cameras(self):
        print("Testing GET /api/v1/cameras ...")
        response = self.client.get("/api/v1/cameras")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_create_camera(self):
        print("Testing POST /api/v1/cameras ...")
        payload = {
            "name": "East Highway Camera",
            "url": "rtsp://192.168.1.103/live",
            "resolution": "1920x1080",
            "fps": 30,
            "recording_enabled": True
        }
        response = self.client.post("/api/v1/cameras", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["name"], "East Highway Camera")

    def test_update_camera(self):
        print("Testing PUT /api/v1/cameras/{id} ...")
        payload = {"name": "East Highway Camera Mod"}
        response = self.client.put("/api/v1/cameras/1", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "East Highway Camera Mod")

    def test_camera_status(self):
        print("Testing GET /api/v1/cameras/status ...")
        response = self.client.get("/api/v1/cameras/status")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("total_cameras", data)

    def test_camera_health(self):
        print("Testing GET /api/v1/cameras/health/{camera_id} ...")
        response = self.client.get("/api/v1/cameras/health/1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("health_score", data)

    # 2. Statistics Dashboard Tests
    def test_get_statistics_overview(self):
        print("Testing GET /api/v1/statistics ...")
        response = self.client.get("/api/v1/statistics")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("total_vehicles", data)

    def test_get_statistics_daily(self):
        print("Testing GET /api/v1/statistics/daily ...")
        response = self.client.get("/api/v1/statistics/daily")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("daily", data)

    def test_get_statistics_performance(self):
        print("Testing GET /api/v1/statistics/performance ...")
        response = self.client.get("/api/v1/statistics/performance")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("gpu_utilization_pct", data)

    # 3. Reports Center Tests
    def test_get_all_reports(self):
        print("Testing GET /api/v1/reports ...")
        response = self.client.get("/api/v1/reports")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_generate_report(self):
        print("Testing POST /api/v1/reports/generate ...")
        payload = {
            "report_type": "daily",
            "export_format": "pdf"
        }
        response = self.client.post("/api/v1/reports/generate", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])

    # 4. Settings Configuration Tests
    def test_get_settings(self):
        print("Testing GET /api/v1/settings ...")
        response = self.client.get("/api/v1/settings")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("smtp_host", data)

    def test_update_settings(self):
        print("Testing PUT /api/v1/settings ...")
        payload = {"smtp_host": "smtp.mailtrap.io"}
        response = self.client.put("/api/v1/settings", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["smtp_host"], "smtp.mailtrap.io")

if __name__ == "__main__":
    import unittest
    unittest.main()

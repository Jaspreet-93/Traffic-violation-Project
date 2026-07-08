import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestEmailEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_get_email_status(self):
        print("Testing GET /api/v1/email/status ...")
        response = self.client.get("/api/v1/email/status")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("connected", data)
        self.assertIn("enabled", data)

    def test_get_email_settings(self):
        print("Testing GET /api/v1/email/settings ...")
        response = self.client.get("/api/v1/email/settings")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("station_name", data)
        self.assertIn("station_email", data)

    def test_update_email_settings(self):
        print("Testing PUT /api/v1/email/settings ...")
        payload = {
            "station_name": "Test Station",
            "station_email": "test@traffic.gov",
            "smtp_email": "test@gmail.com",
            "smtp_password": "testpassword123",
            "enabled": True
        }
        response = self.client.put("/api/v1/email/settings", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["station_name"], "Test Station")
        self.assertEqual(data["station_email"], "test@traffic.gov")

    def test_get_email_logs(self):
        print("Testing GET /api/v1/email/logs ...")
        response = self.client.get("/api/v1/email/logs")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_send_test_email_validation(self):
        print("Testing POST /api/v1/email/send-test validation...")
        # Should return 400 since credentials in test are mock/invalid
        response = self.client.post("/api/v1/email/send-test", json={"recipient_email": "test@test.com"})
        self.assertIn(response.status_code, [200, 400])

if __name__ == "__main__":
    unittest.main()

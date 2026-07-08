import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestEnterpriseStage3Endpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_live_confidence(self):
        print("Testing GET /api/v1/confidence/live ...")
        response = self.client.get("/api/v1/confidence/live")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("vehicle_detection", data)
        self.assertIn("helmet_detection", data)

    def test_confidence_history(self):
        print("Testing GET /api/v1/confidence/history ...")
        response = self.client.get("/api/v1/confidence/history")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("history", data)
        self.assertIsInstance(data["history"], list)

    def test_models_confidence(self):
        print("Testing GET /api/v1/confidence/models ...")
        response = self.client.get("/api/v1/confidence/models")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("models", data)
        self.assertIsInstance(data["models"], list)

    def test_trust_score(self):
        print("Testing GET /api/v1/confidence/trust-score ...")
        response = self.client.get("/api/v1/confidence/trust-score")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("overall_trust_score", data)
        self.assertIn("trust_level", data)

    def test_statistics(self):
        print("Testing GET /api/v1/confidence/statistics ...")
        response = self.client.get("/api/v1/confidence/statistics")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("confidence_trend", data)
        self.assertIn("model_comparison", data)

if __name__ == "__main__":
    import unittest
    unittest.main()

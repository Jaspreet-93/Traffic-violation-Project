import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestEnterpriseStage1Endpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_overview(self):
        print("Testing GET /api/v1/ai/overview ...")
        response = self.client.get("/api/v1/ai/overview")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("system_health", data)
        self.assertIn("total_models", data)
        self.assertIn("running_models", data)
        self.assertIn("loaded_models", data)

    def test_system_health(self):
        print("Testing GET /api/v1/ai/system-health ...")
        response = self.client.get("/api/v1/ai/system-health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("cpu_usage", data)
        self.assertIn("ram_usage", data)
        self.assertIn("disk_usage", data)
        self.assertIn("uptime", data)

    def test_model_health(self):
        print("Testing GET /api/v1/ai/model-health ...")
        response = self.client.get("/api/v1/ai/model-health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("models", data)
        self.assertIsInstance(data["models"], list)
        if data["models"]:
            first_model = data["models"][0]
            self.assertIn("name", first_model)
            self.assertIn("status", first_model)
            self.assertIn("exists", first_model)

    def test_hardware(self):
        print("Testing GET /api/v1/ai/hardware ...")
        response = self.client.get("/api/v1/ai/hardware")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("cpu_cores", data)
        self.assertIn("ram_total_gb", data)

    def test_confidence(self):
        print("Testing GET /api/v1/ai/confidence ...")
        response = self.client.get("/api/v1/ai/confidence")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("vehicle_detection", data)
        self.assertIn("helmet_detection", data)

    def test_performance(self):
        print("Testing GET /api/v1/ai/performance ...")
        response = self.client.get("/api/v1/ai/performance")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("fps", data)
        self.assertIn("inference_time_ms", data)

if __name__ == "__main__":
    import unittest
    unittest.main()

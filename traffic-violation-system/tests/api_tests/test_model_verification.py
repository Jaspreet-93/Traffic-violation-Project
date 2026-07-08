import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestModelVerificationEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_model_overview(self):
        print("Testing GET /api/v1/model/overview ...")
        response = self.client.get("/api/v1/model/overview")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["model_name"], "YOLOv8 Object Detector")
        self.assertIn("framework", data)

    def test_model_health(self):
        print("Testing GET /api/v1/model/health ...")
        response = self.client.get("/api/v1/model/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "Excellent")
        self.assertIn("memory_usage_mb", data)

    def test_model_metrics(self):
        print("Testing GET /api/v1/model/metrics ...")
        response = self.client.get("/api/v1/model/metrics")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("precision", data)
        self.assertIn("f1_score", data)

    def test_model_dataset(self):
        print("Testing GET /api/v1/model/dataset ...")
        response = self.client.get("/api/v1/model/dataset")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("dataset_name", data)
        self.assertIn("training_split", data)

    def test_model_performance(self):
        print("Testing GET /api/v1/model/performance ...")
        response = self.client.get("/api/v1/model/performance")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("precision_trend", data)

    def test_model_benchmark(self):
        print("Testing GET /api/v1/model/benchmark ...")
        response = self.client.get("/api/v1/model/benchmark")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("benchmarks", data)

    def test_model_recommendations(self):
        print("Testing GET /api/v1/model/recommendations ...")
        response = self.client.get("/api/v1/model/recommendations")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("recommendations", data)

    def test_model_verification_checks(self):
        print("Testing GET /api/v1/model/verification ...")
        response = self.client.get("/api/v1/model/verification")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("overall_passed", data)
        self.assertIn("checks", data)

if __name__ == "__main__":
    import unittest
    unittest.main()

import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestAICommandCenterEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_overview(self):
        print("Testing GET /api/v1/ai/overview ...")
        response = self.client.get("/api/v1/ai/overview")
        self.assertEqual(response.status_code, 200)
        self.assertIn("system_health", response.json())
        self.assertIn("total_models", response.json())

    def test_models(self):
        print("Testing GET /api/v1/ai/models ...")
        response = self.client.get("/api/v1/ai/models")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_model_health(self):
        print("Testing GET /api/v1/ai/model-health ...")
        response = self.client.get("/api/v1/ai/model-health")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_datasets(self):
        print("Testing GET /api/v1/ai/datasets ...")
        response = self.client.get("/api/v1/ai/datasets")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_confidence(self):
        print("Testing GET /api/v1/ai/confidence ...")
        response = self.client.get("/api/v1/ai/confidence")
        self.assertEqual(response.status_code, 200)
        self.assertIn("vehicle_detection", response.json())

    def test_performance(self):
        print("Testing GET /api/v1/ai/performance ...")
        response = self.client.get("/api/v1/ai/performance")
        self.assertEqual(response.status_code, 200)
        self.assertIn("fps", response.json())

    def test_benchmark(self):
        print("Testing GET /api/v1/ai/benchmark ...")
        response = self.client.get("/api/v1/ai/benchmark")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_system_health(self):
        print("Testing GET /api/v1/ai/system-health ...")
        response = self.client.get("/api/v1/ai/system-health")
        self.assertEqual(response.status_code, 200)
        self.assertIn("overall_status", response.json())

    def test_diagnostics(self):
        print("Testing GET /api/v1/ai/diagnostics ...")
        response = self.client.get("/api/v1/ai/diagnostics")
        self.assertEqual(response.status_code, 200)
        self.assertIn("issues", response.json())

    def test_recommendations(self):
        print("Testing GET /api/v1/ai/recommendations ...")
        response = self.client.get("/api/v1/ai/recommendations")
        self.assertEqual(response.status_code, 200)
        self.assertIn("recommendations", response.json())

    def test_report(self):
        print("Testing GET /api/v1/ai/report ...")
        response = self.client.get("/api/v1/ai/report")
        self.assertEqual(response.status_code, 200)
        self.assertIn("summary", response.json())

    def test_export_report_pdf(self):
        print("Testing POST /api/v1/ai/report/export (pdf) ...")
        response = self.client.post("/api/v1/ai/report/export", json={"format": "pdf"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("report_file", response.json())

    def test_export_report_csv(self):
        print("Testing POST /api/v1/ai/report/export (csv) ...")
        response = self.client.post("/api/v1/ai/report/export", json={"format": "csv"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("report_file", response.json())

if __name__ == "__main__":
    import unittest
    unittest.main()

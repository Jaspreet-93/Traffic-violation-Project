import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestEnterpriseStage4Endpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_latest_decision(self):
        print("Testing GET /api/v1/decision/latest ...")
        response = self.client.get("/api/v1/decision/latest")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("violation_id", data)
        self.assertIn("violation_type", data)
        self.assertIn("decision", data)

    def test_decision_history(self):
        print("Testing GET /api/v1/decision/history ...")
        response = self.client.get("/api/v1/decision/history")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("history", data)
        self.assertIsInstance(data["history"], list)

    def test_decision_by_id(self):
        print("Testing GET /api/v1/decision/{violation_id} ...")
        response = self.client.get("/api/v1/decision/violation-job-0")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["violation_id"], "violation-job-0")

    def test_explanation(self):
        print("Testing GET /api/v1/decision/explanation/{violation_id} ...")
        response = self.client.get("/api/v1/decision/explanation/violation-job-0")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("reason", data)
        self.assertIn("supporting_detections", data)
        self.assertIn("model_confidence", data)

    def test_audit(self):
        print("Testing GET /api/v1/decision/audit/{violation_id} ...")
        response = self.client.get("/api/v1/decision/audit/violation-job-0")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("decision_time", data)
        self.assertIn("models_used", data)
        self.assertIn("processing_time_ms", data)

if __name__ == "__main__":
    import unittest
    unittest.main()

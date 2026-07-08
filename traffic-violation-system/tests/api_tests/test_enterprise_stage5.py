import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestEnterpriseStage5Endpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_list_replays(self):
        print("Testing GET /api/v1/replay/list ...")
        response = self.client.get("/api/v1/replay/list")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("replays", data)
        self.assertIsInstance(data["replays"], list)

    def test_replay_details(self):
        print("Testing GET /api/v1/replay/{violation_id} ...")
        response = self.client.get("/api/v1/replay/violation-mock-1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["violation_id"], "violation-mock-1")
        self.assertIn("original_video_url", data)

    def test_replay_timeline(self):
        print("Testing GET /api/v1/replay/timeline/{violation_id} ...")
        response = self.client.get("/api/v1/replay/timeline/violation-mock-1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["violation_id"], "violation-mock-1")
        self.assertIn("events", data)

    def test_replay_frame(self):
        print("Testing GET /api/v1/replay/frame/{violation_id}/{frame_number} ...")
        response = self.client.get("/api/v1/replay/frame/violation-mock-1/45")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["frame_number"], 45)
        self.assertIn("image_url", data)

if __name__ == "__main__":
    import unittest
    unittest.main()

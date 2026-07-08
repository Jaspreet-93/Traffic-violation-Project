import unittest
import cv2
import numpy as np
from fastapi.testclient import TestClient
from app.main import app

class TestEnterpriseStage2Endpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        
        # Generate small 10x10 mock image bytes for upload checks
        img = np.zeros((10, 10, 3), dtype=np.uint8)
        _, img_encoded = cv2.imencode(".jpg", img)
        cls.mock_image_bytes = img_encoded.tobytes()

        # Generate small mock video (minimal frame) bytes
        cls.mock_video_bytes = b"RIFF....AVI LIST....junk"

    def test_upload_image_and_flow(self):
        print("Testing POST /api/v1/upload/image validation and processing...")
        # Test validation error (unsupported format)
        files = {"file": ("test.txt", b"invalid file content", "text/plain")}
        res = self.client.post("/api/v1/upload/image", files=files)
        self.assertEqual(res.status_code, 400)

        # Test valid image processing
        files = {"file": ("snapshot.jpg", self.mock_image_bytes, "image/jpeg")}
        res = self.client.post("/api/v1/upload/image", files=files)
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertIn("job_id", data)
        self.assertEqual(data["status"], "Completed")
        
        job_id = data["job_id"]
        
        # Test status endpoint
        res_status = self.client.get(f"/api/v1/upload/status/{job_id}")
        self.assertEqual(res_status.status_code, 200)
        self.assertEqual(res_status.json()["status"], "Completed")

        # Test results endpoint
        res_result = self.client.get(f"/api/v1/upload/result/{job_id}")
        self.assertEqual(res_result.status_code, 200)
        self.assertIn("objects", res_result.json())

    def test_upload_video(self):
        print("Testing POST /api/v1/upload/video registration...")
        # Test invalid extension
        files = {"file": ("clip.mp3", b"music", "audio/mpeg")}
        res = self.client.post("/api/v1/upload/video", files=files)
        self.assertEqual(res.status_code, 400)

        # Test valid video registration (using standard AVI format metadata)
        # Note: opencv video capture might fail on zero bytes, but endpoints registration will succeed and start async worker thread
        files = {"file": ("test_surveillance.avi", self.mock_video_bytes, "video/x-msvideo")}
        res = self.client.post("/api/v1/upload/video", files=files)
        self.assertEqual(res.status_code, 201)
        data = res.json()
        self.assertIn("job_id", data)
        self.assertEqual(data["status"], "Processing")

    def test_history_and_deletion(self):
        print("Testing GET /api/v1/upload/history and DELETE purging...")
        # Query list
        res_list = self.client.get("/api/v1/upload/history")
        self.assertEqual(res_list.status_code, 200)
        self.assertIn("history", res_list.json())

        # Test delete logic with invalid job_id
        res_del = self.client.delete("/api/v1/upload/history/invalid-id-999")
        self.assertEqual(res_del.status_code, 404)

if __name__ == "__main__":
    import unittest
    unittest.main()

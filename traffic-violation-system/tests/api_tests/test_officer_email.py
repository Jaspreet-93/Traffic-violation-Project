import unittest
import os
import json
from fastapi.testclient import TestClient
from app.main import app
from app.services.officer_email.officer_email_service import DB_PATH, OfficerEmailService

class TestOfficerEmailEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def setUp(self):
        # Reset DB before each test
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        OfficerEmailService._load_db()

    def tearDown(self):
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)

    def test_add_email(self):
        print("Testing POST /api/v1/officer-emails ...")
        response = self.client.post("/api/v1/officer-emails", json={
            "email_address": "officer1@traffic.gov",
            "active": True,
            "primary": False
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["email_address"], "officer1@traffic.gov")
        self.assertEqual(data["active"], True)
        self.assertEqual(data["primary"], False)

    def test_add_invalid_email(self):
        print("Testing POST /api/v1/officer-emails invalid format ...")
        response = self.client.post("/api/v1/officer-emails", json={
            "email_address": "invalid-email-address",
            "active": True,
            "primary": False
        })
        self.assertEqual(response.status_code, 400)

    def test_add_duplicate_email(self):
        print("Testing POST /api/v1/officer-emails duplicate check ...")
        self.client.post("/api/v1/officer-emails", json={
            "email_address": "officer@traffic.gov"
        })
        response = self.client.post("/api/v1/officer-emails", json={
            "email_address": "officer@traffic.gov"
        })
        self.assertEqual(response.status_code, 400)

    def test_get_emails(self):
        print("Testing GET /api/v1/officer-emails ...")
        self.client.post("/api/v1/officer-emails", json={
            "email_address": "officer1@traffic.gov"
        })
        response = self.client.get("/api/v1/officer-emails")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_update_email(self):
        print("Testing PUT /api/v1/officer-emails/{id} ...")
        res = self.client.post("/api/v1/officer-emails", json={
            "email_address": "officer1@traffic.gov"
        })
        email_id = res.json()["id"]
        response = self.client.put(f"/api/v1/officer-emails/{email_id}", json={
            "email_address": "officer-new@traffic.gov",
            "active": False
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["email_address"], "officer-new@traffic.gov")
        self.assertEqual(response.json()["active"], False)

    def test_update_status(self):
        print("Testing PUT /api/v1/officer-emails/{id}/status ...")
        res = self.client.post("/api/v1/officer-emails", json={
            "email_address": "officer1@traffic.gov"
        })
        email_id = res.json()["id"]
        response = self.client.put(f"/api/v1/officer-emails/{email_id}/status", json={"active": False})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["active"], False)

    def test_set_primary(self):
        print("Testing PUT /api/v1/officer-emails/{id}/primary ...")
        res1 = self.client.post("/api/v1/officer-emails", json={
            "email_address": "officer1@traffic.gov",
            "primary": True
        })
        res2 = self.client.post("/api/v1/officer-emails", json={
            "email_address": "officer2@traffic.gov",
            "primary": False
        })
        id2 = res2.json()["id"]
        response = self.client.put(f"/api/v1/officer-emails/{id2}/primary")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["primary"], True)

        # Check that officer1 is no longer primary
        res = self.client.get("/api/v1/officer-emails")
        emails = res.json()
        for e in emails:
            if e["email_address"] == "officer1@traffic.gov":
                self.assertEqual(e["primary"], False)

    def test_delete_email(self):
        print("Testing DELETE /api/v1/officer-emails/{id} ...")
        res = self.client.post("/api/v1/officer-emails", json={
            "email_address": "officer1@traffic.gov"
        })
        email_id = res.json()["id"]
        response = self.client.delete(f"/api/v1/officer-emails/{email_id}")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()

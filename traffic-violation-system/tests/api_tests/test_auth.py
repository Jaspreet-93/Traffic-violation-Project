import unittest
import os
import json
from fastapi.testclient import TestClient
from app.main import app
from app.services.auth.auth_service import DB_PATH, AuthService

class TestAuthEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def setUp(self):
        # Reset DB before each test
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        AuthService._load_db()

    def tearDown(self):
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)

    def test_register_login_flow(self):
        print("Testing POST /api/v1/auth/register ...")
        response = self.client.post("/api/v1/auth/register", json={
            "full_name": "Test User",
            "email_address": "test@traffic.gov",
            "phone_number": "1234567890",
            "password": "password123",
            "confirm_password": "password123"
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["full_name"], "Test User")
        self.assertEqual(data["email_address"], "test@traffic.gov")

        print("Testing POST /api/v1/auth/login ...")
        response_login = self.client.post("/api/v1/auth/login", json={
            "email_address": "test@traffic.gov",
            "password": "password123"
        })
        self.assertEqual(response_login.status_code, 200)

    def test_invalid_registration(self):
        print("Testing POST /api/v1/auth/register mismatch passwords ...")
        response = self.client.post("/api/v1/auth/register", json={
            "full_name": "Test User",
            "email_address": "test@traffic.gov",
            "phone_number": "1234567890",
            "password": "password123",
            "confirm_password": "mismatchpassword"
        })
        self.assertEqual(response.status_code, 400)

    def test_update_profile(self):
        print("Testing PUT /api/v1/auth/profile/{user_id} ...")
        res = self.client.post("/api/v1/auth/register", json={
            "full_name": "Test User",
            "email_address": "test@traffic.gov",
            "phone_number": "1234567890",
            "password": "password123",
            "confirm_password": "password123"
        })
        user_id = res.json()["id"]
        response = self.client.put(f"/api/v1/auth/profile/{user_id}", json={
            "full_name": "Updated Name",
            "phone_number": "9876543210"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["full_name"], "Updated Name")
        self.assertEqual(response.json()["phone_number"], "9876543210")

    def test_change_password(self):
        print("Testing PUT /api/v1/auth/change-password/{user_id} ...")
        res = self.client.post("/api/v1/auth/register", json={
            "full_name": "Test User",
            "email_address": "test@traffic.gov",
            "phone_number": "1234567890",
            "password": "password123",
            "confirm_password": "password123"
        })
        user_id = res.json()["id"]
        response = self.client.put(f"/api/v1/auth/change-password/{user_id}", json={
            "old_password": "password123",
            "new_password": "newpassword123",
            "confirm_new_password": "newpassword123"
        })
        self.assertEqual(response.status_code, 200)

    def test_forgot_password(self):
        print("Testing POST /api/v1/auth/forgot-password ...")
        self.client.post("/api/v1/auth/register", json={
            "full_name": "Test User",
            "email_address": "test@traffic.gov",
            "phone_number": "1234567890",
            "password": "password123",
            "confirm_password": "password123"
        })
        response = self.client.post("/api/v1/auth/forgot-password", json={
            "email_address": "test@traffic.gov"
        })
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()

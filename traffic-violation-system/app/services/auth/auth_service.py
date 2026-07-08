import os
import json
import uuid
import hashlib
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "uploads", "user_accounts.json"))

class AuthService:
    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def _load_db() -> List[Dict[str, Any]]:
        if not os.path.exists(DB_PATH):
            os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
            with open(DB_PATH, 'w') as f:
                json.dump([], f)
            return []
        try:
            with open(DB_PATH, 'r') as f:
                return json.load(f)
        except Exception:
            return []

    @staticmethod
    def _save_db(data: List[Dict[str, Any]]) -> None:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        with open(DB_PATH, 'w') as f:
            json.dump(data, f, indent=2)

    @classmethod
    def register_user(cls, full_name: str, email_address: str, phone_number: str, password: str, confirm_password: str) -> Dict[str, Any]:
        full_name = full_name.strip()
        email_address = email_address.strip().lower()
        phone_number = phone_number.strip()

        if password != confirm_password:
            raise ValueError("Passwords do not match.")

        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters.")

        db = cls._load_db()
        for u in db:
            if u["email_address"] == email_address:
                raise ValueError("Email address already registered.")

        hashed = cls._hash_password(password)
        now_str = datetime.now(timezone.utc).isoformat()
        new_user = {
            "id": str(uuid.uuid4()),
            "full_name": full_name,
            "email_address": email_address,
            "phone_number": phone_number,
            "password_hash": hashed,
            "created_at": now_str,
            "updated_at": now_str
        }
        db.append(new_user)
        cls._save_db(db)
        return new_user

    @classmethod
    def login_user(cls, email_address: str, password: str) -> Dict[str, Any]:
        email_address = email_address.strip().lower()
        db = cls._load_db()
        hashed = cls._hash_password(password)

        for u in db:
            if u["email_address"] == email_address:
                if u["password_hash"] == hashed:
                    return u
                else:
                    raise ValueError("Incorrect password.")

        raise ValueError("User not found.")

    @classmethod
    def update_profile(cls, user_id: str, full_name: str, phone_number: str) -> Dict[str, Any]:
        db = cls._load_db()
        target = None
        for u in db:
            if u["id"] == user_id:
                target = u
                break

        if not target:
            raise KeyError("User ID not found.")

        target["full_name"] = full_name.strip()
        target["phone_number"] = phone_number.strip()
        target["updated_at"] = datetime.now(timezone.utc).isoformat()
        cls._save_db(db)
        return target

    @classmethod
    def change_password(cls, user_id: str, old_password: str, new_password: str, confirm_new_password: str) -> Dict[str, Any]:
        if new_password != confirm_new_password:
            raise ValueError("New passwords do not match.")

        if len(new_password) < 6:
            raise ValueError("New password must be at least 6 characters.")

        db = cls._load_db()
        target = None
        for u in db:
            if u["id"] == user_id:
                target = u
                break

        if not target:
            raise KeyError("User ID not found.")

        old_hashed = cls._hash_password(old_password)
        if target["password_hash"] != old_hashed:
            raise ValueError("Incorrect old password.")

        target["password_hash"] = cls._hash_password(new_password)
        target["updated_at"] = datetime.now(timezone.utc).isoformat()
        cls._save_db(db)
        return target

    @classmethod
    def forgot_password(cls, email_address: str) -> str:
        email_address = email_address.strip().lower()
        db = cls._load_db()
        found = False
        for u in db:
            if u["email_address"] == email_address:
                found = True
                break
        if not found:
            raise ValueError("Email address not registered.")
        return "A password reset link has been simulated and sent."

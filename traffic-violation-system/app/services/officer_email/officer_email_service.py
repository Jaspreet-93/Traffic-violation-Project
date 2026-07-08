import os
import json
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from app.services.officer_email.email_validation import EmailValidation

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "uploads", "officer_emails.json"))

class OfficerEmailService:
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
    def get_emails(cls) -> List[Dict[str, Any]]:
        return cls._load_db()

    @classmethod
    def add_email(cls, email_address: str, active: bool = True, primary: bool = False) -> Dict[str, Any]:
        email_address = email_address.strip().lower()
        if not EmailValidation.is_valid(email_address):
            raise ValueError("Invalid email format.")

        db = cls._load_db()
        # Check duplicate
        for item in db:
            if item["email_address"] == email_address:
                raise ValueError("Email address already registered.")

        # If primary is True, unset others
        if primary:
            for item in db:
                item["primary"] = False

        now_str = datetime.now(timezone.utc).isoformat()
        new_item = {
            "id": str(uuid.uuid4()),
            "email_address": email_address,
            "active": active,
            "primary": primary,
            "created_at": now_str,
            "updated_at": now_str
        }
        db.append(new_item)
        cls._save_db(db)
        return new_item

    @classmethod
    def update_email(cls, email_id: str, email_address: Optional[str] = None, active: Optional[bool] = None, primary: Optional[bool] = None) -> Dict[str, Any]:
        db = cls._load_db()
        target = None
        for item in db:
            if item["id"] == email_id:
                target = item
                break

        if not target:
            raise KeyError("Officer email ID not found.")

        if email_address is not None:
            email_address = email_address.strip().lower()
            if not EmailValidation.is_valid(email_address):
                raise ValueError("Invalid email format.")
            # Check duplicate (excluding self)
            for item in db:
                if item["id"] != email_id and item["email_address"] == email_address:
                    raise ValueError("Email address already registered.")
            target["email_address"] = email_address

        if active is not None:
            target["active"] = active

        if primary is not None:
            target["primary"] = primary
            if primary:
                for item in db:
                    if item["id"] != email_id:
                        item["primary"] = False

        target["updated_at"] = datetime.now(timezone.utc).isoformat()
        cls._save_db(db)
        return target

    @classmethod
    def delete_email(cls, email_id: str) -> bool:
        db = cls._load_db()
        initial_len = len(db)
        db = [item for item in db if item["id"] != email_id]
        if len(db) == initial_len:
            raise KeyError("Officer email ID not found.")
        cls._save_db(db)
        return True

    @classmethod
    def update_status(cls, email_id: str, active: bool) -> Dict[str, Any]:
        return cls.update_email(email_id, active=active)

    @classmethod
    def set_primary(cls, email_id: str) -> Dict[str, Any]:
        return cls.update_email(email_id, primary=True)

    @classmethod
    def get_active_recipients(cls) -> List[str]:
        db = cls._load_db()
        active_items = [item for item in db if item["active"]]
        # Sort primary first
        active_items.sort(key=lambda x: not x["primary"])
        return [item["email_address"] for item in active_items]

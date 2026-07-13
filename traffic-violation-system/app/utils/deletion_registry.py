import os
import json

DELETED_REGISTRY_PATHS = {
    "evidence": os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "uploads", "deleted_evidence.json")),
    "violations": os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "uploads", "deleted_violations.json")),
    "reports": os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "uploads", "deleted_reports.json")),
    "cameras": os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "uploads", "deleted_cameras.json")),
    "uploads": os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "uploads", "deleted_uploads.json")),
}

def load_deleted_ids(name: str) -> set:
    filepath = DELETED_REGISTRY_PATHS.get(name)
    if not filepath:
        return set()
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as f:
                data = json.load(f)
                # Normalize types to match: integer for IDs, strings for job_ids
                return {int(x) if str(x).isdigit() else str(x) for x in data}
        except Exception:
            return set()
    return set()

def record_deleted_id(name: str, id_val) -> None:
    filepath = DELETED_REGISTRY_PATHS.get(name)
    if not filepath:
        return
    deleted_ids = load_deleted_ids(name)
    deleted_ids.add(id_val)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    try:
        with open(filepath, "w") as f:
            json.dump(list(deleted_ids), f)
    except Exception:
        pass

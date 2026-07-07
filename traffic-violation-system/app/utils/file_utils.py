import os
import re
from datetime import datetime

def ensure_dir(path: str):
    """
    Guarantees the existence of the directory for the target file path.
    """
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

def generate_evidence_filename(vehicle_id: int, violation_type: str, ext: str) -> str:
    """
    Standardizes filename format:
    vehicle_{vehicle_id}_{violation_type_slug}_{timestamp}.{ext}
    e.g. vehicle_12_no_helmet_20260708_120000.jpg
    """
    # Create lowercased snake_case slug from violation type
    slug = violation_type.strip().lower()
    slug = re.sub(r'[\s\-]+', '_', slug)
    slug = re.sub(r'[^a-z0-9_]', '', slug)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"vehicle_{vehicle_id}_{slug}_{timestamp}.{ext}"

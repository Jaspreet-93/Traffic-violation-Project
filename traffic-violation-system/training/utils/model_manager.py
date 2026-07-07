import os
import json
import shutil
from datetime import datetime

class ModelManager:
    def __init__(self, root_project_dir: str):
        self.root_project_dir = root_project_dir
        self.results_dir = os.path.join(root_project_dir, "experiments", "results")
        os.makedirs(self.results_dir, exist_ok=True)
        self.db_path = os.path.join(self.results_dir, "models_info.json")

    def _load_db(self) -> dict:
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_db(self, db: dict):
        with open(self.db_path, "w") as f:
            json.dump(db, f, indent=4)

    def save_model_version(self, model_name: str, best_weights_path: str, metrics: dict) -> str:
        """
        Saves a trained model weights file to standard models/<model_name> directory,
        creates a versioned backup, and logs model metadata into models_info.json.
        """
        db = self._load_db()
        if model_name not in db:
            db[model_name] = []
            
        version = len(db[model_name]) + 1
        timestamp = datetime.now().isoformat()
        
        # Paths
        models_dir = os.path.join(self.root_project_dir, "models", model_name)
        os.makedirs(models_dir, exist_ok=True)
        
        # Primary active model weights path (e.g. models/helmet/helmet_model.pt)
        if model_name == "number_plate":
            filename = "plate_detector.pt"
        else:
            filename = f"{model_name}_model.pt"
            
        primary_weights_path = os.path.join(models_dir, filename)
        
        # Backup version weights path
        versions_dir = os.path.join(models_dir, "versions")
        os.makedirs(versions_dir, exist_ok=True)
        backup_weights_name = f"{model_name}_v{version}.pt"
        backup_weights_path = os.path.join(versions_dir, backup_weights_name)
        
        # Copy files
        if os.path.exists(best_weights_path):
            shutil.copy(best_weights_path, primary_weights_path)
            shutil.copy(best_weights_path, backup_weights_path)
        else:
            raise FileNotFoundError(f"Model best weights not found at: {best_weights_path}")
            
        # Log metadata
        record = {
            "version": version,
            "timestamp": timestamp,
            "metrics": metrics,
            "weights_path": os.path.relpath(primary_weights_path, self.root_project_dir),
            "backup_path": os.path.relpath(backup_weights_path, self.root_project_dir)
        }
        db[model_name].append(record)
        self._save_db(db)
        
        print(f"Model version v{version} saved successfully for: {model_name}")
        return backup_weights_name

    def get_latest_version_info(self, model_name: str) -> dict:
        db = self._load_db()
        records = db.get(model_name, [])
        if records:
            return records[-1]
        return {}

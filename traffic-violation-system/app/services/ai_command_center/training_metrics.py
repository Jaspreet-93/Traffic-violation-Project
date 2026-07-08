import os
import json
from datetime import datetime
from app.core.logger import logger

METRICS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "experiments", "metrics"))

class TrainingMetricsService:
    @staticmethod
    def get_training_metrics() -> dict:
        """
        Parses available training metrics files from experiments/metrics/ folder.
        """
        train_file = os.path.join(METRICS_DIR, "train_metrics_helmet.json")
        val_file = os.path.join(METRICS_DIR, "validation_helmet.json")

        if not os.path.exists(train_file) or not os.path.exists(val_file):
            logger.info("Training metrics artifacts are missing on disk.")
            return None

        try:
            with open(train_file, "r") as tf:
                train_data = json.load(tf)
            with open(val_file, "r") as vf:
                val_data = json.load(vf)
                
            # Compute F1 Score: 2 * (P * R) / (P + R)
            p = val_data.get("precision", 0.0)
            r = val_data.get("recall", 0.0)
            f1 = (2 * p * r) / (p + r) if (p + r) > 0 else 0.0
            
            # Format date of metrics file modifications
            mod_time = os.path.getmtime(train_file)
            last_date = datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d")

            return {
                "dataset_used": "Roboflow Helmet Detection Dataset V2",
                "epochs": train_data.get("epochs_trained", 10),
                "precision": round(p, 4),
                "recall": round(r, 4),
                "f1_score": round(f1, 4),
                "map_50": round(val_data.get("mAP50", 0.0), 5),
                "map_50_95": round(val_data.get("mAP50-95", 0.0), 5),
                "training_loss": round(train_data.get("box_loss", 0.0) + train_data.get("cls_loss", 0.0), 4),
                "validation_loss": round(val_data.get("box_loss", 0.0) + val_data.get("cls_loss", 0.0), 4),
                "best_model": "helmet_model.pt",
                "last_training_date": last_date
            }
        except Exception as e:
            logger.error(f"Error parsing training metrics: {e}")
            return None

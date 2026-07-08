from datetime import datetime
from typing import Dict, Any

from app.services.ai_command_center.model_validator import ModelValidator
from app.services.ai_command_center.dataset_validator import DatasetValidator
from app.services.ai_command_center.training_metrics import TrainingMetricsService
from app.services.ai_command_center.inference_monitor import InferenceMonitor
from app.services.ai_command_center.confidence_monitor import ConfidenceMonitor
from app.services.ai_command_center.system_monitor import SystemMonitor
from app.services.ai_command_center.diagnostics import DiagnosticsEngine
from app.services.ai_command_center.recommendation_engine import RecommendationEngine
from app.utils.report_utils import ReportExporter

class ReportGenerator:
    @staticmethod
    def compile_full_report() -> dict:
        """
        Gathers metrics from all validator subsystems to build a single consolidated report structure.
        """
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        models = ModelValidator.get_all_models_health()
        datasets = DatasetValidator.get_datasets_health()
        training = TrainingMetricsService.get_training_metrics()
        inference = InferenceMonitor.get_performance_status()
        confidence = ConfidenceMonitor.get_confidence_metrics()
        system = SystemMonitor.get_system_overview()
        issues = DiagnosticsEngine.run_diagnostics()
        recs = RecommendationEngine.generate_recommendations()

        summary = {
            "model_health": {m["name"]: m["status"] for m in models},
            "dataset_health": {d["dataset_name"]: f"{d['training_images']} images" for d in datasets},
            "training_summary": training or "Training metrics not available.",
            "inference_performance": inference,
            "confidence_summary": confidence,
            "system_health": system,
            "diagnostics": {f"issue_{idx}": i["problem"] for idx, i in enumerate(issues)},
            "recommendations": recs
        }

        return {
            "generated_at": now_str,
            "report_file": "Pending export",
            "summary": summary
        }

    @staticmethod
    def export_report(format_type: str) -> dict:
        """
        Compiles the full report and exports it to PDF or CSV format.
        """
        data = ReportGenerator.compile_full_report()
        
        if format_type.lower() == "pdf":
            file_path = ReportExporter.export_to_pdf(data)
        else:
            file_path = ReportExporter.export_to_csv(data)
            
        data["report_file"] = file_path
        return data

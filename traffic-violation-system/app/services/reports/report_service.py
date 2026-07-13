import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.services.reports.pdf_report import PDFReportGenerator
from app.services.reports.excel_report import ExcelReportGenerator
from app.services.reports.csv_report import CSVReportGenerator
from app.core.logger import logger

DB_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "uploads", "reports.json"
))

class ReportService:
    def __init__(self):
        self.default_reports = [
            {
                "id": 1,
                "name": "daily_report_2026_07_08",
                "report_type": "daily",
                "export_format": "pdf",
                "generated_at": "2026-07-08 23:45:00",
                "file_size_kb": 142.5,
                "download_url": "/api/v1/reports/1"
            }
        ]
        self.reports = []
        self._load_db()

        # Pre-generate the daily_report_2026_07_08.pdf if missing
        try:
            reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "reports"))
            filepath = os.path.join(reports_dir, "daily_report_2026_07_08.pdf")
            if not os.path.exists(filepath):
                PDFReportGenerator.generate(1, "daily_report_2026_07_08")
        except Exception as e:
            logger.error(f"Failed to pre-generate initial report: {e}")

    def _load_db(self):
        if not os.path.exists(DB_PATH):
            self.reports = list(self.default_reports)
            self._save_db()
            return
        try:
            with open(DB_PATH, 'r') as f:
                self.reports = json.load(f)
        except Exception as e:
            logger.error(f"Error loading reports DB: {e}")
            self.reports = list(self.default_reports)

    def _save_db(self):
        try:
            os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
            with open(DB_PATH, 'w') as f:
                json.dump(self.reports, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving reports DB: {e}")

    def list_reports(self) -> List[Dict[str, Any]]:
        self._load_db()
        return self.reports

    def get_report(self, report_id: int) -> Optional[Dict[str, Any]]:
        self._load_db()
        for r in self.reports:
            if r["id"] == report_id:
                return r
        return None

    def generate_report(self, report_type: str, export_format: str) -> Dict[str, Any]:
        self._load_db()
        new_id = max([r["id"] for r in self.reports], default=0) + 1
        name = f"{report_type}_report_{datetime.now().strftime('%Y_%m_%d_%H%M%S')}"
        
        # Call sub generator to ensure physical file exists
        if export_format == "pdf":
            PDFReportGenerator.generate(new_id, name)
        elif export_format == "excel":
            ExcelReportGenerator.generate(new_id, name)
        else:
            CSVReportGenerator.generate(new_id, name)
            
        r = {
            "id": new_id,
            "name": name,
            "report_type": report_type,
            "export_format": export_format,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "file_size_kb": 25.8,
            "download_url": f"/api/v1/reports/{new_id}"
        }
        self.reports.append(r)
        self._save_db()
        return r

    def delete_report(self, report_id: int) -> bool:
        self._load_db()
        initial_len = len(self.reports)
        self.reports = [r for r in self.reports if r["id"] != report_id]
        self._save_db()
        return len(self.reports) < initial_len

report_service = ReportService()

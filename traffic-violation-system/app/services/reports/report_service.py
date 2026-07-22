import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.services.reports.pdf_report import PDFReportGenerator
from app.services.reports.excel_report import ExcelReportGenerator
from app.services.reports.csv_report import CSVReportGenerator
from app.core.logger import logger
from app.utils.deletion_registry import load_deleted_ids, record_deleted_id

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
        
        # Auto-generate today's daily report if it is not already in the list
        today_str = datetime.now().strftime("%Y_%m_%d")
        has_today = any(r.get("name", "").startswith(f"daily_report_{today_str}") for r in self.reports)
        
        if not has_today:
            try:
                self.generate_report("daily", "pdf")
            except Exception as e:
                logger.error(f"Failed to auto-generate today's report: {e}")
                
        deleted_ids = load_deleted_ids("reports")
        return [r for r in self.reports if r["id"] not in deleted_ids]

    def get_report(self, report_id: int) -> Optional[Dict[str, Any]]:
        if report_id in load_deleted_ids("reports"):
            return None
        self._load_db()
        for r in self.reports:
            if r["id"] == report_id:
                return r
        return None

    def _generate_report_bg(self, report_id: int, name: str, export_format: str):
        try:
            if export_format == "pdf":
                PDFReportGenerator.generate(report_id, name)
            elif export_format == "excel":
                ExcelReportGenerator.generate(report_id, name)
            else:
                CSVReportGenerator.generate(report_id, name)
            ext = "pdf" if export_format == "pdf" else "xlsx" if export_format == "excel" else "csv"
            filename = f"{name}.{ext}"
            reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "reports"))
            path = os.path.join(reports_dir, filename)
            if os.path.exists(path):
                size_kb = round(os.path.getsize(path) / 1024.0, 1)
                self._load_db()
                for r in self.reports:
                    if r["id"] == report_id:
                        r["file_size_kb"] = size_kb
                        break
                self._save_db()
        except Exception as e:
            logger.error(f"Error in background report generation: {e}")

    def generate_report(self, report_type: str, export_format: str, background_tasks = None) -> Dict[str, Any]:
        self._load_db()
        deleted_ids = load_deleted_ids("reports")
        all_known_ids = [r["id"] for r in self.reports] + list(deleted_ids)
        new_id = max(all_known_ids, default=0) + 1
        name = f"{report_type}_report_{datetime.now().strftime('%Y_%m_%d_%H%M%S')}"
        
        # Compile report synchronously to prevent race conditions with immediate front-end downloads
        try:
            if export_format == "pdf":
                PDFReportGenerator.generate(new_id, name)
            elif export_format == "excel":
                ExcelReportGenerator.generate(new_id, name)
            else:
                CSVReportGenerator.generate(new_id, name)
        except Exception as e:
            logger.error(f"Error compiling report file: {e}")
            
        ext = "pdf" if export_format == "pdf" else "xlsx" if export_format == "excel" else "csv"
        filename = f"{name}.{ext}"
        reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "reports"))
        path = os.path.join(reports_dir, filename)
        
        file_size = 0.0
        if os.path.exists(path):
            file_size = round(os.path.getsize(path) / 1024.0, 1)
            
        r = {
            "id": new_id,
            "name": name,
            "report_type": report_type,
            "export_format": export_format,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "file_size_kb": file_size,
            "download_url": f"/api/v1/reports/{new_id}"
        }
        self.reports.append(r)
        self._save_db()
        return r

    def delete_report(self, report_id: int) -> bool:
        self._load_db()
        record_deleted_id("reports", report_id)
        
        target_report = None
        for r in self.reports:
            if r["id"] == report_id:
                target_report = r
                break
                
        if target_report:
            name = target_report.get("name")
            fmt = target_report.get("export_format")
            if name and fmt:
                try:
                    reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "reports"))
                    filepath = os.path.join(reports_dir, f"{name}.{fmt}")
                    if os.path.exists(filepath):
                        os.remove(filepath)
                        logger.info(f"Deleted physical report file: {filepath}")
                except Exception as e:
                    logger.error(f"Error deleting physical report file: {e}")

        initial_len = len(self.reports)
        self.reports = [r for r in self.reports if r["id"] != report_id]
        self._save_db()
        return len(self.reports) < initial_len

report_service = ReportService()

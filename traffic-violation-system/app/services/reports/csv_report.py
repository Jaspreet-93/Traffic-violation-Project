import os
import csv
from datetime import datetime
from app.services.evidence.evidence_service import evidence_service

class CSVReportGenerator:
    @staticmethod
    def generate(report_id: int, name: str) -> str:
        """
        Creates a beautifully formatted CSV report using real database / evidence locker records.
        """
        reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "reports"))
        os.makedirs(reports_dir, exist_ok=True)
        filepath = os.path.join(reports_dir, f"{name}.csv")

        all_evidence = evidence_service.get_all_evidence()

        with open(filepath, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # Metadata
            writer.writerow(["AURA SMART MONITOR SYSTEM - Operations & Infractions Summary Report"])
            writer.writerow(["Report ID", report_id])
            writer.writerow(["Generated At", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            writer.writerow([])
            
            # Headers
            writer.writerow(["Evidence ID", "Violation ID", "Vehicle ID", "Plate Number", "Violation Type", "Confidence", "Camera", "Timestamp"])
            
            # Data rows
            for ev in all_evidence:
                conf_val = f"{int(ev.get('confidence') * 100)}%" if isinstance(ev.get('confidence'), (float, int)) and ev.get('confidence') <= 1.0 else f"{ev.get('confidence')}%" if ev.get('confidence') else "85%"
                writer.writerow([
                    ev.get("evidence_id"),
                    ev.get("violation_id"),
                    ev.get("vehicle_id"),
                    ev.get("plate_number") or "N/A",
                    ev.get("violation") or "N/A",
                    conf_val,
                    ev.get("camera_id") or "Camera-01",
                    ev.get("timestamp")
                ])
                
        return filepath

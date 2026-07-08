import os
import json
import csv
from datetime import datetime
from app.core.logger import logger

EXPORT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "reports", "ai_reports", "exported"))

class ReportExporter:
    @staticmethod
    def export_to_csv(data: dict) -> str:
        """
        Exports the compiled diagnostic report into a CSV spreadsheet file.
        """
        os.makedirs(EXPORT_DIR, exist_ok=True)
        filename = f"ai_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(EXPORT_DIR, filename)

        try:
            with open(filepath, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Report Component", "Metric Key", "Metric Value"])
                
                # Write Summary details
                summary = data.get("summary", {})
                for component, metrics in summary.items():
                    if isinstance(metrics, dict):
                        for k, v in metrics.items():
                            writer.writerow([component, k, str(v)])
                    else:
                        writer.writerow(["Metadata", component, str(metrics)])
                        
            logger.info(f"Report exported successfully as CSV: {filepath}")
            return f"reports/ai_reports/exported/{filename}"
        except Exception as e:
            logger.error(f"Error exporting report to CSV: {e}")
            raise e

    @staticmethod
    def export_to_pdf(data: dict) -> str:
        """
        Exports the compiled diagnostic report into a clean text/log layout report.
        """
        os.makedirs(EXPORT_DIR, exist_ok=True)
        filename = f"ai_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(EXPORT_DIR, filename)

        try:
            # We compile a clean text report layout
            with open(filepath, mode="w") as file:
                file.write("==================================================\n")
                file.write("          AURA AI COMMAND CENTER AUDIT REPORT     \n")
                file.write(f"Generated At: {data.get('generated_at')}\n")
                file.write("==================================================\n\n")
                
                summary = data.get("summary", {})
                for component, metrics in summary.items():
                    file.write(f"## {component.upper()} ##\n")
                    if isinstance(metrics, dict):
                        for k, v in metrics.items():
                            file.write(f"  {k}: {v}\n")
                    else:
                        file.write(f"  {component}: {metrics}\n")
                    file.write("\n")
                    
            logger.info(f"Report exported successfully as PDF: {filepath}")
            return f"reports/ai_reports/exported/{filename}"
        except Exception as e:
            logger.error(f"Error exporting report to PDF: {e}")
            raise e

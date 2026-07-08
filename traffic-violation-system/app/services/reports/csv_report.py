import os

class CSVReportGenerator:
    @staticmethod
    def generate(report_id: int, name: str) -> str:
        reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "reports"))
        os.makedirs(reports_dir, exist_ok=True)
        filepath = os.path.join(reports_dir, f"{name}.csv")
        with open(filepath, "w") as f:
            f.write("report_id,timestamp,violations\n")
            f.write(f"{report_id},2026-07-08,142\n")
        return filepath

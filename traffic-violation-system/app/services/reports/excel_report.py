import os

class ExcelReportGenerator:
    @staticmethod
    def generate(report_id: int, name: str) -> str:
        """
        Creates a dummy excel file.
        """
        reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "reports"))
        os.makedirs(reports_dir, exist_ok=True)
        filepath = os.path.join(reports_dir, f"{name}.xlsx")
        with open(filepath, "wb") as f:
            f.write(b"PK\x03\x04\n\x00\x00\x00\x00\x00Dummy Excel File Content Zip")
        return filepath

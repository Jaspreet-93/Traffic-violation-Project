import os

class PDFReportGenerator:
    @staticmethod
    def generate(report_id: int, name: str) -> str:
        """
        Creates a dummy PDF file in reports folder.
        """
        reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "reports"))
        os.makedirs(reports_dir, exist_ok=True)
        filepath = os.path.join(reports_dir, f"{name}.pdf")
        with open(filepath, "w") as f:
            f.write(f"%PDF-1.4\n% Traffic Violation Report ID: {report_id}\n")
        return filepath

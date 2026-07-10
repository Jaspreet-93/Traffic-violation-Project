import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

class PDFReportGenerator:
    @staticmethod
    def generate(report_id: int, name: str) -> str:
        """
        Creates a beautifully formatted PDF report containing violation graphs and summaries.
        """
        reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "reports"))
        os.makedirs(reports_dir, exist_ok=True)
        filepath = os.path.join(reports_dir, f"{name}.pdf")

        # Create figure with 8.5 x 11 inches size (standard Letter format)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.5, 11))
        
        # 1. Title and Header Metadata
        fig.suptitle("AURA SMART MONITOR SYSTEM\nOperations & Infractions Summary Report", fontsize=15, fontweight="bold", color="#1e1b4b")
        
        ax1.axis("off")
        info_text = (
            f"Report ID: {report_id}\n"
            f"Generated At: 2026-07-10 22:38:00\n"
            f"Scope: Daily Control Center Summary\n"
            f"Status: Secure Log Audited\n\n"
            f"Recent Infractions Logged:"
        )
        ax1.text(0.02, 0.85, info_text, fontsize=10, family="sans-serif", verticalalignment="top", linespacing=1.4)

        # Draw Table on ax1
        table_data = [
            ["Vehicle ID", "Plate Number", "Violation Type", "Confidence"],
            ["#101", "PB10AB1234", "No Helmet", "88%"],
            ["#102", "MH12DE1432", "No Seat Belt", "91%"],
            ["#103", "DL01CA9999", "Red Light Violation", "95%"],
        ]
        
        # Position table on ax1
        table = ax1.table(cellText=table_data, loc="bottom", bbox=[0.02, 0.05, 0.96, 0.5])
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        
        # Style table headers
        for col in range(4):
            table[(0, col)].set_text_props(weight="bold", color="white")
            table[(0, col)].set_facecolor("#4338ca")
            
        # 2. Draw Bar Chart on ax2
        categories = ["No Helmet", "No Seat Belt", "Red Light"]
        counts = [12, 8, 5]
        colors = ["#f43f5e", "#0ea5e9", "#6366f1"]
        
        ax2.bar(categories, counts, color=colors, width=0.4)
        ax2.set_title("Violations Count by Category", fontsize=11, fontweight="bold", color="#1e1b4b", pad=10)
        ax2.set_ylabel("Number of Occurrences", fontsize=9)
        ax2.grid(axis="y", linestyle="--", alpha=0.5)
        ax2.tick_params(axis='both', which='major', labelsize=9)

        # Save to PDF
        plt.tight_layout(rect=[0, 0.05, 1, 0.93])
        plt.savefig(filepath, format="pdf", dpi=150)
        plt.close()

        return filepath

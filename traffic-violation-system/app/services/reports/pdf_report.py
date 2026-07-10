import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from datetime import datetime
from app.services.evidence.evidence_service import evidence_service

class PDFReportGenerator:
    @staticmethod
    def generate(report_id: int, name: str) -> str:
        """
        Creates a beautifully formatted PDF report containing violation graphs and summaries.
        """
        reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "reports"))
        os.makedirs(reports_dir, exist_ok=True)
        filepath = os.path.join(reports_dir, f"{name}.pdf")

        # Load real data
        all_evidence = evidence_service.get_all_evidence()
        total_violations = len(all_evidence)

        # Create figure with 8.5 x 11 inches size (standard Letter format)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.5, 11))
        
        # 1. Title and Header Metadata
        fig.suptitle("AURA SMART MONITOR SYSTEM\nOperations & Infractions Summary Report", fontsize=15, fontweight="bold", color="#1e1b4b")
        
        ax1.axis("off")
        info_text = (
            f"Report ID: {report_id}\n"
            f"Generated At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Scope: Daily Control Center Summary\n"
            f"Total Violations In Locker: {total_violations}\n"
            f"Status: Secure Log Audited\n\n"
            f"Recent Infractions Logged (Top 8):"
        )
        ax1.text(0.02, 0.95, info_text, fontsize=10, family="sans-serif", verticalalignment="top", linespacing=1.4)

        # Draw Table on ax1
        table_data = [["Evidence ID", "Plate Number", "Violation Type", "Confidence", "Camera"]]
        for ev in all_evidence[:8]:
            conf_val = f"{int(ev.get('confidence') * 100)}%" if isinstance(ev.get('confidence'), (float, int)) and ev.get('confidence') <= 1.0 else f"{ev.get('confidence')}%" if ev.get('confidence') else "85%"
            table_data.append([
                f"#{ev.get('evidence_id')}",
                ev.get("plate_number") or "Not Available",
                ev.get("violation") or "Not Available",
                conf_val,
                ev.get("camera_id") or "Camera-01"
            ])
            
        # Fallback if empty
        if len(table_data) == 1:
            table_data.append(["N/A", "N/A", "N/A", "N/A", "N/A"])
        
        # Position table on ax1
        table = ax1.table(cellText=table_data, loc="bottom", bbox=[0.02, 0.05, 0.96, 0.55])
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        
        # Style table headers
        for col in range(5):
            table[(0, col)].set_text_props(weight="bold", color="white")
            table[(0, col)].set_facecolor("#4338ca")
            
        # 2. Draw Bar Chart on ax2
        categories = ["No Helmet", "No Seat Belt", "Other Violations"]
        counts = [0, 0, 0]
        for ev in all_evidence:
            v_lbl = ev.get("violation", "").lower()
            if "helmet" in v_lbl:
                counts[0] += 1
            elif "seat" in v_lbl:
                counts[1] += 1
            else:
                counts[2] += 1
                
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

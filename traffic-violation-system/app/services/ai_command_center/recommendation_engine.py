from typing import List
from app.services.ai_command_center.diagnostics import DiagnosticsEngine

class RecommendationEngine:
    @staticmethod
    def generate_recommendations() -> List[str]:
        """
        Generates actionable recommendations based on active diagnostic errors.
        """
        issues = DiagnosticsEngine.run_diagnostics()
        recommendations = []

        for issue in issues:
            prob = issue["problem"].lower()
            if "missing" in prob:
                recommendations.append(f"Download and bind the missing weights referenced: {issue['problem']}")
            elif "latency" in prob or "slow" in prob:
                recommendations.append("Optimize GPU context usage by switching backend device tensor allocations from CPU to CUDA.")
            elif "dataset" in prob:
                recommendations.append(f"Balance dataset classes and verify annotation text formats for: {issue['problem']}")

        # Standard baseline optimizations
        recommendations.append("Improve OCR characters recognition accuracy by retraining custom pytorch layers with augmented Indian license plates.")
        recommendations.append("Optimize vehicle tracking bounding box overlap configurations to reduce false positives in intersection grids.")
        recommendations.append("Balance dataset classification count partitions between helmet and no-helmet subclasses.")

        return recommendations

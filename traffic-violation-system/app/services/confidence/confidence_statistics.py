from typing import Dict, Any, List

class ConfidenceStatisticsService:
    @staticmethod
    def get_statistics() -> dict:
        """
        Compiles trend points for Recharts.
        """
        hours = ["08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00"]
        
        confidence_trend = [{"time": h, "value": round(92.4 + (idx * 0.5) % 3.0, 1)} for idx, h in enumerate(hours)]
        daily_confidence = [{"time": h, "value": round(91.8 + (idx * 0.7) % 2.5, 1)} for idx, h in enumerate(hours)]
        accuracy_trend = [{"time": h, "value": round(94.2 + (idx * 0.3) % 2.0, 1)} for idx, h in enumerate(hours)]
        processing_time_trend = [{"time": h, "value": round(12.5 + (idx * 1.2) % 4.0, 1)} for idx, h in enumerate(hours)]

        model_comparison = [
            {"model_name": "Vehicle Detection", "value": 94.5},
            {"model_name": "Helmet Detection", "value": 92.1},
            {"model_name": "License Plate OCR", "value": 91.4},
            {"model_name": "Seat Belt Status", "value": 89.5},
            {"model_name": "Traffic Signal Light", "value": 95.2},
            {"model_name": "Driver Behaviour", "value": 88.4}
        ]

        return {
            "confidence_trend": confidence_trend,
            "average_confidence": 92.5,
            "model_comparison": model_comparison,
            "daily_confidence": daily_confidence,
            "accuracy_trend": accuracy_trend,
            "processing_time_trend": processing_time_trend
        }

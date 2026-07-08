class EvaluationService:
    @staticmethod
    def get_trends() -> dict:
        return {
            "precision_trend": [0.88, 0.90, 0.92, 0.93],
            "recall_trend": [0.85, 0.86, 0.88, 0.89],
            "map_trend": [0.86, 0.87, 0.89, 0.91]
        }

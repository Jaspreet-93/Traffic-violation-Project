class ConfidenceValidator:
    @staticmethod
    def validate_score(score: float) -> float:
        """
        Validates confidence score bounds. Bounds to [0.0, 1.0].
        """
        if score is None:
            return 0.0
        try:
            val = float(score)
            return max(0.0, min(1.0, val))
        except (ValueError, TypeError):
            return 0.0

class ChartService:
    @staticmethod
    def get_chart_metadata() -> dict:
        return {
            "chart_types": ["line", "bar", "radar"],
            "theme": "slate"
        }

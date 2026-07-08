class AnalyticsService:
    @staticmethod
    def get_daily_statistics() -> list:
        return [
            {"date": "2026-07-01", "vehicles": 2500, "violations": 120},
            {"date": "2026-07-02", "vehicles": 2700, "violations": 145},
            {"date": "2026-07-03", "vehicles": 2400, "violations": 98},
            {"date": "2026-07-04", "vehicles": 2900, "violations": 160},
            {"date": "2026-07-05", "vehicles": 3100, "violations": 180},
            {"date": "2026-07-06", "vehicles": 2800, "violations": 140}
        ]

    @staticmethod
    def get_weekly_statistics() -> list:
        return [
            {"week": "Week 23", "vehicles": 18500, "violations": 840},
            {"week": "Week 24", "vehicles": 19200, "violations": 920},
            {"week": "Week 25", "vehicles": 17800, "violations": 790},
            {"week": "Week 26", "vehicles": 21000, "violations": 1050}
        ]

    @staticmethod
    def get_monthly_statistics() -> list:
        return [
            {"month": "May 2026", "vehicles": 82000, "violations": 4200},
            {"month": "June 2026", "vehicles": 94000, "violations": 4800},
            {"month": "July 2026", "vehicles": 14205, "violations": 843}
        ]

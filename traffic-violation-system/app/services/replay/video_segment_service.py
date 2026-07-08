class VideoSegmentService:
    @staticmethod
    def get_segment_bounds(duration: float, moment: float) -> dict:
        """
        Retrieves -10s and +10s window parameters.
        """
        start = max(0.0, moment - 10.0)
        end = min(duration, moment + 10.0)
        return {
            "start_sec": start,
            "end_sec": end,
            "duration": end - start
        }

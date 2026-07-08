class PlaybackService:
    @staticmethod
    def get_playback_details(violation_id: str) -> dict:
        return {
            "resolution": "1920x1080",
            "codec": "H.264",
            "frame_rate": 30.0,
            "bitrate_kbps": 4500
        }

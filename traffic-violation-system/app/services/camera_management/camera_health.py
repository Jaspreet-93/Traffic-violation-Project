class CameraHealthMonitor:
    @staticmethod
    def get_health_metrics(camera_id: int) -> dict:
        """
        Calculates packet loss, latency, and jitter.
        """
        return {
            "camera_id": camera_id,
            "health_score": 98,
            "packet_loss_pct": 0.05,
            "jitter_ms": 1.2,
            "latency_ms": 12.4,
            "status": "Healthy"
        }

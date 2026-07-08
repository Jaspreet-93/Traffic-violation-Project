from app.services.upload_detection.video_detector import results_registry

class ResultGenerator:
    @staticmethod
    def get_job_result(job_id: str) -> dict:
        """
        Compiles the job results dictionary if completed.
        """
        return results_registry.get(job_id)

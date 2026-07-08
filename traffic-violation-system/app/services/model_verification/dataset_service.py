class DatasetService:
    @staticmethod
    def get_dataset_summary() -> dict:
        return {
            "dataset_name": "Traffic Violation Infraction Dataset",
            "dataset_size_mb": 1420.5,
            "images_count": 8500,
            "videos_count": 420,
            "classes_count": 8,
            "annotations_count": 28400,
            "training_split": 0.70,
            "validation_split": 0.20,
            "test_split": 0.10
        }

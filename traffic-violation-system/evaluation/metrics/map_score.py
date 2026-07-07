def calculate_map(yolo_val_results) -> tuple:
    """
    Extracts mAP@50 and mAP@50-95 from YOLOv8 validation output result dict.
    Returns: (map50, map50_95)
    """
    if not yolo_val_results or not hasattr(yolo_val_results, "results_dict"):
        return 0.0, 0.0
    results_dict = yolo_val_results.results_dict
    map50 = float(results_dict.get("metrics/mAP50(B)", 0.0))
    map50_95 = float(results_dict.get("metrics/mAP50-95(B)", 0.0))
    return map50, map50_95

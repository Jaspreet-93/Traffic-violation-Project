import numpy as np

def calculate_precision_recall_f1(y_true, y_pred) -> tuple:
    """
    Calculates macro-averaged Precision, Recall, and F1-score for classification.
    Returns: (precision, recall, f1_score)
    """
    classes = set(y_true) | set(y_pred)
    if not classes or len(y_true) == 0:
        return 0.0, 0.0, 0.0
        
    precision_sum = 0.0
    recall_sum = 0.0
    f1_sum = 0.0
    
    for c in classes:
        tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == c and yp == c)
        fp = sum(1 for yt, yp in zip(y_true, y_pred) if yt != c and yp == c)
        fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == c and yp != c)
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
        
        precision_sum += precision
        recall_sum += recall
        f1_sum += f1
        
    n = len(classes)
    return float(precision_sum / n), float(recall_sum / n), float(f1_sum / n)

import numpy as np

def calculate_accuracy(y_true, y_pred) -> float:
    """
    Calculates classification accuracy.
    y_true: List or array of ground truth labels.
    y_pred: List or array of predicted labels.
    """
    if len(y_true) == 0:
        return 0.0
    correct = sum(1 for yt, yp in zip(y_true, y_pred) if yt == yp)
    return float(correct / len(y_true))

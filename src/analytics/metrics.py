"""
Evaluation metrics: IoU, Precision, Recall, F1-Score, Confusion Matrix, and Benchmark analytics.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple
import numpy as np


def compute_iou(mask_pred: np.ndarray, mask_gt: np.ndarray) -> float:
    """Computes Intersection-over-Union (Jaccard Index) between prediction and ground truth masks."""
    pred_bool = mask_pred > 0
    gt_bool = mask_gt > 0
    intersection = np.logical_and(pred_bool, gt_bool).sum()
    union = np.logical_or(pred_bool, gt_bool).sum()
    if union == 0:
        return 1.0 if intersection == 0 else 0.0
    return float(intersection) / float(union)


def calculate_classification_metrics(y_true: List[str], y_pred: List[str]) -> Dict[str, Any]:
    """
    Calculates Precision, Recall, F1-score, and per-class metrics.
    """
    labels = sorted(list(set(y_true + y_pred)))
    if not labels:
        return {"overall_accuracy": 1.0, "macro_f1": 1.0, "classes": {}}

    total = len(y_true)
    correct = sum(1 for yt, yp in zip(y_true, y_pred) if yt == yp)
    accuracy = correct / total if total > 0 else 0.0

    class_metrics = {}
    f1_scores = []

    for label in labels:
        tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == label and yp == label)
        fp = sum(1 for yt, yp in zip(y_true, y_pred) if yt != label and yp == label)
        fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == label and yp != label)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

        f1_scores.append(f1)
        class_metrics[label] = {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1, 4),
            "support": sum(1 for yt in y_true if yt == label)
        }

    macro_f1 = float(np.mean(f1_scores)) if f1_scores else 0.0

    return {
        "overall_accuracy": round(accuracy, 4),
        "macro_f1": round(macro_f1, 4),
        "total_samples": total,
        "classes": class_metrics
    }


@dataclass
class BenchmarkResult:
    """Latency and throughput performance profiling metrics."""
    total_images: int
    mean_latency_ms: float
    min_latency_ms: float
    max_latency_ms: float
    p95_latency_ms: float
    fps: float
    image_resolution: Tuple[int, int]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_images": self.total_images,
            "mean_latency_ms": round(self.mean_latency_ms, 2),
            "min_latency_ms": round(self.min_latency_ms, 2),
            "max_latency_ms": round(self.max_latency_ms, 2),
            "p95_latency_ms": round(self.p95_latency_ms, 2),
            "throughput_fps": round(self.fps, 2),
            "resolution": f"{self.image_resolution[1]}x{self.image_resolution[0]}"
        }

"""
Adaptive thresholding and morphological gradient operators for defect boundary detection.
"""
from typing import Tuple
import cv2
import numpy as np


def apply_otsu_threshold(gray_image: np.ndarray, invert: bool = True) -> Tuple[float, np.ndarray]:
    """
    Computes optimal binarization threshold via Otsu's intra-class variance minimization.
    """
    thresh_type = cv2.THRESH_BINARY_INV if invert else cv2.THRESH_BINARY
    threshold_val, binary = cv2.threshold(gray_image, 0, 255, thresh_type + cv2.THRESH_OTSU)
    return float(threshold_val), binary


def apply_statistical_threshold(residual: np.ndarray, sigma_multiplier: float = 3.2, min_thresh: float = 38.0) -> Tuple[float, np.ndarray]:
    """
    Applies adaptive statistical threshold based on mean and standard deviation of surface texture.
    Robustly rejects homogeneous background grain while isolating anomalous peaks.
    """
    mean_val = float(np.mean(residual))
    std_val = float(np.std(residual))
    thresh = max(min_thresh, mean_val + sigma_multiplier * std_val)
    _, binary = cv2.threshold(residual, int(thresh), 255, cv2.THRESH_BINARY)
    return thresh, binary


def apply_diffuse_anomaly_threshold(gray_image: np.ndarray, blur_k: int = 71, delta_thresh: int = 58) -> np.ndarray:
    """
    Detects low-frequency diffuse anomalies (stains, localized discoloration) by subtracting
    from a heavily smoothed background illumination estimation.
    """
    k = blur_k if blur_k % 2 != 0 else blur_k + 1
    bg = cv2.medianBlur(gray_image, k)
    diff_dark = cv2.subtract(bg, gray_image)
    _, binary = cv2.threshold(diff_dark, delta_thresh, 255, cv2.THRESH_BINARY)
    return binary


def apply_adaptive_threshold(
    gray_image: np.ndarray,
    block_size: int = 25,
    c: int = 5,
    invert: bool = True
) -> np.ndarray:
    """
    Local adaptive thresholding for non-uniform illumination fields.
    """
    b = block_size if block_size % 2 != 0 else block_size + 1
    thresh_type = cv2.THRESH_BINARY_INV if invert else cv2.THRESH_BINARY
    return cv2.adaptiveThreshold(
        gray_image,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresh_type,
        b,
        c
    )


def compute_morphological_gradient(gray_image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """
    Morphological gradient (Dilation - Erosion) highlights sharp structural edges
    regardless of local gradient polarity.
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    return cv2.morphologyEx(gray_image, cv2.MORPH_GRADIENT, kernel)

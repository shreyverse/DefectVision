"""
Spatial and edge-preserving filtering operations for surface defect inspection.
"""
import cv2
import numpy as np


def apply_gaussian_blur(image: np.ndarray, kernel_size: int = 5, sigma: float = 1.2) -> np.ndarray:
    """Applies Gaussian smoothing to suppress high-frequency random thermal/sensor noise."""
    k = kernel_size if kernel_size % 2 != 0 else kernel_size + 1
    return cv2.GaussianBlur(image, (k, k), sigmaX=sigma, sigmaY=sigma)


def apply_bilateral_filter(
    image: np.ndarray,
    d: int = 7,
    sigma_color: float = 75.0,
    sigma_space: float = 75.0
) -> np.ndarray:
    """
    Applies bilateral filtering for edge-preserving noise reduction.
    Smoothes homogeneous surface texture while preserving sharp defect edges (cracks/scratches).
    """
    return cv2.bilateralFilter(image, d=d, sigmaColor=sigma_color, sigmaSpace=sigma_space)


def apply_median_filter(image: np.ndarray, kernel_size: int = 3) -> np.ndarray:
    """Removes impulse and salt-and-pepper noise spikes."""
    k = kernel_size if kernel_size % 2 != 0 else kernel_size + 1
    return cv2.medianBlur(image, k)

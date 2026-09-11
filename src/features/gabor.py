"""
Multi-scale, multi-orientation Gabor filter bank for anisotropic defect detection.
"""
from typing import List, Tuple
import cv2
import numpy as np


def create_gabor_filter_bank(
    ksize: int = 15,
    sigma: float = 2.0,
    lambdas: List[float] = None,
    thetas_deg: List[float] = None,
    gamma: float = 0.5,
    psi: float = 0.0
) -> List[Tuple[float, float, np.ndarray]]:
    """
    Generates a bank of 2D Gabor kernels varying across wavelengths and orientations.
    Ideal for detecting directional scratches (at specific angles) and textured fissures.
    """
    if lambdas is None:
        lambdas = [4.0, 8.0]
    if thetas_deg is None:
        thetas_deg = [0.0, 45.0, 90.0, 135.0]

    filters = []
    for lmbd in lambdas:
        for th in thetas_deg:
            theta_rad = np.deg2rad(th)
            kernel = cv2.getGaborKernel(
                ksize=(ksize, ksize),
                sigma=sigma,
                theta=theta_rad,
                lambd=lmbd,
                gamma=gamma,
                psi=psi,
                ktype=cv2.CV_32F
            )
            filters.append((lmbd, th, kernel))
    return filters


def extract_gabor_features(
    image: np.ndarray,
    filters: List[Tuple[float, float, np.ndarray]] = None
) -> dict:
    """
    Filters image across the Gabor bank and extracts spatial energy magnitude maps.
    """
    if filters is None:
        filters = create_gabor_filter_bank()

    img_f = image.astype(np.float32)
    max_energy_map = np.zeros_like(img_f)
    responses = []

    for _, _, kernel in filters:
        filtered = cv2.filter2D(img_f, cv2.CV_32F, kernel)
        energy = np.abs(filtered)
        max_energy_map = np.maximum(max_energy_map, energy)
        responses.append(energy)

    mean_energy = float(np.mean(max_energy_map))
    variance_energy = float(np.var(max_energy_map))

    return {
        "gabor_mean_energy": mean_energy,
        "gabor_variance": variance_energy,
        "energy_map": max_energy_map
    }

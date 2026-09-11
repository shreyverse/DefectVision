"""
Gray-Level Co-occurrence Matrix (GLCM) statistical texture analysis.
"""
from typing import List
import numpy as np
from skimage.feature import graycomatrix, graycoprops


def extract_glcm_features(
    patch: np.ndarray,
    distances: List[int] = None,
    angles: List[float] = None
) -> dict:
    """
    Computes Haralick texture descriptors from the spatial Gray-Level Co-occurrence Matrix.
    Captures surface roughness, uniformity, correlation, and localized intensity variance.
    """
    if distances is None:
        distances = [1, 3]
    if angles is None:
        angles = [0.0, np.pi / 4, np.pi / 2, 3 * np.pi / 4]

    # Ensure 8-bit unsigned integer
    if patch.dtype != np.uint8:
        patch = (patch / np.max(patch) * 255).astype(np.uint8) if np.max(patch) > 0 else patch.astype(np.uint8)

    # Quantize to 32 gray levels for computational efficiency and robust co-occurrence
    quantized = (patch // 8).astype(np.uint8)

    # Compute GLCM
    glcm = graycomatrix(quantized, distances=distances, angles=angles, levels=32, symmetric=True, normed=True)

    contrast = float(np.mean(graycoprops(glcm, 'contrast')))
    dissimilarity = float(np.mean(graycoprops(glcm, 'dissimilarity')))
    homogeneity = float(np.mean(graycoprops(glcm, 'homogeneity')))
    energy = float(np.mean(graycoprops(glcm, 'energy')))
    correlation = float(np.mean(graycoprops(glcm, 'correlation')))

    return {
        "glcm_contrast": contrast,
        "glcm_dissimilarity": dissimilarity,
        "glcm_homogeneity": homogeneity,
        "glcm_energy": energy,
        "glcm_correlation": 0.0 if np.isnan(correlation) else correlation,
    }

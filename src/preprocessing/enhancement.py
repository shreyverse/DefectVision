"""
Contrast enhancement, illumination equalization, and morphological filtering.
"""
import cv2
import numpy as np


def to_grayscale(image: np.ndarray) -> np.ndarray:
    """Safely converts an RGB/BGR image to 8-bit single-channel grayscale."""
    if len(image.shape) == 2:
        return image
    if image.shape[2] == 4:
        return cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def apply_clahe(
    gray_image: np.ndarray,
    clip_limit: float = 2.5,
    tile_grid_size: tuple = (8, 8)
) -> np.ndarray:
    """
    Applies Contrast Limited Adaptive Histogram Equalization (CLAHE).
    Enhances local contrast while avoiding amplification of homogeneous background noise.
    """
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    return clahe.apply(gray_image)


def apply_morphological_tophat(gray_image: np.ndarray, kernel_size: int = 15) -> np.ndarray:
    """
    White Top-Hat transform: Extracts elements that are brighter than their surroundings.
    Useful for detecting metallic glints, bright scratches, and inclusions.
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    return cv2.morphologyEx(gray_image, cv2.MORPH_TOPHAT, kernel)


def apply_morphological_blackhat(gray_image: np.ndarray, kernel_size: int = 15) -> np.ndarray:
    """
    Black Top-Hat transform: Extracts elements that are darker than their surroundings.
    Specifically isolates dark surface cracks, fissures, and deep pits.
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    return cv2.morphologyEx(gray_image, cv2.MORPH_BLACKHAT, kernel)


def enhance_surface_features(
    image: np.ndarray,
    clahe_clip: float = 2.5,
    tophat_k: int = 15
) -> dict:
    """
    Complete enhancement pipeline returning enhanced grayscale, contrast-boosted,
    and morphological residual representations.
    """
    gray = to_grayscale(image)
    clahe_img = apply_clahe(gray, clip_limit=clahe_clip)
    tophat = apply_morphological_tophat(gray, kernel_size=tophat_k)
    blackhat = apply_morphological_blackhat(gray, kernel_size=tophat_k)
    # Combine bright and dark defect residuals
    morph_diff = cv2.add(tophat, blackhat)
    
    return {
        "gray": gray,
        "enhanced": clahe_img,
        "tophat": tophat,
        "blackhat": blackhat,
        "morph_residual": morph_diff
    }

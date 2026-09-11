"""
Marker-controlled watershed segmentation and defect contour extraction.
Preserves thin scratches and crack boundaries while separating clustered defect aggregates.
"""
from typing import List, Tuple
import cv2
import numpy as np


def segment_defects_watershed(
    binary_mask: np.ndarray,
    distance_ratio: float = 0.4
) -> Tuple[np.ndarray, List[np.ndarray]]:
    """
    Applies selective morphological cleanup and watershed segmentation.
    Preserves thin line defects (cracks, scratches) while separating dense aggregates.
    """
    # Use 2x2 elliptical kernel for opening to avoid eroding thin 1-pixel scratch lines
    kernel_small = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    cleaned = cv2.morphologyEx(binary_mask, cv2.MORPH_OPEN, kernel_small)

    # Initial contour check
    contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if any large blob requires watershed decomposition
    has_large_blob = any(cv2.contourArea(c) > 600 for c in contours)
    if not has_large_blob or len(contours) == 0:
        return cleaned, list(contours)

    # Apply distance transform and marker-controlled watershed
    dist_transform = cv2.distanceTransform(cleaned, cv2.DIST_L2, 5)
    max_dist = dist_transform.max()
    if max_dist > 3.0:
        _, sure_fg = cv2.threshold(dist_transform, distance_ratio * max_dist, 255, 0)
        sure_fg = np.uint8(sure_fg)
        kernel_3 = np.ones((3, 3), np.uint8)
        sure_bg = cv2.dilate(cleaned, kernel_3, iterations=2)
        unknown = cv2.subtract(sure_bg, sure_fg)

        _, markers = cv2.connectedComponents(sure_fg)
        markers = markers + 1
        markers[unknown == 255] = 0

        pseudo_color = cv2.cvtColor(cleaned, cv2.COLOR_GRAY2BGR)
        markers = cv2.watershed(pseudo_color, markers)

        defect_mask = np.zeros_like(cleaned)
        defect_mask[markers > 1] = 255
        # Re-include thin components that may have been lost in distance thresholding
        defect_mask = cv2.bitwise_or(defect_mask, cleaned)
        out_contours, _ = cv2.findContours(defect_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return defect_mask, list(out_contours)

    return cleaned, list(contours)


def extract_candidate_contours(
    binary_mask: np.ndarray,
    min_area: int = 20,
    max_area: int = 500000
) -> List[np.ndarray]:
    """
    Filters defect contours by area constraints to eliminate single-pixel noise
    and whole-frame segmentation artifacts.
    """
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    valid_contours = []
    for c in contours:
        area = cv2.contourArea(c)
        if min_area <= area <= max_area:
            valid_contours.append(c)
    return valid_contours

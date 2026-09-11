"""
Geometric, morphology, and invariant moments descriptors for defect contours.
"""
from typing import List, Tuple, Optional
import cv2
import numpy as np
from ..core.types import GeometricFeatures


def extract_geometric_features(
    contour: np.ndarray,
    gray_image: Optional[np.ndarray] = None
) -> GeometricFeatures:
    """
    Extracts geometric properties, radiometric intensity, and scale/rotation invariant Hu moments.
    """
    area = float(cv2.contourArea(contour))
    perimeter = float(cv2.arcLength(contour, closed=True))

    # Circularity (Isoperimetric quotient: 4 * pi * area / perimeter^2)
    circularity = (4.0 * np.pi * area) / (perimeter ** 2) if perimeter > 0 else 0.0
    circularity = min(max(circularity, 0.0), 1.0)

    # Bounding box & Aspect Ratio
    x, y, w, h = cv2.boundingRect(contour)
    aspect_ratio = float(max(w, h)) / float(max(min(w, h), 1))

    # Extent
    rect_area = float(w * h)
    extent = area / rect_area if rect_area > 0 else 0.0

    # Solidity
    hull = cv2.convexHull(contour)
    hull_area = float(cv2.contourArea(hull))
    solidity = area / hull_area if hull_area > 0 else 0.0

    # Equivalent diameter
    equivalent_diameter = float(np.sqrt(4.0 * area / np.pi))

    # Radiometric intensity within contour mask
    mean_intensity = 0.0
    min_intensity = 0.0
    if gray_image is not None and area > 0:
        c_mask = np.zeros(gray_image.shape, dtype=np.uint8)
        cv2.drawContours(c_mask, [contour], -1, 255, -1)
        pixels = gray_image[c_mask == 255]
        if len(pixels) > 0:
            mean_intensity = float(np.mean(pixels))
            min_intensity = float(np.min(pixels))

    # Hu Moments (Log-transformed invariants)
    moments = cv2.moments(contour)
    raw_hu = cv2.HuMoments(moments)
    hu_list: List[float] = []
    for h_val in raw_hu:
        val = float(h_val[0])
        log_hu = -1.0 * np.sign(val) * np.log10(abs(val)) if abs(val) > 1e-12 else 0.0
        hu_list.append(float(log_hu))

    return GeometricFeatures(
        area=area,
        perimeter=perimeter,
        circularity=circularity,
        aspect_ratio=aspect_ratio,
        solidity=solidity,
        extent=extent,
        equivalent_diameter=equivalent_diameter,
        mean_intensity=mean_intensity,
        min_intensity=min_intensity,
        hu_moments=hu_list
    )

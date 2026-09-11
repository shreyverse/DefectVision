"""
Multi-class defect classification and industrial severity assessment.
Combines geometric morphology, radiometric intensity, and texture features.
"""
from typing import Tuple, Dict, Any, Optional
import numpy as np
from ..core.types import (
    DefectClass,
    DefectSeverity,
    GeometricFeatures,
    TextureFeatures,
    DefectRegion
)


def assess_severity(defect_type: DefectClass, area: float, aspect_ratio: float) -> DefectSeverity:
    """
    Determines defect severity according to industrial tolerance criteria.
    Cracks have higher structural hazard weighting than stains or pinholes.
    """
    if defect_type == DefectClass.CRACK:
        if area > 1000 or aspect_ratio > 4.0:
            return DefectSeverity.CRITICAL
        elif area > 250:
            return DefectSeverity.MODERATE
        return DefectSeverity.MINOR

    elif defect_type == DefectClass.SCRATCH:
        if area > 2000 or aspect_ratio > 5.0:
            return DefectSeverity.CRITICAL
        elif area > 500:
            return DefectSeverity.MODERATE
        return DefectSeverity.MINOR

    elif defect_type == DefectClass.PINHOLE:
        if area > 800:
            return DefectSeverity.MODERATE
        elif area > 80:
            return DefectSeverity.MINOR
        return DefectSeverity.NEGLIGIBLE

    elif defect_type == DefectClass.STAIN:
        if area > 4000:
            return DefectSeverity.MODERATE
        return DefectSeverity.MINOR

    return DefectSeverity.NEGLIGIBLE


def classify_defect_region(
    geometry: GeometricFeatures,
    texture: Optional[TextureFeatures] = None
) -> Tuple[DefectClass, float, DefectSeverity]:
    """
    Rule-based & statistical feature decision engine.
    Distinguishes PINHOLE, SCRATCH, CRACK, and STAIN.
    """
    circ = geometry.circularity
    ar = geometry.aspect_ratio
    area = geometry.area
    solidity = geometry.solidity
    extent = geometry.extent
    min_i = geometry.min_intensity

    # 1. Pinhole: Small compact void with deep dark core (min intensity < 50)
    if circ >= 0.50 and ar < 2.2 and area < 1000 and (min_i < 50 or min_i == 0):
        conf = min(0.78 + 0.20 * circ, 0.99)
        sev = assess_severity(DefectClass.PINHOLE, area, ar)
        return DefectClass.PINHOLE, conf, sev

    # 2. Scratch: High aspect ratio, thin elongated line, very low circularity
    if ar >= 2.5 and (circ < 0.35 or extent < 0.40):
        gabor_boost = 0.05 if (texture and texture.gabor_mean_energy > 12.0) else 0.0
        conf = min(0.80 + min(ar / 12.0, 0.18) + gabor_boost, 0.98)
        sev = assess_severity(DefectClass.SCRATCH, area, ar)
        return DefectClass.SCRATCH, conf, sev

    # 3. Crack: Branching or tortuous path, low circularity, lower solidity or low extent
    if circ < 0.45 and (solidity < 0.75 or extent < 0.48 or area > 400):
        conf = min(0.75 + (1.0 - circ) * 0.22, 0.97)
        sev = assess_severity(DefectClass.CRACK, area, ar)
        return DefectClass.CRACK, conf, sev

    # 4. Stain: Diffuse region with moderate-to-high solidity and lighter minimum intensity
    if min_i >= 50 or area >= 200:
        conf = 0.85
        sev = assess_severity(DefectClass.STAIN, area, ar)
        return DefectClass.STAIN, conf, sev

    # Default fallback
    if ar > 1.8:
        return DefectClass.SCRATCH, 0.65, assess_severity(DefectClass.SCRATCH, area, ar)
    else:
        return DefectClass.STAIN, 0.62, assess_severity(DefectClass.STAIN, area, ar)


class DefectClassifier:
    """Wrapper class providing classification and batch decision support."""

    def __init__(self, confidence_threshold: float = 0.60):
        self.confidence_threshold = confidence_threshold

    def predict(
        self,
        geometry: GeometricFeatures,
        texture: Optional[TextureFeatures] = None
    ) -> Tuple[DefectClass, float, DefectSeverity]:
        return classify_defect_region(geometry, texture)

"""
Annotation overlay, bounding-box graphics, severity badges, and comparison panels.
"""
from typing import List, Optional
import os
import cv2
import numpy as np
from ..core.types import DefectClass, DefectSeverity, InspectionResult


CLASS_COLORS = {
    DefectClass.CRACK: (0, 0, 230),       # High-visibility Red
    DefectClass.SCRATCH: (0, 140, 255),   # Industrial Orange
    DefectClass.STAIN: (200, 30, 180),     # Magenta / Purple
    DefectClass.PINHOLE: (0, 220, 255),   # Yellow
    DefectClass.DEFECT_FREE: (60, 200, 60) # Emerald Green
}


def render_inspection_overlay(
    image: np.ndarray,
    result: InspectionResult,
    draw_contours: bool = True
) -> np.ndarray:
    """
    Renders bounding boxes, severity banners, and geometric indicators on the input image.
    """
    annotated = image.copy()
    if len(annotated.shape) == 2:
        annotated = cv2.cvtColor(annotated, cv2.COLOR_GRAY2BGR)

    h, w = annotated.shape[:2]

    # Top Status Bar
    header_color = (40, 40, 40)
    cv2.rectangle(annotated, (0, 0), (w, 42), header_color, -1)
    
    status_text = "STATUS: DEFECTIVE" if result.is_defective else "STATUS: DEFECT-FREE (PASS)"
    status_color = (0, 0, 240) if result.is_defective else (0, 220, 0)
    cv2.putText(annotated, status_text, (15, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.75, status_color, 2)
    
    info_str = f"Defects: {result.total_defects} | Max Severity: {result.max_severity.value} | Time: {result.execution_time_ms:.1f}ms"
    cv2.putText(annotated, info_str, (320, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (220, 220, 220), 1)

    for r in result.regions:
        x, y, rw, rh = r.bbox
        color = CLASS_COLORS.get(r.defect_type, (0, 255, 255))

        # Bounding box
        cv2.rectangle(annotated, (x, y), (x + rw, y + rh), color, 2)

        # Label tag
        tag = f"#{r.region_id} {r.defect_type.value} [{r.confidence:.2f}]"
        (tw, th), _ = cv2.getTextSize(tag, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
        tag_y1 = max(0, y - th - 6)
        cv2.rectangle(annotated, (x, tag_y1), (x + tw + 6, y), color, -1)
        cv2.putText(annotated, tag, (x + 3, y - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

        # Dimension annotation
        dim_str = f"{rw}x{rh}px ({r.severity.value})"
        cv2.putText(annotated, dim_str, (x, y + rh + 14), cv2.FONT_HERSHEY_SIMPLEX, 0.38, color, 1)

    return annotated


def render_comparison_quad(
    original: np.ndarray,
    enhanced: np.ndarray,
    defect_mask: np.ndarray,
    annotated: np.ndarray
) -> np.ndarray:
    """
    Builds a 2x2 multi-panel diagnostic dashboard:
    [Original]     [CLAHE/Enhanced]
    [Defect Mask]  [Final Inspection Result]
    """
    def ensure_bgr(im):
        if len(im.shape) == 2:
            return cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
        return im

    orig_bgr = ensure_bgr(original)
    enh_bgr = ensure_bgr(enhanced)
    mask_bgr = ensure_bgr(defect_mask)
    res_bgr = ensure_bgr(annotated)

    # Standardize height and width
    h, w = orig_bgr.shape[:2]
    enh_bgr = cv2.resize(enh_bgr, (w, h))
    mask_bgr = cv2.resize(mask_bgr, (w, h))
    res_bgr = cv2.resize(res_bgr, (w, h))

    # Add panel headers
    for img, title in [
        (orig_bgr, "1. Raw Surface Input"),
        (enh_bgr, "2. CLAHE & Morphological Residual"),
        (mask_bgr, "3. Binarized Defect Segmentation Mask"),
        (res_bgr, "4. Multi-Defect Detection & Sizing")
    ]:
        cv2.rectangle(img, (0, 0), (w, 30), (30, 30, 30), -1)
        cv2.putText(img, title, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)

    top_row = np.hstack([orig_bgr, enh_bgr])
    bottom_row = np.hstack([mask_bgr, res_bgr])
    quad = np.vstack([top_row, bottom_row])
    return quad


def save_visualization(image: np.ndarray, output_path: str) -> None:
    """Safely saves annotated visual frame to output directory."""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    cv2.imwrite(output_path, image)

"""
SurfaceVision Master Inspection Pipeline.
Integrates preprocessing, feature extraction, segmentation, classification, and diagnostics.
"""
import os
import time
from datetime import datetime
from typing import List, Union, Optional, Tuple
import cv2
import numpy as np

from .core.types import (
    DefectClass,
    DefectSeverity,
    DefectRegion,
    InspectionResult
)
from .core.config import InspectionConfig, get_default_config
from .preprocessing.filter import apply_bilateral_filter
from .preprocessing.enhancement import to_grayscale, apply_clahe, enhance_surface_features
from .segmentation.threshold import apply_statistical_threshold, apply_diffuse_anomaly_threshold
from .segmentation.watershed import segment_defects_watershed, extract_candidate_contours
from .features.geometry import extract_geometric_features
from .features.glcm import extract_glcm_features
from .features.gabor import extract_gabor_features
from .classifier.defect_classifier import DefectClassifier, classify_defect_region
from .analytics.visualizer import render_inspection_overlay, render_comparison_quad, save_visualization


class SurfaceVisionPipeline:
    """
    End-to-End Automated Industrial Surface Defect Inspection Pipeline.
    """

    def __init__(self, config: Optional[InspectionConfig] = None):
        self.config = config or get_default_config()
        self.classifier = DefectClassifier(self.config.confidence_threshold)

    def load_image(self, input_source: Union[str, np.ndarray]) -> np.ndarray:
        """Loads and verifies an image from filepath or numpy array."""
        if isinstance(input_source, str):
            if not os.path.exists(input_source):
                raise FileNotFoundError(f"Input image path does not exist: {input_source}")
            img = cv2.imread(input_source)
            if img is None:
                raise ValueError(f"Could not decode image at: {input_source}")
            return img
        elif isinstance(input_source, np.ndarray):
            return input_source
        else:
            raise TypeError("input_source must be a file path string or numpy ndarray")

    def process(
        self,
        image_input: Union[str, np.ndarray],
        extract_texture: bool = True
    ) -> Tuple[InspectionResult, dict]:
        """
        Executes the full inspection workflow on a single image.
        Returns (InspectionResult, intermediate_artifacts_dict).
        """
        start_time = time.perf_counter()
        raw_bgr = self.load_image(image_input)
        img_path = image_input if isinstance(image_input, str) else "in_memory_array"
        h, w = raw_bgr.shape[:2]

        # 1. Preprocessing & Edge-Preserving Enhancement
        gray = to_grayscale(raw_bgr)
        denoised = apply_bilateral_filter(
            gray,
            d=self.config.preprocessing.bilateral_d,
            sigma_color=self.config.preprocessing.bilateral_sigma_color,
            sigma_space=self.config.preprocessing.bilateral_sigma_space
        )
        enhancement_pack = enhance_surface_features(
            denoised,
            clahe_clip=self.config.preprocessing.clahe_clip_limit,
            tophat_k=self.config.preprocessing.tophat_kernel_size
        )
        enhanced_gray = enhancement_pack["enhanced"]
        morph_residual = enhancement_pack["morph_residual"]

        # 2. Defect Segmentation
        # A. High-frequency structural defects (cracks, scratches, pinholes)
        _, binary_struct = apply_statistical_threshold(morph_residual, sigma_multiplier=3.2, min_thresh=38.0)
        # B. Low-frequency diffuse defects (stains, surface burns)
        binary_stain = apply_diffuse_anomaly_threshold(denoised, blur_k=71, delta_thresh=55)

        combined_binary = cv2.bitwise_or(binary_struct, binary_stain)

        # Apply marker-controlled watershed segmentation
        cleaned_mask, watershed_contours = segment_defects_watershed(
            combined_binary,
            distance_ratio=self.config.segmentation.watershed_distance_ratio
        )

        # Filter contours by area constraints
        valid_contours = extract_candidate_contours(
            cleaned_mask,
            min_area=self.config.segmentation.min_defect_area,
            max_area=self.config.segmentation.max_defect_area
        )

        # 3. Feature Extraction & Classification
        detected_regions: List[DefectRegion] = []
        defect_counts = {c.value: 0 for c in DefectClass if c != DefectClass.DEFECT_FREE}
        max_severity = DefectSeverity.NEGLIGIBLE
        severity_rank = {
            DefectSeverity.NEGLIGIBLE: 0,
            DefectSeverity.MINOR: 1,
            DefectSeverity.MODERATE: 2,
            DefectSeverity.CRITICAL: 3
        }

        for idx, cnt in enumerate(valid_contours, start=1):
            geom = extract_geometric_features(cnt, gray_image=gray)
            x, y, rw, rh = cv2.boundingRect(cnt)

            # Centroid calculation
            M = cv2.moments(cnt)
            cx = int(M["m10"] / M["m00"]) if M["m00"] != 0 else x + rw // 2
            cy = int(M["m01"] / M["m00"]) if M["m00"] != 0 else y + rh // 2

            # Extract localized texture if requested
            tex_features = None
            if extract_texture:
                patch = gray[max(0, y - 5):min(h, y + rh + 5), max(0, x - 5):min(w, x + rw + 5)]
                if patch.size > 20:
                    tex_dict = extract_glcm_features(patch)
                    gabor_dict = extract_gabor_features(patch)
                    from .core.types import TextureFeatures
                    tex_features = TextureFeatures(
                        glcm_contrast=tex_dict["glcm_contrast"],
                        glcm_dissimilarity=tex_dict["glcm_dissimilarity"],
                        glcm_homogeneity=tex_dict["glcm_homogeneity"],
                        glcm_energy=tex_dict["glcm_energy"],
                        glcm_correlation=tex_dict["glcm_correlation"],
                        gabor_mean_energy=gabor_dict["gabor_mean_energy"],
                        gabor_variance=gabor_dict["gabor_variance"]
                    )

            defect_type, conf, sev = self.classifier.predict(geom, tex_features)

            if conf >= self.config.confidence_threshold:
                defect_counts[defect_type.value] += 1
                if severity_rank[sev] > severity_rank[max_severity]:
                    max_severity = sev

                region = DefectRegion(
                    region_id=idx,
                    bbox=(x, y, rw, rh),
                    centroid=(cx, cy),
                    defect_type=defect_type,
                    confidence=conf,
                    severity=sev,
                    geometry=geom,
                    texture=tex_features
                )
                detected_regions.append(region)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        total_defects = len(detected_regions)
        is_defective = total_defects > 0

        # Construct final inspection result
        result = InspectionResult(
            image_path=img_path,
            dimensions=(h, w),
            timestamp=datetime.now().isoformat(),
            regions=detected_regions,
            total_defects=total_defects,
            is_defective=is_defective,
            max_severity=max_severity if is_defective else DefectSeverity.NEGLIGIBLE,
            execution_time_ms=elapsed_ms,
            defect_summary={k: v for k, v in defect_counts.items() if v > 0}
        )

        artifacts = {
            "raw": raw_bgr,
            "gray": gray,
            "enhanced": enhanced_gray,
            "morph_residual": morph_residual,
            "defect_mask": cleaned_mask
        }

        return result, artifacts

    def inspect_and_visualize(
        self,
        image_input: Union[str, np.ndarray],
        output_dir: Optional[str] = None,
        save_quad: bool = True
    ) -> Tuple[InspectionResult, np.ndarray, np.ndarray]:
        """
        Runs inspection and generates overlay & 2x2 comparison dashboard.
        """
        result, artifacts = self.process(image_input)
        overlay = render_inspection_overlay(artifacts["raw"], result)
        quad = render_comparison_quad(
            artifacts["raw"],
            artifacts["enhanced"],
            artifacts["defect_mask"],
            overlay
        )

        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            base_name = os.path.splitext(os.path.basename(result.image_path))[0] if os.path.isabs(result.image_path) else "inspection"
            save_visualization(overlay, os.path.join(output_dir, f"{base_name}_annotated.png"))
            if save_quad:
                save_visualization(quad, os.path.join(output_dir, f"{base_name}_quad.png"))

        return result, overlay, quad

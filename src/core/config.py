"""
Configuration management for SurfaceVision pipeline.
"""
from dataclasses import dataclass, field
from typing import Tuple, List, Dict, Any
import json
import os


@dataclass
class PreprocessingConfig:
    """Parameters for noise suppression and contrast enhancement."""
    gaussian_kernel_size: int = 5
    gaussian_sigma: float = 1.2
    bilateral_d: int = 7
    bilateral_sigma_color: float = 75.0
    bilateral_sigma_space: float = 75.0
    clahe_clip_limit: float = 2.5
    clahe_tile_grid_size: Tuple[int, int] = (8, 8)
    morph_kernel_size: int = 3
    tophat_kernel_size: int = 15


@dataclass
class FeatureConfig:
    """Parameters for GLCM and Gabor feature extraction."""
    glcm_distances: List[int] = field(default_factory=lambda: [1, 3, 5])
    glcm_angles: List[float] = field(default_factory=lambda: [0.0, 0.785398, 1.570796, 2.356194]) # 0, 45, 90, 135 deg in rad
    gabor_frequencies: List[float] = field(default_factory=lambda: [0.1, 0.25])
    gabor_thetas: List[float] = field(default_factory=lambda: [0.0, 45.0, 90.0, 135.0])
    gabor_sigma_x: float = 2.0
    gabor_sigma_y: float = 2.0


@dataclass
class SegmentationConfig:
    """Parameters for thresholding and watershed segmentation."""
    min_defect_area: int = 25       # reject smaller noise speckles
    max_defect_area: int = 500000   # reject massive full-image illumination artifacts
    adaptive_block_size: int = 25
    adaptive_c: int = 5
    canny_low_thresh: int = 50
    canny_high_thresh: int = 150
    watershed_distance_ratio: float = 0.4


@dataclass
class InspectionConfig:
    """Master configuration container for SurfaceVision."""
    preprocessing: PreprocessingConfig = field(default_factory=PreprocessingConfig)
    features: FeatureConfig = field(default_factory=FeatureConfig)
    segmentation: SegmentationConfig = field(default_factory=SegmentationConfig)
    confidence_threshold: float = 0.60
    output_dir: str = "output"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "preprocessing": self.preprocessing.__dict__,
            "features": self.features.__dict__,
            "segmentation": self.segmentation.__dict__,
            "confidence_threshold": self.confidence_threshold,
            "output_dir": self.output_dir
        }

    def save_json(self, file_path: str) -> None:
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)


def get_default_config() -> InspectionConfig:
    """Factory for standard industrial inspection config."""
    return InspectionConfig()

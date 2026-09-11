"""
Core types and data structures for the SurfaceVision inspection system.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Tuple, Dict, Any, Optional


class DefectClass(str, Enum):
    """Supported industrial surface defect classifications."""
    CRACK = "CRACK"
    SCRATCH = "SCRATCH"
    STAIN = "STAIN"
    PINHOLE = "PINHOLE"
    DEFECT_FREE = "DEFECT_FREE"


class DefectSeverity(str, Enum):
    """Defect severity ranking based on geometric area and structural impact."""
    NEGLIGIBLE = "NEGLIGIBLE"
    MINOR = "MINOR"
    MODERATE = "MODERATE"
    CRITICAL = "CRITICAL"


@dataclass
class GeometricFeatures:
    """Geometric, radiometric, and morphology descriptors for a detected defect contour."""
    area: float
    perimeter: float
    circularity: float
    aspect_ratio: float
    solidity: float
    extent: float
    equivalent_diameter: float
    mean_intensity: float = 0.0
    min_intensity: float = 0.0
    hu_moments: List[float] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "area": round(float(self.area), 2),
            "perimeter": round(float(self.perimeter), 2),
            "circularity": round(float(self.circularity), 4),
            "aspect_ratio": round(float(self.aspect_ratio), 4),
            "solidity": round(float(self.solidity), 4),
            "extent": round(float(self.extent), 4),
            "equivalent_diameter": round(float(self.equivalent_diameter), 2),
            "mean_intensity": round(float(self.mean_intensity), 2),
            "min_intensity": round(float(self.min_intensity), 2),
            "hu_moments": [round(float(h), 6) for h in self.hu_moments]
        }


@dataclass
class TextureFeatures:
    """Texture and frequency energy descriptors."""
    glcm_contrast: float
    glcm_dissimilarity: float
    glcm_homogeneity: float
    glcm_energy: float
    glcm_correlation: float
    gabor_mean_energy: float
    gabor_variance: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "glcm_contrast": round(float(self.glcm_contrast), 4),
            "glcm_dissimilarity": round(float(self.glcm_dissimilarity), 4),
            "glcm_homogeneity": round(float(self.glcm_homogeneity), 4),
            "glcm_energy": round(float(self.glcm_energy), 4),
            "glcm_correlation": round(float(self.glcm_correlation), 4),
            "gabor_mean_energy": round(float(self.gabor_mean_energy), 4),
            "gabor_variance": round(float(self.gabor_variance), 4)
        }


@dataclass
class DefectRegion:
    """Single detected defect candidate with spatial, shape, and class information."""
    region_id: int
    bbox: Tuple[int, int, int, int]  # (x, y, width, height)
    centroid: Tuple[int, int]         # (cx, cy)
    defect_type: DefectClass
    confidence: float
    severity: DefectSeverity
    geometry: GeometricFeatures
    texture: Optional[TextureFeatures] = None
    contour_points: Optional[List[List[int]]] = None

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "region_id": self.region_id,
            "bbox": list(self.bbox),
            "centroid": list(self.centroid),
            "defect_type": self.defect_type.value,
            "confidence": round(float(self.confidence), 4),
            "severity": self.severity.value,
            "geometry": self.geometry.to_dict(),
        }
        if self.texture:
            data["texture"] = self.texture.to_dict()
        return data


@dataclass
class InspectionResult:
    """Complete visual inspection output for an industrial surface image."""
    image_path: str
    dimensions: Tuple[int, int]  # (height, width)
    timestamp: str
    regions: List[DefectRegion] = field(default_factory=list)
    total_defects: int = 0
    is_defective: bool = False
    max_severity: DefectSeverity = DefectSeverity.NEGLIGIBLE
    execution_time_ms: float = 0.0
    defect_summary: Dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "image_path": self.image_path,
            "dimensions": {"height": self.dimensions[0], "width": self.dimensions[1]},
            "timestamp": self.timestamp,
            "total_defects": self.total_defects,
            "is_defective": self.is_defective,
            "max_severity": self.max_severity.value,
            "execution_time_ms": round(float(self.execution_time_ms), 2),
            "defect_summary": self.defect_summary,
            "regions": [r.to_dict() for r in self.regions]
        }

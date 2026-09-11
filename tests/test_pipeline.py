"""Tests for end-to-end SurfaceVision pipeline."""
import unittest
import numpy as np
import cv2
from src.pipeline import SurfaceVisionPipeline
from src.core.types import DefectClass


class TestPipeline(unittest.TestCase):

    def setUp(self):
        self.pipeline = SurfaceVisionPipeline()

    def test_clean_surface_inspection(self):
        # Uniform metallic surface
        clean_img = np.full((200, 200, 3), 180, dtype=np.uint8)
        result, _ = self.pipeline.process(clean_img)
        self.assertFalse(result.is_defective)
        self.assertEqual(result.total_defects, 0)

    def test_scratch_defect_inspection(self):
        # Surface with a sharp scratch
        img = np.full((200, 200, 3), 180, dtype=np.uint8)
        cv2.line(img, (20, 100), (180, 100), (20, 20, 20), 2) # Dark line
        result, artifacts = self.pipeline.process(img)
        self.assertTrue(result.is_defective)
        self.assertGreaterEqual(result.total_defects, 1)
        self.assertIn("raw", artifacts)
        self.assertIn("defect_mask", artifacts)

    def test_inspect_and_visualize(self):
        img = np.full((200, 200, 3), 180, dtype=np.uint8)
        cv2.circle(img, (100, 100), 10, (20, 20, 20), -1)
        res, overlay, quad = self.pipeline.inspect_and_visualize(img)
        self.assertEqual(overlay.shape, (200, 200, 3))
        self.assertEqual(quad.shape, (400, 400, 3))


if __name__ == "__main__":
    unittest.main()

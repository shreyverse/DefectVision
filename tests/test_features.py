"""Tests for feature extraction modules."""
import unittest
import numpy as np
import cv2
from src.features.geometry import extract_geometric_features
from src.features.glcm import extract_glcm_features
from src.features.gabor import create_gabor_filter_bank, extract_gabor_features


class TestFeatures(unittest.TestCase):

    def test_extract_geometric_features_circle(self):
        # Draw a synthetic circle
        canvas = np.zeros((120, 120), dtype=np.uint8)
        cv2.circle(canvas, (60, 60), 30, 255, -1)
        cnts, _ = cv2.findContours(canvas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.assertEqual(len(cnts), 1)

        geom = extract_geometric_features(cnts[0], gray_image=canvas)
        # Circularity of a circle should be close to 1.0
        self.assertGreater(geom.circularity, 0.85)
        # Aspect ratio of a circle should be close to 1.0
        self.assertAlmostEqual(geom.aspect_ratio, 1.0, delta=0.2)
        self.assertGreater(geom.solidity, 0.90)
        self.assertEqual(len(geom.hu_moments), 7)

    def test_extract_geometric_features_line(self):
        # Draw an elongated horizontal line
        canvas = np.zeros((120, 120), dtype=np.uint8)
        cv2.line(canvas, (20, 60), (100, 60), 255, 3)
        cnts, _ = cv2.findContours(canvas, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        geom = extract_geometric_features(cnts[0], gray_image=canvas)
        # Aspect ratio should be large
        self.assertGreater(geom.aspect_ratio, 3.0)
        # Circularity should be small
        self.assertLess(geom.circularity, 0.35)

    def test_extract_glcm_features(self):
        patch = np.random.randint(50, 200, (40, 40), dtype=np.uint8)
        glcm_res = extract_glcm_features(patch)
        self.assertIn("glcm_contrast", glcm_res)
        self.assertIn("glcm_homogeneity", glcm_res)
        self.assertIn("glcm_energy", glcm_res)

    def test_extract_gabor_features(self):
        img = np.random.randint(50, 200, (64, 64), dtype=np.uint8)
        filters = create_gabor_filter_bank(ksize=11, lambdas=[4.0], thetas_deg=[0.0, 90.0])
        self.assertEqual(len(filters), 2)
        gabor_res = extract_gabor_features(img, filters)
        self.assertIn("gabor_mean_energy", gabor_res)
        self.assertIn("energy_map", gabor_res)
        self.assertEqual(gabor_res["energy_map"].shape, (64, 64))


if __name__ == "__main__":
    unittest.main()

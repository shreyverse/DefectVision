"""Tests for segmentation and thresholding modules."""
import unittest
import numpy as np
import cv2
from src.segmentation.threshold import apply_otsu_threshold, apply_statistical_threshold, apply_diffuse_anomaly_threshold
from src.segmentation.watershed import segment_defects_watershed, extract_candidate_contours


class TestSegmentation(unittest.TestCase):

    def setUp(self):
        self.canvas = np.zeros((150, 150), dtype=np.uint8)
        # Add two discrete defect spots
        cv2.circle(self.canvas, (40, 40), 12, 255, -1)
        cv2.circle(self.canvas, (110, 110), 15, 255, -1)

    def test_otsu_threshold(self):
        # Bimodal test image (half 50, half 200)
        bimodal = np.full((100, 100), 50, dtype=np.uint8)
        bimodal[50:, :] = 200
        val, binary = apply_otsu_threshold(bimodal, invert=False)
        self.assertGreaterEqual(val, 50)
        self.assertLess(val, 200)
        self.assertEqual(binary[75, 50], 255)
        self.assertEqual(binary[25, 50], 0)

    def test_statistical_threshold(self):
        res = np.full((100, 100), 10, dtype=np.uint8)
        res[50:60, 50:60] = 120 # Anomaly
        val, b = apply_statistical_threshold(res, sigma_multiplier=3.0)
        self.assertGreater(val, 20)
        self.assertEqual(b[55, 55], 255)
        self.assertEqual(b[0, 0], 0)

    def test_watershed_segmentation(self):
        cleaned, contours = segment_defects_watershed(self.canvas)
        self.assertEqual(len(contours), 2)

    def test_extract_candidate_contours(self):
        contours = extract_candidate_contours(self.canvas, min_area=30)
        self.assertEqual(len(contours), 2)


if __name__ == "__main__":
    unittest.main()

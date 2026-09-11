"""Tests for preprocessing and enhancement modules."""
import unittest
import numpy as np
from src.preprocessing.filter import apply_gaussian_blur, apply_bilateral_filter, apply_median_filter
from src.preprocessing.enhancement import to_grayscale, apply_clahe, apply_morphological_tophat, apply_morphological_blackhat, enhance_surface_features


class TestPreprocessing(unittest.TestCase):

    def setUp(self):
        # 100x100 synthetic test image with background 120
        self.img_gray = np.full((100, 100), 120, dtype=np.uint8)
        # Small 6x6 bright spot (smaller than 15x15 kernel for top-hat)
        self.img_gray[47:53, 47:53] = 230
        self.img_bgr = np.repeat(self.img_gray[:, :, None], 3, axis=2)

    def test_to_grayscale(self):
        gray = to_grayscale(self.img_bgr)
        self.assertEqual(len(gray.shape), 2)
        self.assertEqual(gray.shape, (100, 100))

    def test_apply_gaussian_blur(self):
        blurred = apply_gaussian_blur(self.img_gray, kernel_size=5, sigma=1.0)
        self.assertEqual(blurred.shape, (100, 100))
        self.assertEqual(blurred.dtype, np.uint8)

    def test_apply_bilateral_filter(self):
        filtered = apply_bilateral_filter(self.img_gray, d=5, sigma_color=50, sigma_space=50)
        self.assertEqual(filtered.shape, (100, 100))

    def test_apply_clahe(self):
        clahe = apply_clahe(self.img_gray, clip_limit=2.0)
        self.assertEqual(clahe.shape, (100, 100))
        self.assertEqual(clahe.dtype, np.uint8)

    def test_morphological_transforms(self):
        tophat = apply_morphological_tophat(self.img_gray, kernel_size=15)
        blackhat = apply_morphological_blackhat(self.img_gray, kernel_size=15)
        self.assertEqual(tophat.shape, (100, 100))
        self.assertEqual(blackhat.shape, (100, 100))
        # Top-hat isolates bright features smaller than kernel
        self.assertGreater(tophat[50, 50], 0)

    def test_enhance_surface_features(self):
        res = enhance_surface_features(self.img_bgr)
        self.assertIn("enhanced", res)
        self.assertIn("morph_residual", res)
        self.assertEqual(res["morph_residual"].shape, (100, 100))


if __name__ == "__main__":
    unittest.main()

"""
Synthetic industrial surface defect generator.
Creates reproducible benchmark images with textured backgrounds and ground truth masks.
"""
import os
import random
from typing import Tuple, List
import cv2
import numpy as np


def generate_brushed_metal_background(width: int = 640, height: int = 480, grain: float = 12.0) -> np.ndarray:
    """Generates a realistic brushed metal texture background with horizontal grain."""
    base_val = 180 + np.random.randint(-15, 15)
    bg = np.full((height, width), base_val, dtype=np.float32)
    # Add horizontal directional grain
    horizontal_lines = np.random.normal(0, grain, (height, 1))
    bg += horizontal_lines
    # Add random 2D noise
    bg += np.random.normal(0, 4.0, (height, width))
    # Add subtle non-uniform illumination gradient
    y_grad = np.linspace(0.9, 1.1, height)[:, None]
    x_grad = np.linspace(0.95, 1.05, width)[None, :]
    bg = bg * y_grad * x_grad
    return np.clip(bg, 0, 255).astype(np.uint8)


def inject_crack(image: np.ndarray, mask: np.ndarray) -> None:
    """Injects a tortuous, branching dark crack into the surface."""
    h, w = image.shape[:2]
    # Random starting point
    x = random.randint(w // 4, 3 * w // 4)
    y = random.randint(h // 4, 3 * h // 4)
    length = random.randint(80, 160)
    angle = random.uniform(0, 2 * np.pi)

    points = [(x, y)]
    for _ in range(length):
        angle += random.uniform(-0.4, 0.4)
        step = random.uniform(1.0, 2.5)
        x += int(step * np.cos(angle))
        y += int(step * np.sin(angle))
        x = max(5, min(w - 6, x))
        y = max(5, min(h - 6, y))
        points.append((x, y))

    for i in range(len(points) - 1):
        pt1 = points[i]
        pt2 = points[i + 1]
        thickness = random.choice([2, 3])
        # Dark crack line
        cv2.line(image, pt1, pt2, (random.randint(20, 50), random.randint(20, 50), random.randint(20, 50)), thickness)
        cv2.line(mask, pt1, pt2, 255, thickness + 1)


def inject_scratch(image: np.ndarray, mask: np.ndarray) -> None:
    """Injects a linear surface scratch with specular highlight edge."""
    h, w = image.shape[:2]
    x1 = random.randint(50, w - 150)
    y1 = random.randint(50, h - 150)
    length = random.randint(70, 150)
    angle = random.uniform(0, np.pi)
    x2 = int(x1 + length * np.cos(angle))
    y2 = int(y1 + length * np.sin(angle))
    x2 = max(5, min(w - 6, x2))
    y2 = max(5, min(h - 6, y2))

    # Dark groove
    cv2.line(image, (x1, y1), (x2, y2), (30, 30, 30), 2)
    # Bright specular edge adjacent to groove
    cv2.line(image, (x1 + 1, y1 + 1), (x2 + 1, y2 + 1), (235, 235, 235), 1)
    cv2.line(mask, (x1, y1), (x2, y2), 255, 3)


def inject_pinhole(image: np.ndarray, mask: np.ndarray) -> None:
    """Injects small circular dark pit or void."""
    h, w = image.shape[:2]
    cx = random.randint(60, w - 60)
    cy = random.randint(60, h - 60)
    radius = random.randint(4, 10)
    cv2.circle(image, (cx, cy), radius, (20, 20, 20), -1)
    cv2.circle(mask, (cx, cy), radius + 1, 255, -1)


def inject_stain(image: np.ndarray, mask: np.ndarray) -> None:
    """Injects diffuse discoloration spot."""
    h, w = image.shape[:2]
    cx = random.randint(70, w - 70)
    cy = random.randint(70, h - 70)
    axes = (random.randint(18, 35), random.randint(12, 25))
    angle = random.randint(0, 180)
    
    stain_layer = np.zeros((h, w), dtype=np.uint8)
    cv2.ellipse(stain_layer, (cx, cy), axes, angle, 0, 360, 255, -1)
    stain_blurred = cv2.GaussianBlur(stain_layer, (21, 21), 7.0)
    
    # Darken image where stain is present
    factor = 1.0 - (stain_blurred.astype(np.float32) / 255.0) * 0.45
    for c in range(3):
        image[:, :, c] = np.clip(image[:, :, c] * factor, 0, 255).astype(np.uint8)
    
    mask[stain_blurred > 60] = 255


def create_sample_dataset(output_dir: str, count_per_class: int = 3) -> None:
    """
    Generates a balanced dataset of benchmark images and ground truth masks:
    classes: crack, scratch, pinhole, stain, defect_free.
    """
    os.makedirs(os.path.join(output_dir, "images"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "ground_truth"), exist_ok=True)

    classes = ["crack", "scratch", "pinhole", "stain", "defect_free"]

    for defect_type in classes:
        for idx in range(1, count_per_class + 1):
            bg = generate_brushed_metal_background(640, 480)
            img = cv2.cvtColor(bg, cv2.COLOR_GRAY2BGR)
            mask = np.zeros((480, 640), dtype=np.uint8)

            if defect_type == "crack":
                inject_crack(img, mask)
            elif defect_type == "scratch":
                inject_scratch(img, mask)
            elif defect_type == "pinhole":
                inject_pinhole(img, mask)
            elif defect_type == "stain":
                inject_stain(img, mask)
            elif defect_type == "defect_free":
                pass  # Clean surface

            file_stem = f"{defect_type}_{idx:02d}"
            img_path = os.path.join(output_dir, "images", f"{file_stem}.png")
            gt_path = os.path.join(output_dir, "ground_truth", f"{file_stem}_mask.png")

            cv2.imwrite(img_path, img)
            cv2.imwrite(gt_path, mask)

    print(f"Generated {len(classes) * count_per_class} benchmark samples in {output_dir}")

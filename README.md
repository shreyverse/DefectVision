# 🔍 DefectVision

### Automated Industrial Surface Defect Detection & Quality Inspection System

DefectVision is a Computer Vision-based industrial inspection system designed to automatically **detect, segment, classify, measure, and analyze surface defects** in manufactured materials.

The system combines classical image-processing and computer-vision techniques to identify defects such as **cracks, scratches, pinholes, stains, and other surface anomalies**.

---

## 🚀 Project Overview

In modern manufacturing, manual surface inspection can be time-consuming and affected by human fatigue and subjectivity.

**DefectVision** provides an automated inspection pipeline that processes surface images and identifies potential defects using a combination of:

- Image preprocessing
- Contrast enhancement
- Morphological operations
- Statistical thresholding
- Watershed segmentation
- Geometric feature extraction
- Texture analysis
- Defect classification
- Visual inspection overlays
- Quantitative evaluation

The system is designed to operate using standard CPU-based image-processing techniques without requiring a dedicated GPU.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🔍 **Defect Detection** | Detects potential defects from industrial surface images |
| 🧹 **Image Preprocessing** | Noise reduction and contrast enhancement |
| 🎯 **Defect Segmentation** | Separates defect regions from the surface |
| 📐 **Feature Extraction** | Extracts geometric and texture descriptors |
| 🏷️ **Defect Classification** | Categorizes detected defect regions |
| 📊 **Inspection Analytics** | Calculates IoU, accuracy, precision, recall and F1-score |
| 🖼️ **Visual Diagnostics** | Generates annotated images and diagnostic dashboards |
| ⚡ **Performance Benchmarking** | Measures processing latency and FPS |
| 📄 **PDF Reporting** | Generates structured inspection reports |
| 🧪 **Automated Testing** | Includes unit and integration tests |

---

# 🧠 Computer Vision Pipeline

```text
┌──────────────────────────┐
│   Industrial Surface     │
│          Image            │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│   Image Preprocessing    │
│ Bilateral / Gaussian     │
│ Filtering + CLAHE        │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Feature Enhancement      │
│ Top-Hat / Black-Hat      │
│ Morphological Operations │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│   Defect Segmentation    │
│ Thresholding + Watershed │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│   Feature Extraction     │
│ Geometry + GLCM + Gabor  │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│   Defect Classification  │
│ Crack / Scratch / Stain  │
│ Pinhole / Defect-Free    │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Analysis & Visualization │
│ Metrics + Overlays       │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│     Inspection Report    │
└──────────────────────────┘
🔬 Defect Detection Techniques
1. Image Preprocessing

The preprocessing stage improves image quality and makes surface abnormalities easier to detect.

Techniques include:

Bilateral Filtering
Gaussian Blurring
CLAHE
Grayscale Conversion
Morphological Filtering
2. Feature Enhancement

Morphological transformations are used to emphasize localized defects while reducing the influence of regular surface textures.

Implemented techniques include:

White Top-Hat Transformation
Black-Hat Transformation
Morphological Opening
Morphological Closing
3. Defect Segmentation

Potential defect regions are separated from the background using:

Statistical Thresholding
Otsu Thresholding
Background Subtraction
Distance Transform
Marker-Controlled Watershed

Watershed segmentation is particularly useful for separating touching or overlapping defect regions.

4. Feature Extraction

For every detected region, DefectVision can extract geometric and texture-based descriptors.

Geometric Features
Hu Moments
Circularity
Solidity
Aspect Ratio
Area
Bounding Box Dimensions
Texture Features
GLCM / Haralick Features
Gabor Filter Responses
Multi-orientation Texture Analysis
🏷️ Supported Defect Classes

The documented pipeline works with the following defect categories:

┌───────────────────┐
│      CRACK        │
├───────────────────┤
│     SCRATCH       │
├───────────────────┤
│      PINHOLE      │
├───────────────────┤
│       STAIN       │
├───────────────────┤
│   DEFECT-FREE     │
└───────────────────┘
📊 Evaluation

The project includes a ground-truth evaluation pipeline for measuring segmentation and classification performance.

The documented benchmark uses 20 ground-truth samples.

Reported Results
Metric	Result
Mean IoU	0.6341
Overall Accuracy	85.00%
Macro F1-Score	0.8421
Per-Class Evaluation
Class	Precision	Recall	F1
CRACK	0.67	0.50	0.57
DEFECT-FREE	1.00	1.00	1.00
PINHOLE	1.00	1.00	1.00
SCRATCH	0.75	0.75	0.75
STAIN	0.80	1.00	0.89

Note: These are the documented benchmark results for the existing project. Actual results may vary depending on hardware, environment, and input data.

⚡ Performance Benchmark

The documented performance benchmark uses a 640 × 480 frame resolution.

Performance Metric	Result
Mean Latency	13.56 ms
Minimum Latency	12.25 ms
Maximum Latency	14.92 ms
95th Percentile	14.60 ms
Throughput	73.77 FPS

Actual performance may vary depending on the machine and execution environment.

🖼️ Diagnostic Visualization

For every inspected image, DefectVision can generate diagnostic outputs including:

┌───────────────────────┬───────────────────────┐
│                       │                       │
│    Original Image     │   Processed Image     │
│                       │                       │
├───────────────────────┼───────────────────────┤
│                       │                       │
│    Defect Mask        │   Annotated Result    │
│                       │                       │
└───────────────────────┴───────────────────────┘

The annotated output can include:

Defect bounding boxes
Defect class
Confidence information
Pixel dimensions
Severity information
🛠️ Technology Stack
Programming
Python 3.8+
Computer Vision
OpenCV
Scikit-Image
Scientific Computing
NumPy
SciPy
Data & Analytics
Pandas
Visualization
Matplotlib
Reporting
ReportLab
PyMuPDF
PyPDF
Testing
Python unittest
📁 Project Structure
DefectVision/
│
├── data/
│   ├── samples/
│   │   └── Sample surface images
│   │
│   └── benchmark/
│       ├── images/
│       └── ground_truth/
│
├── docs/
│   └── diagrams/
│       ├── architecture_diagram.png
│       ├── workflow_diagram.png
│       └── class_diagram.png
│
├── output/
│   └── inspections/
│
├── reports/
│   ├── generate_report.py
│   ├── generate_diagrams.py
│   └── DefectVision_Project_Report.pdf
│
├── src/
│   ├── core/
│   ├── preprocessing/
│   ├── features/
│   ├── segmentation/
│   ├── classifier/
│   ├── analytics/
│   ├── data_generator.py
│   ├── pipeline.py
│   └── cli/
│       └── main.py
│
├── tests/
│
├── requirements.txt
├── setup.py
├── statement.md
├── .gitignore
└── README.md
⚙️ Installation
Prerequisites
Python 3.8+
pip
Git

Supported operating systems:

Windows
Linux
macOS
1. Clone the Repository
git clone https://github.com/shreyverse/DefectVision.git
cd DefectVision
2. Create a Virtual Environment
Windows
python -m venv venv
venv\Scripts\activate
Linux / macOS
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
🖥️ Command-Line Usage

DefectVision provides a command-line interface for running different inspection operations.

🔍 Inspect a Single Image
python -m src.cli.main inspect \
    --input data/samples/sample_scratch.png \
    --output output/inspections \
    --verbose

Generated outputs may include:

output/inspections/
├── sample_scratch_annotated.png
├── sample_scratch_quad.png
└── inspection_summary.json
📂 Batch Inspection

Process all images inside a directory:

python -m src.cli.main inspect \
    --input data/samples \
    --output output/inspections
📊 Ground-Truth Evaluation

Evaluate the system against ground-truth masks:

python -m src.cli.main evaluate \
    --images data/benchmark/images \
    --ground-truth data/benchmark/ground_truth \
    --output output/eval_results.json

Evaluation metrics include:

Mean IoU
Accuracy
Macro F1-score
Precision
Recall
⚡ Performance Benchmark

Run the performance benchmark:

python -m src.cli.main benchmark \
    --iterations 30 \
    --width 640 \
    --height 480 \
    --output output/benchmark_results.json
🧪 Generate Sample Data

Generate synthetic benchmark samples:

python -m src.cli.main generate-samples \
    --output data/benchmark \
    --count 4
📄 Generate Project Report

Generate the project report:

python -m src.cli.main report \
    --output reports/DefectVision_Project_Report.pdf
🧪 Testing

DefectVision includes automated unit and integration tests using Python's unittest framework.

Run the complete test suite:

python -m unittest discover -s tests -p "test_*.py" -v

The test suite covers areas including:

CLI functionality
Image preprocessing
CLAHE
Gaussian filtering
Bilateral filtering
Morphological operations
Feature extraction
Gabor features
GLCM features
Geometric features
Thresholding
Watershed segmentation
End-to-end pipeline inspection

The documented project test suite contains 19 tests.

🎯 Applications

DefectVision can be adapted for automated inspection scenarios including:

🏭 Steel surface inspection
🔩 Aluminum manufacturing
🧱 Ceramic manufacturing
💾 Semiconductor inspection
⚙️ Industrial component inspection
🔍 Automated quality control
📊 Manufacturing defect analysis
🔮 Future Scope

The system can be extended with:

Deep-learning-based defect detection
CNN-based classification
YOLO-based real-time detection
GPU acceleration
Live industrial camera integration
Web-based monitoring dashboard
Database-backed inspection history
Automated production-line alerts
Cloud-based analytics
Continuous model improvement
📌 Project Information
Field	Details
Project Name	DefectVision
Domain	Computer Vision
Focus	Industrial Machine Vision & Quality Inspection
Language	Python
Primary Libraries	OpenCV, Scikit-Image, NumPy, SciPy
Interface	Command Line
Testing	Python unittest
📜 License

This project is released under the MIT License.

⭐ Summary

DefectVision demonstrates how classical Computer Vision techniques can be combined to create an automated industrial surface inspection pipeline.

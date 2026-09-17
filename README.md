# DefectVision: Automated Industrial Surface Defect Detection & Quality Inspection System

DefectVision is an automated industrial surface defect detection and quality inspection system designed to detect, segment, classify, and analyze surface defects in manufactured materials.

The system is designed for applications such as inspection of steel, aluminum, silicon wafers, ceramics, and other industrial surfaces where manual inspection can be slow and subjective.

---

## 🚀 Overview

Quality inspection in manufacturing environments often requires identifying small and difficult-to-detect surface abnormalities.

DefectVision uses image processing and computer vision techniques to automatically identify defects such as:

- Cracks
- Scratches
- Pinholes
- Surface stains
- Other localized surface anomalies

The system processes input images, enhances defect-related features, separates defective regions from the background, extracts useful measurements, and generates visual inspection results.

---

## ✨ Key Features

### 🔍 Automated Defect Detection
Automatically identifies potential defects from industrial surface images.

### 🧹 Image Preprocessing
Uses multiple image-processing techniques to improve defect visibility:

- Bilateral Filtering
- Gaussian Blurring
- CLAHE
- Morphological Operations
- White Top-Hat Transformation
- Black-Hat Transformation

### 🎯 Defect Segmentation
Separates defect regions from the surrounding surface using:

- Statistical Thresholding
- Otsu Thresholding
- Background Subtraction
- Distance Transforms
- Watershed Segmentation

### 📐 Feature Extraction

The system extracts geometric and texture-based features including:

- Hu Moments
- Circularity
- Solidity
- Aspect Ratio
- GLCM / Haralick Texture Features
- Gabor Filter Features

### 🏷️ Defect Classification

Detected regions can be analyzed and categorized into defect classes such as:

- Crack
- Scratch
- Pinhole
- Stain
- Defect-Free Surface

### 📊 Inspection Analytics

The system provides:

- Defect measurements
- Bounding boxes
- Severity information
- Segmentation metrics
- Classification metrics
- IoU evaluation
- F1-score and accuracy measurements

### 🖼️ Diagnostic Visualization

DefectVision generates visual inspection dashboards containing:

1. Original surface image
2. Enhanced / processed image
3. Defect segmentation mask
4. Annotated defect detection result

### ⚡ Performance Benchmarking

The project includes a benchmarking module for measuring:

- Processing latency
- Minimum and maximum latency
- 95th percentile latency
- Processing throughput / FPS

### 📄 Automated Reports

The system can generate structured PDF inspection reports containing project and experimental information.

### 🧪 Automated Testing

The project includes unit and integration tests using Python's `unittest` framework.

---

## 🏗️ System Workflow

```text
             Input Surface Image
                     │
                     ▼
            Image Preprocessing
                     │
                     ▼
        Feature Enhancement & Filtering
                     │
                     ▼
            Defect Segmentation
                     │
                     ▼
           Candidate Region Detection
                     │
                     ▼
          Feature Extraction
                     │
                     ▼
          Defect Classification
                     │
                     ▼
        Defect Measurement & Analysis
                     │
                     ▼
       Visualization & Inspection Report
       🧠 Computer Vision Pipeline

The inspection pipeline consists of several major stages.

1. Input

The system accepts individual surface images or directories containing multiple images.

2. Preprocessing

Noise reduction and contrast enhancement are performed using techniques such as bilateral filtering, Gaussian filtering, and CLAHE.

3. Feature Enhancement

Morphological operations such as white top-hat and black-hat transformations help highlight localized surface abnormalities.

4. Segmentation

Potential defect regions are isolated using statistical thresholding, Otsu thresholding, background subtraction, and watershed-based separation.

5. Feature Extraction

Geometric and texture descriptors are calculated for detected regions.

6. Classification

Detected regions are analyzed and categorized into relevant defect classes.

7. Visualization

The system generates annotated images and diagnostic dashboards showing detected defects and their measurements.

🛠️ Technologies Used
Technology	Purpose
Python	Core programming language
OpenCV	Computer vision and image processing
Scikit-Image	Image processing and feature extraction
NumPy	Numerical and matrix operations
SciPy	Scientific computing
Pandas	Data and metric analysis
Matplotlib	Visualization
ReportLab	PDF report generation
PyMuPDF	PDF processing
PyPDF	PDF utilities
unittest	Automated testing
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
Windows, Linux, or macOS
1. Clone the Repository
git clone https://github.com/YOUR_USERNAME/DefectVision.git
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
🖥️ Usage

DefectVision provides a command-line interface for different inspection operations.

Inspect a Single Image
python -m src.cli.main inspect --input data/samples/sample_scratch.png --output output/inspections --verbose

The system generates inspection outputs such as:

output/inspections/
├── sample_scratch_annotated.png
├── sample_scratch_quad.png
└── inspection_summary.json
Batch Image Inspection

To inspect multiple images:

python -m src.cli.main inspect --input data/samples --output output/inspections
Ground-Truth Evaluation

Evaluate segmentation and classification performance:

python -m src.cli.main evaluate \
    --images data/benchmark/images \
    --ground-truth data/benchmark/ground_truth \
    --output output/eval_results.json

The evaluation includes metrics such as:

Mean IoU
Accuracy
Macro F1-score
Per-class precision
Per-class recall
Performance Benchmark

Run the processing performance benchmark:

python -m src.cli.main benchmark \
    --iterations 30 \
    --width 640 \
    --height 480 \
    --output output/benchmark_results.json

The benchmark measures:

Mean processing latency
Minimum latency
Maximum latency
95th percentile latency
Throughput in FPS
Generate Sample Data

Generate synthetic benchmark samples:

python -m src.cli.main generate-samples \
    --output data/benchmark \
    --count 4
Generate Project Report

Generate the project PDF report:

python -m src.cli.main report \
    --output reports/DefectVision_Project_Report.pdf
🧪 Testing

The project contains automated unit and integration tests.

Run the complete test suite:

python -m unittest discover -s tests -p "test_*.py" -v

The existing project contains tests covering areas including:

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
Pipeline inspection
📊 Evaluation

The existing benchmark documentation reports evaluation results on a set of 20 ground-truth samples.

Reported metrics include:

Mean IoU          : 0.6341
Overall Accuracy  : 85.00%
Macro F1-Score    : 0.8421

Per-class evaluation includes:

CRACK
DEFECT_FREE
PINHOLE
SCRATCH
STAIN

These values represent the project's documented benchmark results and may vary depending on the environment and input data.

⚡ Performance

The documented benchmark uses:

Frame Resolution : 640 × 480
Mean Latency     : 13.56 ms
95th Percentile  : 14.60 ms
Throughput       : 73.77 FPS

Actual performance can vary depending on hardware, Python version, image characteristics, and system configuration.

📸 Diagnostic Output

For an inspected image, DefectVision can generate a diagnostic visualization containing:

┌─────────────────────┬─────────────────────┐
│                     │                     │
│   Original Image    │ Processed Image     │
│                     │                     │
├─────────────────────┼─────────────────────┤
│                     │                     │
│   Defect Mask       │ Annotated Result    │
│                     │                     │
└─────────────────────┴─────────────────────┘

The annotated output provides information about detected defect regions and their characteristics.

🎯 Applications

DefectVision can be applied to automated quality inspection scenarios such as:

Steel surface inspection
Aluminum surface inspection
Ceramic manufacturing
Semiconductor surface inspection
Industrial component inspection
Automated quality control
Manufacturing defect analysis
🔮 Future Scope

Possible future improvements include:

Deep-learning-based defect detection
CNN-based image classification
YOLO-based real-time object detection
GPU acceleration
Live industrial camera integration
Web-based monitoring dashboard
Database integration for inspection history
Automated production-line alerts
Cloud-based inspection analytics
Continuous model improvement using new inspection data
👨‍💻 Project Information

Project: DefectVision
Domain: Computer Vision
Focus: Industrial Machine Vision & Quality Inspection
Programming Language: Python

📜 License

This project is released under the MIT License.

⭐ Project Summary

DefectVision demonstrates how classical Computer Vision and image-processing techniques can be combined to create an automated industrial surface inspection pipeline.

The system integrates preprocessing, feature enhancement, segmentation, feature extraction, classification, analytics, visualization, benchmarking, testing, and automated reporting into a single inspection workflow.
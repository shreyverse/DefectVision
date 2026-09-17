# Project Statement: DefectVision

## 1. Problem Statement
In high-precision manufacturing industries?such as automotive body panel fabrication, semiconductor substrate manufacturing, cold-rolled sheet metal rolling, and structural ceramics?surface quality is synonymous with mechanical durability and safety. Minute surface flaws (hairline cracks, linear scratches, micro-pinholes, and chemical stains) act as catastrophic stress concentrators leading to mechanical fatigue failure, corrosion initiation, or immediate product rejection.

Traditional industrial quality control relies on manual human inspection under strobe illumination. However, manual inspection is fundamentally subjective, suffers from rapid human fatigue degradation (effective defect detection rates drop below 70% after only 20 minutes of continuous monitoring), and introduces severe throughput bottlenecks (< 2 parts per second).

**DefectVision** solves this critical problem by providing an automated, high-throughput, deterministic Computer Vision inspection system that operates directly on standard edge CPUs. The system autonomously detects, sizes, localizes, and categorizes surface defects against challenging textured and non-uniform backgrounds at line speeds (> 70 FPS).

---

## 2. Scope of the Project

### In-Scope:
- **Multi-Format Ingestion:** Ingestion of raw digital imagery from industrial area-scan or line-scan cameras (PNG, JPG, BMP, TIFF).
- **Edge-Preserving Filtering:** Suppression of Gaussian and impulse sensor noise without blurring sharp defect transitions using Bilateral and Median filtering.
- **Illumination & Texture Decoupling:** Contrast-Limited Adaptive Histogram Equalization (CLAHE) and morphological Top-Hat/Black-Hat bandpass decomposition to decouple defect anomalies from anisotropic background grain (e.g., brushed metal).
- **Dual-Mode Segmentation:** High-frequency structural anomaly segmentation via statistical variance thresholding combined with low-frequency diffuse stain detection.
- **Watershed Separation:** Distance-transform and marker-controlled watershed decomposition to separate clustered or touching defect bodies.
- **Invariant Feature Metrology:** Computation of 7 log-transformed Hu moment invariants, circularity/compactness, aspect ratio, solidity, extent, equivalent diameter, and Haralick GLCM texture metrics.
- **Multi-Class Defect Categorization:** Deterministic classification into five industrial categories: `CRACK`, `SCRATCH`, `PINHOLE`, `STAIN`, and `DEFECT_FREE`.
- **Severity Grading:** Grading flaws into `NEGLIGIBLE`, `MINOR`, `MODERATE`, and `CRITICAL` based on geometric area thresholds and structural risk weighting.
- **Command-Line Interface (CLI):** 100% headless, terminal-executable tool suite (`inspect`, `evaluate`, `benchmark`, `generate-samples`, `report`).
- **Telemetry & Reporting:** Automated export of annotated frames, 2x2 diagnostic quad dashboards, JSON inspection logs, and an official 15-section project report PDF.

### Out-of-Scope (Future Iterations):
- Direct robotic PLC hardware integration via Modbus/EtherCAT.
- 3D photometric stereo normal reconstruction (requires multi-light hardware synchronizer).

---

## 3. Target Users
1. **Industrial Quality Assurance Engineers:** Setting inspection tolerance thresholds, reviewing defect heatmaps, and monitoring manufacturing line yield.
2. **Manufacturing & Automation System Integrators:** Embedding the CLI pipeline into robotic pick-and-place or sorting conveyor systems.
3. **Computer Vision & Machine Learning Researchers:** Benchmarking classical morphological descriptors against modern deep learning architectures for edge inference.
4. **Plant Operations Managers:** Analyzing real-time defect distribution summaries to detect tooling wear and machinery degradation before catastrophic breakdowns.

---

## 4. High-Level Features
1. **Real-Time High Throughput:** Executes full inspection in under 15ms per frame (> 70 FPS on standard multi-core CPUs), fulfilling line-rate requirements without requiring expensive GPUs.
2. **Deterministic & Explainable Decision Engine:** Flaws are sized and categorized according to measurable physical invariants (aspect ratio, circularity, area in $mm^2$ or pixels) rather than opaque neural network black-box embeddings.
3. **Multi-Defect Discrimination:** Accurately isolates long branching cracks from linear abrasion scratches and discriminates deep dark pinholes from light surface discoloration stains.
4. **Zero-Leakage Defect-Free Precision:** 100% precision on pristine surfaces, eliminating costly false-alarm conveyor line halts.
5. **Turnkey CLI & Reproducibility:** Single-command execution for single images, batch directories, ground-truth evaluations, synthetic sample generation, and automated PDF report compilation.

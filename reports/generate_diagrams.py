"""
Generates high-resolution architectural, workflow, and UML diagrams for documentation and report.
"""
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

OUTPUT_DIR = "D:/SurfaceVision-CV/docs/diagrams"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_architecture_diagram():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Colors
    c_blue = "#2B6CB0"
    c_teal = "#2C7A7B"
    c_orange = "#C05621"
    c_purple = "#6B46C1"
    c_green = "#276749"
    c_bg = "#EDF2F7"

    # Title
    ax.text(50, 95, "SurfaceVision: System Architecture", ha="center", va="center", fontsize=14, fontweight="bold", color="#1A202C")

    # Layer 1: Ingestion
    ax.add_patch(patches.FancyBboxPatch((5, 68), 26, 20, boxstyle="round,pad=1", ec=c_blue, fc=c_bg, lw=2))
    ax.text(18, 83, "1. Input & Ingestion", ha="center", fontsize=10, fontweight="bold", color=c_blue)
    ax.text(18, 76, "• Multi-format Loader\n• Resolution Scaling\n• Format Normalization", ha="center", fontsize=8)

    # Arrow 1 -> 2
    ax.annotate("", xy=(36, 78), xytext=(32, 78), arrowprops=dict(arrowstyle="->", lw=2, color="#4A5568"))

    # Layer 2: Preprocessing
    ax.add_patch(patches.FancyBboxPatch((37, 68), 26, 20, boxstyle="round,pad=1", ec=c_teal, fc=c_bg, lw=2))
    ax.text(50, 83, "2. Preprocessing Layer", ha="center", fontsize=10, fontweight="bold", color=c_teal)
    ax.text(50, 75, "• Bilateral Filtering\n• CLAHE Equalization\n• Top-Hat / Black-Hat Residual", ha="center", fontsize=8)

    # Arrow 2 -> 3
    ax.annotate("", xy=(68, 78), xytext=(64, 78), arrowprops=dict(arrowstyle="->", lw=2, color="#4A5568"))

    # Layer 3: Segmentation
    ax.add_patch(patches.FancyBboxPatch((69, 68), 26, 20, boxstyle="round,pad=1", ec=c_orange, fc=c_bg, lw=2))
    ax.text(82, 83, "3. Anomaly Segmentation", ha="center", fontsize=10, fontweight="bold", color=c_orange)
    ax.text(82, 75, "• Statistical Residual Split\n• Diffuse Anomaly Subtraction\n• Watershed Separation", ha="center", fontsize=8)

    # Down arrow from 3 to 4
    ax.annotate("", xy=(82, 58), xytext=(82, 67), arrowprops=dict(arrowstyle="->", lw=2, color="#4A5568"))

    # Layer 4: Feature Extraction
    ax.add_patch(patches.FancyBboxPatch((69, 36), 26, 20, boxstyle="round,pad=1", ec=c_purple, fc=c_bg, lw=2))
    ax.text(82, 51, "4. Feature Extraction", ha="center", fontsize=10, fontweight="bold", color=c_purple)
    ax.text(82, 43, "• GLCM Texture Descriptors\n• Gabor Filter Bank Energy\n• Geometric & Hu Moments", ha="center", fontsize=8)

    # Left arrow from 4 to 5
    ax.annotate("", xy=(64, 46), xytext=(68, 46), arrowprops=dict(arrowstyle="->", lw=2, color="#4A5568"))

    # Layer 5: Classification
    ax.add_patch(patches.FancyBboxPatch((37, 36), 26, 20, boxstyle="round,pad=1", ec="#D69E2E", fc=c_bg, lw=2))
    ax.text(50, 51, "5. Defect Classification", ha="center", fontsize=10, fontweight="bold", color="#B7791F")
    ax.text(50, 43, "• Rule & Decision Engine\n• 5-Class Categorization\n• Industrial Severity Rank", ha="center", fontsize=8)

    # Left arrow from 5 to 6
    ax.annotate("", xy=(32, 46), xytext=(36, 46), arrowprops=dict(arrowstyle="->", lw=2, color="#4A5568"))

    # Layer 6: Output & Analytics
    ax.add_patch(patches.FancyBboxPatch((5, 36), 26, 20, boxstyle="round,pad=1", ec=c_green, fc=c_bg, lw=2))
    ax.text(18, 51, "6. Reporting & Analytics", ha="center", fontsize=10, fontweight="bold", color=c_green)
    ax.text(18, 43, "• Visual BBox Overlays\n• 2x2 Diagnostic Dashboard\n• JSON/CSV & PDF Report", ha="center", fontsize=8)

    # Bottom Foundation Bar
    ax.add_patch(patches.Rectangle((5, 8), 90, 18, ec="#4A5568", fc="#F7FAFC", lw=1.5, ls="--"))
    ax.text(50, 21, "Core Cross-Cutting Capabilities & Interfaces", ha="center", fontsize=10, fontweight="bold", color="#2D3748")
    ax.text(50, 13, "CLI Dispatcher (Inspect, Evaluate, Benchmark, Report) | Configuration Management | Strict Logging & Telemetry", ha="center", fontsize=8)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "architecture_diagram.png"), bbox_inches="tight", dpi=300)
    plt.close()


def generate_workflow_diagram():
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    ax.text(50, 95, "SurfaceVision: Process Flowchart", ha="center", fontsize=14, fontweight="bold", color="#1A202C")

    steps = [
        ("Acquire Frame", 10, "#3182CE"),
        ("Bilateral\nDenoising", 26, "#319795"),
        ("CLAHE & Top/Black\nHat Residual", 42, "#DD6B20"),
        ("Dual-Threshold\n& Watershed", 58, "#805AD5"),
        ("Morphological\nContour Filter", 74, "#D69E2E"),
        ("Classification\n& Decision", 90, "#38A169")
    ]

    for label, x_pos, color in steps:
        ax.add_patch(patches.FancyBboxPatch((x_pos - 6, 40), 12, 24, boxstyle="round,pad=0.5", ec=color, fc="#F7FAFC", lw=2))
        ax.text(x_pos, 52, label, ha="center", va="center", fontsize=7.5, fontweight="bold", color=color)

    for i in range(len(steps) - 1):
        x1 = steps[i][1] + 6.5
        x2 = steps[i+1][1] - 6.5
        ax.annotate("", xy=(x2, 52), xytext=(x1, 52), arrowprops=dict(arrowstyle="->", lw=2, color="#718096"))

    # Outcomes
    ax.annotate("", xy=(90, 26), xytext=(90, 39), arrowprops=dict(arrowstyle="->", lw=1.5, color="#718096"))
    ax.add_patch(patches.FancyBboxPatch((76, 12), 28, 14, boxstyle="round,pad=0.5", ec="#2B6CB0", fc="#EBF8FF", lw=1.5))
    ax.text(90, 19, "Output Annotations,\nMetrics & Inspection Logs", ha="center", va="center", fontsize=8, fontweight="bold", color="#2B6CB0")

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "workflow_diagram.png"), bbox_inches="tight", dpi=300)
    plt.close()


def generate_uml_usecase_diagram():
    fig, ax = plt.subplots(figsize=(9, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    ax.text(50, 95, "UML Use Case Diagram: SurfaceVision", ha="center", fontsize=14, fontweight="bold", color="#1A202C")

    # Boundary Box
    ax.add_patch(patches.Rectangle((25, 5), 70, 85, ec="#718096", fc="#F8FAFC", lw=1.5))
    ax.text(60, 86, "SurfaceVision System Boundary", ha="center", fontsize=10, fontweight="bold", color="#4A5568")

    # Actor: Quality Engineer / Automated Rig
    ax.plot([12, 12], [55, 65], color="#2D3748", lw=3) # Body
    circle = plt.Circle((12, 70), 3.5, ec="#2D3748", fc="#E2E8F0", lw=2) # Head
    ax.add_patch(circle)
    ax.plot([5, 19], [60, 60], color="#2D3748", lw=2.5) # Arms
    ax.plot([12, 7], [55, 45], color="#2D3748", lw=2.5) # Left Leg
    ax.plot([12, 17], [55, 45], color="#2D3748", lw=2.5) # Right Leg
    ax.text(12, 38, "Quality Inspector\n/ Automated Rig", ha="center", fontsize=8.5, fontweight="bold", color="#1A202C")

    # Use Cases
    use_cases = [
        ("UC-1: Single/Batch Surface Inspection", 72),
        ("UC-2: Anomaly Localization & Sizing", 56),
        ("UC-3: Multi-Class Defect Categorization", 40),
        ("UC-4: Accuracy & IoU Ground-Truth Evaluation", 24),
        ("UC-5: Real-time Throughput Benchmarking", 10),
    ]

    for title, y in use_cases:
        ellipse = patches.Ellipse((60, y), 36, 9, ec="#3182CE", fc="#EBF8FF", lw=1.5)
        ax.add_patch(ellipse)
        ax.text(60, y, title, ha="center", va="center", fontsize=8, fontweight="bold", color="#2B6CB0")
        ax.plot([19, 42], [55, y], color="#A0AEC0", lw=1.2, ls="--")

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "usecase_diagram.png"), bbox_inches="tight", dpi=300)
    plt.close()


def generate_uml_class_diagram():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    ax.text(50, 95, "UML Class / Component Diagram", ha="center", fontsize=14, fontweight="bold", color="#1A202C")

    # Pipeline Class Box
    ax.add_patch(patches.Rectangle((5, 45), 38, 42, ec="#2B6CB0", fc="#F7FAFC", lw=2))
    ax.add_patch(patches.Rectangle((5, 75), 38, 12, ec="#2B6CB0", fc="#EBF8FF", lw=1))
    ax.text(24, 81, "SurfaceVisionPipeline", ha="center", va="center", fontsize=10, fontweight="bold", color="#2B6CB0")
    ax.text(7, 65, "+ config: InspectionConfig\n+ classifier: DefectClassifier\n\n+ load_image(src): ndarray\n+ process(src): (Result, dict)\n+ inspect_and_visualize()", fontsize=8)

    # DefectRegion Box
    ax.add_patch(patches.Rectangle((55, 52), 40, 35, ec="#2C7A7B", fc="#F7FAFC", lw=2))
    ax.add_patch(patches.Rectangle((55, 75), 40, 12, ec="#2C7A7B", fc="#E6FFFA", lw=1))
    ax.text(75, 81, "DefectRegion", ha="center", va="center", fontsize=10, fontweight="bold", color="#2C7A7B")
    ax.text(57, 64, "+ region_id: int\n+ bbox: (x,y,w,h)\n+ defect_type: DefectClass\n+ severity: DefectSeverity\n+ geometry: GeometricFeatures\n+ texture: TextureFeatures", fontsize=8)

    # DefectClassifier Box
    ax.add_patch(patches.Rectangle((5, 5), 38, 30, ec="#D69E2E", fc="#F7FAFC", lw=2))
    ax.add_patch(patches.Rectangle((5, 23), 38, 12, ec="#D69E2E", fc="#FEFCBF", lw=1))
    ax.text(24, 29, "DefectClassifier", ha="center", va="center", fontsize=10, fontweight="bold", color="#B7791F")
    ax.text(7, 14, "+ confidence_threshold: float\n\n+ predict(geom, tex): (Class, conf, sev)\n+ assess_severity(class, area): Sev", fontsize=8)

    # InspectionResult Box
    ax.add_patch(patches.Rectangle((55, 5), 40, 38, ec="#6B46C1", fc="#F7FAFC", lw=2))
    ax.add_patch(patches.Rectangle((55, 31), 40, 12, ec="#6B46C1", fc="#FAF5FF", lw=1))
    ax.text(75, 37, "InspectionResult", ha="center", va="center", fontsize=10, fontweight="bold", color="#6B46C1")
    ax.text(57, 18, "+ image_path: str\n+ total_defects: int\n+ is_defective: bool\n+ max_severity: DefectSeverity\n+ execution_time_ms: float\n+ to_dict(): dict", fontsize=8)

    # Connectors
    ax.plot([43, 55], [68, 68], color="#4A5568", lw=2) # Pipeline to DefectRegion
    ax.plot([24, 24], [45, 35], color="#4A5568", lw=2) # Pipeline to Classifier
    ax.plot([75, 75], [52, 43], color="#4A5568", lw=2) # DefectRegion to Result

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "class_diagram.png"), bbox_inches="tight", dpi=300)
    plt.close()


def generate_sequence_diagram():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    ax.text(50, 95, "UML Sequence Diagram: Surface Inspection Execution", ha="center", fontsize=13, fontweight="bold", color="#1A202C")

    lifelines = [
        ("User / CLI", 12),
        ("Pipeline", 36),
        ("Preprocess / Seg", 60),
        ("Feature / Class", 84)
    ]

    for name, x in lifelines:
        ax.add_patch(patches.Rectangle((x - 8, 80), 16, 8, ec="#2B6CB0", fc="#EBF8FF", lw=1.5))
        ax.text(x, 84, name, ha="center", va="center", fontsize=8.5, fontweight="bold", color="#2B6CB0")
        ax.plot([x, x], [20, 80], color="#CBD5E0", lw=1.5, ls="--")

    # Sequence Messages
    msgs = [
        (12, 36, 72, "1: inspect_and_visualize(image_path)", True),
        (36, 60, 62, "2: enhance & compute_residuals()", True),
        (60, 36, 54, "3: defect_mask & contours", False),
        (36, 84, 46, "4: extract_features() & predict()", True),
        (84, 36, 38, "5: DefectRegion(type, conf, sev)", False),
        (36, 12, 28, "6: InspectionResult + Overlays", False),
    ]

    for x1, x2, y, text, is_call in msgs:
        ls = "-" if is_call else "--"
        color = "#2B6CB0" if is_call else "#38A169"
        ax.annotate("", xy=(x2, y), xytext=(x1, y), arrowprops=dict(arrowstyle="->", lw=1.8, color=color, ls=ls))
        mid_x = (x1 + x2) / 2
        ax.text(mid_x, y + 2, text, ha="center", fontsize=7.5, fontweight="bold", color="#2D3748")

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "sequence_diagram.png"), bbox_inches="tight", dpi=300)
    plt.close()


if __name__ == "__main__":
    generate_architecture_diagram()
    generate_workflow_diagram()
    generate_uml_usecase_diagram()
    generate_uml_class_diagram()
    generate_sequence_diagram()
    print("All architecture, workflow, and UML diagrams generated in:", OUTPUT_DIR)

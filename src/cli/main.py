"""
Command-Line Interface (CLI) for SurfaceVision Industrial Inspection System.
Provides commands for inspection, batch evaluation, latency benchmarking, and sample generation.
"""
import argparse
import glob
import json
import os
import sys
import time
from typing import List
import cv2
import numpy as np

from ..pipeline import SurfaceVisionPipeline
from ..core.config import get_default_config
from ..analytics.metrics import compute_iou, calculate_classification_metrics, BenchmarkResult
from ..data_generator import create_sample_dataset, generate_brushed_metal_background


def cmd_inspect(args: argparse.Namespace) -> int:
    """Inspects a single image or directory of images."""
    pipeline = SurfaceVisionPipeline()
    output_dir = args.output
    os.makedirs(output_dir, exist_ok=True)

    targets: List[str] = []
    if os.path.isfile(args.input):
        targets.append(args.input)
    elif os.path.isdir(args.input):
        for ext in ("*.png", "*.jpg", "*.jpeg", "*.bmp", "*.tif"):
            targets.extend(glob.glob(os.path.join(args.input, ext)))
    else:
        print(f"[ERROR] Input path not found: {args.input}", file=sys.stderr)
        return 1

    if not targets:
        print(f"[WARNING] No valid image files found at: {args.input}")
        return 0

    print(f"\n============================================================")
    print(f" SurfaceVision Inspection Engine: Processing {len(targets)} image(s)")
    print(f"============================================================")

    all_results = []
    for idx, path in enumerate(targets, start=1):
        try:
            result, overlay, quad = pipeline.inspect_and_visualize(
                path,
                output_dir=output_dir,
                save_quad=args.save_quad
            )
            all_results.append(result.to_dict())

            status = "DEFECTIVE" if result.is_defective else "DEFECT-FREE"
            print(f"[{idx}/{len(targets)}] {os.path.basename(path):<25} -> {status:<12} | "
                  f"Defects: {result.total_defects:<2} | Max Severity: {result.max_severity.value:<10} | "
                  f"Time: {result.execution_time_ms:.1f}ms")

            if args.verbose and result.regions:
                for r in result.regions:
                    print(f"    Region #{r.region_id}: {r.defect_type.value} "
                          f"(Conf: {r.confidence:.2f}, Sev: {r.severity.value}, "
                          f"BBox: {r.bbox}, Area: {r.geometry.area:.1f}px)")
        except Exception as e:
            print(f"[ERROR] Failed processing {path}: {e}", file=sys.stderr)

    # Save summary JSON
    summary_path = os.path.join(output_dir, "inspection_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)

    print(f"\n[DONE] Saved inspection overlays & JSON summary to: {output_dir}\n")
    return 0


def cmd_evaluate(args: argparse.Namespace) -> int:
    """Evaluates pipeline predictions against ground truth masks."""
    pipeline = SurfaceVisionPipeline()
    img_dir = args.images
    gt_dir = args.ground_truth

    if not os.path.isdir(img_dir) or not os.path.isdir(gt_dir):
        print(f"[ERROR] Valid images and ground truth directories required.", file=sys.stderr)
        return 1

    img_files = sorted(glob.glob(os.path.join(img_dir, "*.png")) + glob.glob(os.path.join(img_dir, "*.jpg")))
    if not img_files:
        print(f"[ERROR] No images found in {img_dir}", file=sys.stderr)
        return 1

    print(f"\n============================================================")
    print(f" SurfaceVision Evaluation: Evaluating {len(img_files)} Ground-Truth Samples")
    print(f"============================================================")

    ious = []
    y_true = []
    y_pred = []

    for img_p in img_files:
        stem = os.path.splitext(os.path.basename(img_p))[0]
        # Look for corresponding mask
        gt_candidates = glob.glob(os.path.join(gt_dir, f"{stem}*mask*.*")) + [os.path.join(gt_dir, f"{stem}.png")]
        gt_p = next((p for p in gt_candidates if os.path.isfile(p)), None)

        if not gt_p:
            print(f"[SKIP] Ground truth mask missing for: {img_p}")
            continue

        gt_mask = cv2.imread(gt_p, cv2.IMREAD_GRAYSCALE)
        res, artifacts = pipeline.process(img_p)
        pred_mask = artifacts["defect_mask"]

        iou = compute_iou(pred_mask, gt_mask)
        ious.append(iou)

        # Ground truth class inferred from filename prefix (crack, scratch, pinhole, stain, defect_free)
        expected_class = stem.split("_")[0].upper()
        if expected_class not in ["CRACK", "SCRATCH", "PINHOLE", "STAIN", "DEFECT"]:
            expected_class = "DEFECT_FREE" if np.max(gt_mask) == 0 else "DEFECTIVE"
        elif expected_class == "DEFECT":
            expected_class = "DEFECT_FREE"

        predicted_class = res.regions[0].defect_type.value if res.regions else "DEFECT_FREE"
        y_true.append(expected_class)
        y_pred.append(predicted_class)

    mean_iou = float(np.mean(ious)) if ious else 0.0
    clf_metrics = calculate_classification_metrics(y_true, y_pred)

    print(f"\nEvaluation Results Summary:")
    print(f"  Total Validated Samples : {len(ious)}")
    print(f"  Mean IoU (Segmentation) : {mean_iou:.4f}")
    print(f"  Overall Accuracy        : {clf_metrics['overall_accuracy'] * 100:.2f}%")
    print(f"  Macro F1-Score          : {clf_metrics['macro_f1']:.4f}")
    print("\nPer-Class Performance:")
    for cls_name, m in clf_metrics["classes"].items():
        print(f"  {cls_name:<14} | Precision: {m['precision']:.2f} | Recall: {m['recall']:.2f} | F1: {m['f1_score']:.2f} (n={m['support']})")

    out_dict = {
        "mean_iou": round(mean_iou, 4),
        "classification": clf_metrics,
        "sample_count": len(ious)
    }

    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(out_dict, f, indent=2)
        print(f"\n[DONE] Saved evaluation metrics to: {args.output}")

    return 0


def cmd_benchmark(args: argparse.Namespace) -> int:
    """Measures pipeline inference speed and throughput (FPS)."""
    pipeline = SurfaceVisionPipeline()
    w, h = args.width, args.height
    n = args.iterations

    print(f"\n============================================================")
    print(f" SurfaceVision Benchmark: Measuring Latency over {n} frames ({w}x{h})")
    print(f"============================================================")

    # Warmup
    dummy = cv2.cvtColor(generate_brushed_metal_background(w, h), cv2.COLOR_GRAY2BGR)
    for _ in range(3):
        pipeline.process(dummy)

    latencies = []
    for i in range(n):
        frame = cv2.cvtColor(generate_brushed_metal_background(w, h), cv2.COLOR_GRAY2BGR)
        t0 = time.perf_counter()
        pipeline.process(frame, extract_texture=False)
        dt = (time.perf_counter() - t0) * 1000.0
        latencies.append(dt)

    mean_l = float(np.mean(latencies))
    min_l = float(np.min(latencies))
    max_l = float(np.max(latencies))
    p95_l = float(np.percentile(latencies, 95))
    fps = 1000.0 / mean_l if mean_l > 0 else 0.0

    bench = BenchmarkResult(
        total_images=n,
        mean_latency_ms=mean_l,
        min_latency_ms=min_l,
        max_latency_ms=max_l,
        p95_latency_ms=p95_l,
        fps=fps,
        image_resolution=(h, w)
    )

    print(f"\nPerformance Benchmark Results:")
    print(f"  Frame Resolution : {w}x{h}")
    print(f"  Mean Latency     : {mean_l:.2f} ms")
    print(f"  Min / Max        : {min_l:.2f} ms / {max_l:.2f} ms")
    print(f"  95th Percentile  : {p95_l:.2f} ms")
    print(f"  Throughput (FPS) : {fps:.2f} FPS")

    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(bench.to_dict(), f, indent=2)
        print(f"[DONE] Saved benchmark log to: {args.output}")

    return 0


def cmd_generate_samples(args: argparse.Namespace) -> int:
    """Generates synthetic benchmark dataset with ground-truth masks."""
    out_dir = args.output
    count = args.count
    print(f"Generating synthetic industrial dataset in: {out_dir} ({count} per class)...")
    create_sample_dataset(out_dir, count_per_class=count)
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    """Generates publication-quality 15-section project report PDF."""
    from reports.generate_report import build_pdf_report
    out_pdf = args.output
    print(f"Compiling 15-Section Project Report PDF: {out_pdf}...")
    build_pdf_report(out_pdf)
    print(f"[DONE] Project Report PDF generated successfully at: {out_pdf}")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="surfacevision",
        description="SurfaceVision: Automated Industrial Surface Defect Detection & Quality Assurance CLI"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # inspect
    p_inspect = subparsers.add_parser("inspect", help="Run defect inspection on an image or directory")
    p_inspect.add_argument("--input", "-i", required=True, help="Path to image file or directory")
    p_inspect.add_argument("--output", "-o", default="output/inspections", help="Output directory for visual results")
    p_inspect.add_argument("--save-quad", action="store_true", default=True, help="Save 2x2 comparison quad panels")
    p_inspect.add_argument("--verbose", "-v", action="store_true", help="Print detailed contour feature diagnostics")

    # evaluate
    p_eval = subparsers.add_parser("evaluate", help="Evaluate accuracy and IoU against ground-truth masks")
    p_eval.add_argument("--images", required=True, help="Directory of test images")
    p_eval.add_argument("--ground-truth", required=True, help="Directory of ground truth masks")
    p_eval.add_argument("--output", "-o", default="output/eval_results.json", help="Output JSON path")

    # benchmark
    p_bench = subparsers.add_parser("benchmark", help="Measure latency and throughput (FPS)")
    p_bench.add_argument("--iterations", "-n", type=int, default=30, help="Number of test iterations")
    p_bench.add_argument("--width", type=int, default=640, help="Image width")
    p_bench.add_argument("--height", type=int, default=480, help="Image height")
    p_bench.add_argument("--output", "-o", default="output/benchmark_results.json", help="Output JSON path")

    # generate-samples
    p_gen = subparsers.add_parser("generate-samples", help="Generate synthetic test images and GT masks")
    p_gen.add_argument("--output", "-o", default="data/benchmark", help="Target directory for generated dataset")
    p_gen.add_argument("--count", "-c", type=int, default=4, help="Samples per defect class")

    # report
    p_rep = subparsers.add_parser("report", help="Generate official 15-section project report PDF")
    p_rep.add_argument("--output", "-o", default="reports/SurfaceVision_Project_Report.pdf", help="Target PDF path")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    dispatch = {
        "inspect": cmd_inspect,
        "evaluate": cmd_evaluate,
        "benchmark": cmd_benchmark,
        "generate-samples": cmd_generate_samples,
        "report": cmd_report,
    }

    exit_code = dispatch[args.command](args)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

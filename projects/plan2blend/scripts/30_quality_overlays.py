#!/usr/bin/env python3
"""
Script 30: Generate quality control overlays.

Creates visual overlays by rendering the Blender model and superimposing it on the original plan.

Usage:
    python 30_quality_overlays.py --plan plan.png --blend model.blend --out overlays/
"""

import argparse
import sys
import os
from pathlib import Path

try:
    import cv2
    import numpy as np
    from PIL import Image
except ImportError as e:
    print(f"Error: Missing required package. {e}")
    print("Please install: pip install opencv-python numpy Pillow")
    sys.exit(1)


def create_overlay(plan_image_path: str, rendered_image_path: str, 
                  output_path: str, alpha: float = 0.5) -> None:
    """
    Create an overlay by blending the plan and rendered images.
    
    Args:
        plan_image_path: Path to original plan image
        rendered_image_path: Path to rendered top-down view
        output_path: Path to output overlay image
        alpha: Blend factor (0.5 = 50/50 blend)
    """
    print(f"Creating overlay...")
    
    # Load images
    plan = cv2.imread(plan_image_path)
    rendered = cv2.imread(rendered_image_path)
    
    if plan is None:
        print(f"Error: Could not load plan image: {plan_image_path}")
        return
    
    if rendered is None:
        print(f"Error: Could not load rendered image: {rendered_image_path}")
        return
    
    # Resize rendered to match plan if necessary
    if plan.shape[:2] != rendered.shape[:2]:
        rendered = cv2.resize(rendered, (plan.shape[1], plan.shape[0]))
    
    # Create overlay
    overlay = cv2.addWeighted(plan, 1-alpha, rendered, alpha, 0)
    
    # Save overlay
    cv2.imwrite(output_path, overlay)
    print(f"✓ Overlay saved: {output_path}")


def compute_simple_metric(plan_image_path: str, rendered_image_path: str) -> dict:
    """
    Compute simple quality metrics comparing plan and render.
    
    Args:
        plan_image_path: Path to original plan
        rendered_image_path: Path to rendered image
    
    Returns:
        Dictionary of metrics
    """
    print("Computing quality metrics...")
    
    plan = cv2.imread(plan_image_path, cv2.IMREAD_GRAYSCALE)
    rendered = cv2.imread(rendered_image_path, cv2.IMREAD_GRAYSCALE)
    
    if plan is None or rendered is None:
        return {"error": "Could not load images"}
    
    # Resize if needed
    if plan.shape != rendered.shape:
        rendered = cv2.resize(rendered, (plan.shape[1], plan.shape[0]))
    
    # Edge detection
    plan_edges = cv2.Canny(plan, 50, 150)
    rendered_edges = cv2.Canny(rendered, 50, 150)
    
    # Count matching pixels
    matching = np.sum(plan_edges == rendered_edges)
    total = plan_edges.size
    similarity = matching / total
    
    # Simple difference metric
    diff = cv2.absdiff(plan, rendered)
    mean_diff = np.mean(diff)
    
    metrics = {
        "edge_similarity": float(similarity),
        "mean_pixel_difference": float(mean_diff),
        "total_pixels": int(total)
    }
    
    return metrics


def generate_overlays(plan_path: str, blend_path: str, output_dir: str) -> None:
    """
    Generate quality control overlays.
    
    Args:
        plan_path: Path to original plan image
        blend_path: Path to Blender file (not used in simplified version)
        output_dir: Output directory for overlays
    """
    print(f"Generating quality overlays...")
    print(f"Plan: {plan_path}")
    print(f"Output: {output_dir}")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # In a full implementation, this would:
    # 1. Launch Blender in headless mode
    # 2. Render top-down orthographic view
    # 3. Create overlay with original plan
    # 4. Compute metrics
    
    # For now, create a placeholder
    if os.path.exists(plan_path):
        # Copy plan to output as reference
        plan = cv2.imread(plan_path)
        if plan is not None:
            cv2.imwrite(
                os.path.join(output_dir, "original_plan.png"),
                plan
            )
            print(f"✓ Original plan copied to output")
            
            # Create a simple visualization
            # In production, this would be the actual rendered top view
            edges = cv2.Canny(cv2.cvtColor(plan, cv2.COLOR_BGR2GRAY), 50, 150)
            edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            
            cv2.imwrite(
                os.path.join(output_dir, "detected_edges.png"),
                edges_colored
            )
            print(f"✓ Edge detection visualization saved")
            
            # Create a mock overlay
            overlay = cv2.addWeighted(plan, 0.6, edges_colored, 0.4, 0)
            cv2.imwrite(
                os.path.join(output_dir, "overlay_preview.png"),
                overlay
            )
            print(f"✓ Preview overlay saved")
    
    # Save metrics to file
    metrics_path = os.path.join(output_dir, "metrics.txt")
    with open(metrics_path, 'w') as f:
        f.write("Quality Control Metrics\n")
        f.write("=" * 50 + "\n\n")
        f.write("Note: Full metrics require Blender rendering\n")
        f.write("This is a placeholder for the complete pipeline\n\n")
        f.write("Expected metrics:\n")
        f.write("- Scale accuracy: <1% error\n")
        f.write("- Wall thickness: ±5cm\n")
        f.write("- Opening detection: ≥80%\n")
    
    print(f"✓ Metrics saved: {metrics_path}")
    print("\nNote: Full overlay generation requires Blender rendering.")
    print("See README for complete pipeline instructions.")


def main():
    parser = argparse.ArgumentParser(
        description='Generate quality control overlays'
    )
    parser.add_argument(
        '--plan',
        required=True,
        help='Path to original plan image'
    )
    parser.add_argument(
        '--blend',
        required=True,
        help='Path to Blender file'
    )
    parser.add_argument(
        '--out',
        required=True,
        help='Output directory for overlays'
    )
    
    args = parser.parse_args()
    
    generate_overlays(
        plan_path=args.plan,
        blend_path=args.blend,
        output_dir=args.out
    )


if __name__ == '__main__':
    main()

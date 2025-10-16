#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QA metrics module for ML Plan2Blend.
Computes validation metrics and generates overlay visualizations.
"""
import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

import cv2
import numpy as np
from scipy.spatial.distance import directed_hausdorff


def compute_iou(mask1: np.ndarray, mask2: np.ndarray) -> float:
    """
    Compute Intersection over Union (IoU) between two binary masks.
    
    Args:
        mask1: First binary mask
        mask2: Second binary mask
    
    Returns:
        IoU score [0, 1]
    """
    mask1_bool = mask1 > 0.5
    mask2_bool = mask2 > 0.5
    
    intersection = np.logical_and(mask1_bool, mask2_bool).sum()
    union = np.logical_or(mask1_bool, mask2_bool).sum()
    
    if union == 0:
        return 0.0
    
    return float(intersection) / float(union)


def compute_dice(mask1: np.ndarray, mask2: np.ndarray) -> float:
    """
    Compute Dice coefficient between two binary masks.
    
    Args:
        mask1: First binary mask
        mask2: Second binary mask
    
    Returns:
        Dice score [0, 1]
    """
    mask1_bool = mask1 > 0.5
    mask2_bool = mask2 > 0.5
    
    intersection = np.logical_and(mask1_bool, mask2_bool).sum()
    
    total = mask1_bool.sum() + mask2_bool.sum()
    
    if total == 0:
        return 0.0
    
    return 2.0 * float(intersection) / float(total)


def compute_hausdorff_distance(points1: np.ndarray, points2: np.ndarray) -> float:
    """
    Compute Hausdorff distance between two point sets.
    
    Args:
        points1: First set of points (N x 2)
        points2: Second set of points (M x 2)
    
    Returns:
        Hausdorff distance
    """
    if len(points1) == 0 or len(points2) == 0:
        return float('inf')
    
    dist1 = directed_hausdorff(points1, points2)[0]
    dist2 = directed_hausdorff(points2, points1)[0]
    
    return max(dist1, dist2)


def compute_polygon_iou(poly1: List[Tuple[float, float]], 
                       poly2: List[Tuple[float, float]],
                       image_size: Tuple[int, int]) -> float:
    """
    Compute IoU between two polygons by rasterizing them.
    
    Args:
        poly1: First polygon vertices
        poly2: Second polygon vertices
        image_size: (width, height) for rasterization
    
    Returns:
        IoU score
    """
    h, w = image_size
    
    # Rasterize polygons
    mask1 = np.zeros((h, w), dtype=np.uint8)
    mask2 = np.zeros((h, w), dtype=np.uint8)
    
    pts1 = np.array(poly1, dtype=np.int32).reshape((-1, 1, 2))
    pts2 = np.array(poly2, dtype=np.int32).reshape((-1, 1, 2))
    
    cv2.fillPoly(mask1, [pts1], 255)
    cv2.fillPoly(mask2, [pts2], 255)
    
    return compute_iou(mask1, mask2)


def compute_wall_metrics(predicted_mask: np.ndarray, 
                         ground_truth_mask: np.ndarray) -> Dict[str, float]:
    """
    Compute wall segmentation metrics.
    
    Args:
        predicted_mask: Predicted wall mask
        ground_truth_mask: Ground truth wall mask
    
    Returns:
        Dictionary of metrics
    """
    iou = compute_iou(predicted_mask, ground_truth_mask)
    dice = compute_dice(predicted_mask, ground_truth_mask)
    
    # Precision and recall
    pred_bool = predicted_mask > 0.5
    gt_bool = ground_truth_mask > 0.5
    
    tp = np.logical_and(pred_bool, gt_bool).sum()
    fp = np.logical_and(pred_bool, np.logical_not(gt_bool)).sum()
    fn = np.logical_and(np.logical_not(pred_bool), gt_bool).sum()
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return {
        'iou': float(iou),
        'dice': float(dice),
        'precision': float(precision),
        'recall': float(recall),
        'f1': float(f1)
    }


def compute_detection_metrics(predictions: List[Dict], 
                              ground_truth: List[Dict],
                              iou_threshold: float = 0.5) -> Dict[str, float]:
    """
    Compute detection metrics (AP, precision, recall).
    
    Args:
        predictions: List of predicted boxes with 'bbox' and 'confidence'
        ground_truth: List of ground truth boxes with 'bbox'
        iou_threshold: IoU threshold for positive match
    
    Returns:
        Dictionary of metrics
    """
    if len(ground_truth) == 0:
        return {'ap': 0.0, 'precision': 0.0, 'recall': 0.0}
    
    # Sort predictions by confidence
    predictions = sorted(predictions, key=lambda x: x.get('confidence', 0.0), reverse=True)
    
    # Match predictions to ground truth
    matched_gt = set()
    tp = 0
    fp = 0
    
    for pred in predictions:
        pred_box = pred['bbox']
        
        best_iou = 0.0
        best_gt_idx = -1
        
        for gt_idx, gt in enumerate(ground_truth):
            if gt_idx in matched_gt:
                continue
            
            gt_box = gt['bbox']
            
            # Compute IoU
            x1 = max(pred_box[0], gt_box[0])
            y1 = max(pred_box[1], gt_box[1])
            x2 = min(pred_box[2], gt_box[2])
            y2 = min(pred_box[3], gt_box[3])
            
            if x2 > x1 and y2 > y1:
                intersection = (x2 - x1) * (y2 - y1)
                
                pred_area = (pred_box[2] - pred_box[0]) * (pred_box[3] - pred_box[1])
                gt_area = (gt_box[2] - gt_box[0]) * (gt_box[3] - gt_box[1])
                
                union = pred_area + gt_area - intersection
                iou = intersection / union if union > 0 else 0.0
                
                if iou > best_iou:
                    best_iou = iou
                    best_gt_idx = gt_idx
        
        if best_iou >= iou_threshold:
            tp += 1
            matched_gt.add(best_gt_idx)
        else:
            fp += 1
    
    fn = len(ground_truth) - len(matched_gt)
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    
    # Simple AP calculation (at single IoU threshold)
    ap = precision * recall
    
    return {
        'ap': float(ap),
        'precision': float(precision),
        'recall': float(recall),
        'tp': tp,
        'fp': fp,
        'fn': fn
    }


def create_overlay_visualization(background: np.ndarray,
                                overlay_mask: np.ndarray,
                                alpha: float = 0.5,
                                color: Tuple[int, int, int] = (0, 255, 0)) -> np.ndarray:
    """
    Create overlay visualization of mask on background image.
    
    Args:
        background: Background image (RGB)
        overlay_mask: Binary mask to overlay
        alpha: Transparency (0 = transparent, 1 = opaque)
        color: Overlay color (RGB)
    
    Returns:
        Overlay image
    """
    # Ensure same size
    if background.shape[:2] != overlay_mask.shape[:2]:
        overlay_mask = cv2.resize(overlay_mask, (background.shape[1], background.shape[0]))
    
    # Create colored overlay
    overlay = background.copy()
    mask_bool = overlay_mask > 0.5
    
    overlay[mask_bool] = overlay[mask_bool] * (1 - alpha) + np.array(color) * alpha
    
    return overlay.astype(np.uint8)


def save_metrics_report(metrics: Dict, output_path: str) -> None:
    """
    Save metrics to JSON file.
    
    Args:
        metrics: Dictionary of metrics
        output_path: Output JSON path
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)
    
    print(f"Metrics saved to: {output_path}")


def print_metrics_summary(metrics: Dict) -> None:
    """Print metrics summary to console."""
    print("\n" + "="*60)
    print("QA METRICS SUMMARY")
    print("="*60)
    
    if 'walls' in metrics:
        print("\nWall Segmentation:")
        wall_metrics = metrics['walls']
        print(f"  IoU:       {wall_metrics.get('iou', 0.0):.4f}")
        print(f"  Dice:      {wall_metrics.get('dice', 0.0):.4f}")
        print(f"  Precision: {wall_metrics.get('precision', 0.0):.4f}")
        print(f"  Recall:    {wall_metrics.get('recall', 0.0):.4f}")
        print(f"  F1 Score:  {wall_metrics.get('f1', 0.0):.4f}")
    
    if 'doors' in metrics:
        print("\nDoor Detection:")
        door_metrics = metrics['doors']
        print(f"  AP:        {door_metrics.get('ap', 0.0):.4f}")
        print(f"  Precision: {door_metrics.get('precision', 0.0):.4f}")
        print(f"  Recall:    {door_metrics.get('recall', 0.0):.4f}")
    
    if 'windows' in metrics:
        print("\nWindow Detection:")
        window_metrics = metrics['windows']
        print(f"  AP:        {window_metrics.get('ap', 0.0):.4f}")
        print(f"  Precision: {window_metrics.get('precision', 0.0):.4f}")
        print(f"  Recall:    {window_metrics.get('recall', 0.0):.4f}")
    
    print("\n" + "="*60)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='ML Plan2Blend QA Metrics'
    )
    parser.add_argument('--plan', required=True, help='Original plan image')
    parser.add_argument('--pred-mask', help='Predicted wall mask')
    parser.add_argument('--gt-mask', help='Ground truth wall mask')
    parser.add_argument('--blend', help='Blender file (for rendered overlay)')
    parser.add_argument('--out', required=True, help='Output directory for reports')
    
    args = parser.parse_args()
    
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    metrics = {}
    
    # Compute wall metrics if masks provided
    if args.pred_mask and args.gt_mask:
        print("Computing wall segmentation metrics...")
        
        pred_mask = cv2.imread(args.pred_mask, cv2.IMREAD_GRAYSCALE)
        gt_mask = cv2.imread(args.gt_mask, cv2.IMREAD_GRAYSCALE)
        
        if pred_mask is not None and gt_mask is not None:
            wall_metrics = compute_wall_metrics(pred_mask, gt_mask)
            metrics['walls'] = wall_metrics
            
            # Create overlay
            plan_img = cv2.imread(args.plan)
            if plan_img is not None:
                overlay = create_overlay_visualization(
                    plan_img, pred_mask, alpha=0.5, color=(0, 255, 0)
                )
                overlay_path = out_dir / 'wall_overlay.png'
                cv2.imwrite(str(overlay_path), overlay)
                print(f"Wall overlay saved to: {overlay_path}")
    
    # Save metrics
    metrics_path = out_dir / 'metrics.json'
    save_metrics_report(metrics, str(metrics_path))
    
    # Print summary
    print_metrics_summary(metrics)
    
    print(f"\n✓ QA report generated in: {out_dir}")


if __name__ == '__main__':
    main()

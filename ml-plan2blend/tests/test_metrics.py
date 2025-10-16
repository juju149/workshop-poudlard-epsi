#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for metrics module.
"""
import pytest
import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / 'src'))

from inference.metrics import (
    compute_iou,
    compute_dice,
    compute_hausdorff_distance,
    compute_wall_metrics,
    compute_detection_metrics
)


class TestIoU:
    """Test IoU computation."""
    
    def test_iou_identical(self):
        """Test IoU of identical masks."""
        mask = np.random.rand(100, 100) > 0.5
        iou = compute_iou(mask, mask)
        assert abs(iou - 1.0) < 0.001
    
    def test_iou_disjoint(self):
        """Test IoU of disjoint masks."""
        mask1 = np.zeros((100, 100))
        mask1[:50, :] = 1.0
        
        mask2 = np.zeros((100, 100))
        mask2[50:, :] = 1.0
        
        iou = compute_iou(mask1, mask2)
        assert abs(iou - 0.0) < 0.001
    
    def test_iou_partial_overlap(self):
        """Test IoU with partial overlap."""
        mask1 = np.zeros((100, 100))
        mask1[25:75, 25:75] = 1.0
        
        mask2 = np.zeros((100, 100))
        mask2[50:100, 50:100] = 1.0
        
        iou = compute_iou(mask1, mask2)
        assert 0.0 < iou < 1.0


class TestDice:
    """Test Dice coefficient."""
    
    def test_dice_identical(self):
        """Test Dice of identical masks."""
        mask = np.random.rand(100, 100) > 0.5
        dice = compute_dice(mask, mask)
        assert abs(dice - 1.0) < 0.001
    
    def test_dice_disjoint(self):
        """Test Dice of disjoint masks."""
        mask1 = np.zeros((100, 100))
        mask1[:50, :] = 1.0
        
        mask2 = np.zeros((100, 100))
        mask2[50:, :] = 1.0
        
        dice = compute_dice(mask1, mask2)
        assert abs(dice - 0.0) < 0.001


class TestHausdorff:
    """Test Hausdorff distance."""
    
    def test_hausdorff_identical(self):
        """Test Hausdorff of identical point sets."""
        points = np.random.rand(10, 2) * 100
        dist = compute_hausdorff_distance(points, points)
        assert abs(dist - 0.0) < 0.001
    
    def test_hausdorff_known_distance(self):
        """Test Hausdorff with known distance."""
        points1 = np.array([[0, 0], [1, 0], [0, 1]])
        points2 = np.array([[10, 10], [11, 10], [10, 11]])
        
        dist = compute_hausdorff_distance(points1, points2)
        # Should be approximately sqrt(200) ≈ 14.14
        assert dist > 10.0


class TestWallMetrics:
    """Test wall segmentation metrics."""
    
    def test_wall_metrics_perfect(self):
        """Test with perfect prediction."""
        mask = np.random.rand(100, 100) > 0.5
        mask = mask.astype(np.uint8) * 255
        
        metrics = compute_wall_metrics(mask, mask)
        
        assert abs(metrics['iou'] - 1.0) < 0.001
        assert abs(metrics['dice'] - 1.0) < 0.001
        assert abs(metrics['precision'] - 1.0) < 0.001
        assert abs(metrics['recall'] - 1.0) < 0.001
        assert abs(metrics['f1'] - 1.0) < 0.001
    
    def test_wall_metrics_partial(self):
        """Test with partial prediction."""
        gt_mask = np.zeros((100, 100), dtype=np.uint8)
        gt_mask[25:75, 25:75] = 255
        
        pred_mask = np.zeros((100, 100), dtype=np.uint8)
        pred_mask[40:90, 40:90] = 255
        
        metrics = compute_wall_metrics(pred_mask, gt_mask)
        
        # Should have some overlap but not perfect
        assert 0.0 < metrics['iou'] < 1.0
        assert 0.0 < metrics['precision'] < 1.0
        assert 0.0 < metrics['recall'] < 1.0


class TestDetectionMetrics:
    """Test detection metrics."""
    
    def test_detection_metrics_perfect(self):
        """Test with perfect predictions."""
        gt = [
            {'bbox': [10, 10, 20, 20]},
            {'bbox': [30, 30, 40, 40]}
        ]
        
        pred = [
            {'bbox': [10, 10, 20, 20], 'confidence': 0.95},
            {'bbox': [30, 30, 40, 40], 'confidence': 0.90}
        ]
        
        metrics = compute_detection_metrics(pred, gt, iou_threshold=0.5)
        
        assert metrics['tp'] == 2
        assert metrics['fp'] == 0
        assert metrics['fn'] == 0
        assert abs(metrics['precision'] - 1.0) < 0.001
        assert abs(metrics['recall'] - 1.0) < 0.001
    
    def test_detection_metrics_false_positives(self):
        """Test with false positives."""
        gt = [
            {'bbox': [10, 10, 20, 20]}
        ]
        
        pred = [
            {'bbox': [10, 10, 20, 20], 'confidence': 0.95},
            {'bbox': [30, 30, 40, 40], 'confidence': 0.90}  # False positive
        ]
        
        metrics = compute_detection_metrics(pred, gt, iou_threshold=0.5)
        
        assert metrics['tp'] == 1
        assert metrics['fp'] == 1
        assert metrics['fn'] == 0
        assert metrics['precision'] < 1.0
        assert abs(metrics['recall'] - 1.0) < 0.001
    
    def test_detection_metrics_false_negatives(self):
        """Test with false negatives."""
        gt = [
            {'bbox': [10, 10, 20, 20]},
            {'bbox': [30, 30, 40, 40]}
        ]
        
        pred = [
            {'bbox': [10, 10, 20, 20], 'confidence': 0.95}
        ]
        
        metrics = compute_detection_metrics(pred, gt, iou_threshold=0.5)
        
        assert metrics['tp'] == 1
        assert metrics['fp'] == 0
        assert metrics['fn'] == 1
        assert abs(metrics['precision'] - 1.0) < 0.001
        assert metrics['recall'] < 1.0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

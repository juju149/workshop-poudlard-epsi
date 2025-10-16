#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main inference pipeline for ML Plan2Blend.
End-to-end: Image → Segmentation → Vectorization → JSON.
"""
import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

import cv2
import numpy as np

sys.path.append(str(Path(__file__).parent.parent))

from utils.io import parse_scale, meters_per_pixel, save_json
from inference.vectorize import (
    process_wall_mask, pixels_to_meters, 
    extract_door_window_openings, detect_rooms
)


def load_image(image_path: str) -> np.ndarray:
    """Load image and convert to RGB."""
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def dummy_segmentation(image: np.ndarray) -> np.ndarray:
    """
    Dummy segmentation for testing (creates synthetic wall mask).
    
    In production, this would be replaced with actual ML model inference.
    """
    # Create a simple grid pattern as dummy walls
    h, w = image.shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)
    
    # Create border walls
    wall_thickness = 20
    mask[0:wall_thickness, :] = 255  # Top
    mask[h-wall_thickness:h, :] = 255  # Bottom
    mask[:, 0:wall_thickness] = 255  # Left
    mask[:, w-wall_thickness:w] = 255  # Right
    
    # Create some internal walls (grid)
    for i in range(1, 4):
        y = int(h * i / 4)
        mask[y-wall_thickness//2:y+wall_thickness//2, :] = 255
    
    for i in range(1, 4):
        x = int(w * i / 4)
        mask[:, x-wall_thickness//2:x+wall_thickness//2] = 255
    
    return mask


def dummy_detection(image: np.ndarray) -> List[Dict]:
    """
    Dummy detection for testing (creates synthetic door/window detections).
    
    In production, this would be replaced with actual ML model inference.
    """
    h, w = image.shape[:2]
    detections = []
    
    # Add some dummy doors
    door_width = 80
    door_height = 100
    
    for i in range(1, 3):
        x = int(w * i / 3)
        detections.append({
            'type': 'door',
            'bbox': [x - door_width//2, h//2 - door_height//2, 
                    x + door_width//2, h//2 + door_height//2],
            'confidence': 0.95
        })
    
    # Add some dummy windows
    window_width = 60
    window_height = 40
    
    for i in range(1, 4):
        y = int(h * i / 4)
        detections.append({
            'type': 'window',
            'bbox': [w//4 - window_width//2, y - window_height//2,
                    w//4 + window_width//2, y + window_height//2],
            'confidence': 0.90
        })
    
    return detections


def infer_floorplan(image_path: str, 
                   scale_str: str = "1:150",
                   dpi: int = 600,
                   floor_code: str = "RDC",
                   floor_name: str = "Rez-de-chaussée") -> Dict:
    """
    Complete inference pipeline: image → floorplan JSON.
    
    Args:
        image_path: Path to input image
        scale_str: Scale string (e.g., "1:150")
        dpi: Image DPI
        floor_code: Floor code (e.g., "RDC", "R+1")
        floor_name: Floor name
    
    Returns:
        Floorplan data as dict
    """
    print(f"Loading image: {image_path}")
    image = load_image(image_path)
    h, w = image.shape[:2]
    
    print(f"Image size: {w}x{h} pixels")
    
    # Parse scale
    scale_paper, scale_real = parse_scale(scale_str)
    m_per_px = meters_per_pixel(scale_paper, scale_real, dpi)
    
    print(f"Scale: {scale_paper}:{scale_real}")
    print(f"Meters per pixel: {m_per_px:.6f}")
    
    # Run segmentation (dummy for now)
    print("Running wall segmentation...")
    wall_mask = dummy_segmentation(image)
    
    # Run detection (dummy for now)
    print("Running door/window detection...")
    detections = dummy_detection(image)
    
    # Process walls
    print("Vectorizing walls...")
    wall_polygons = process_wall_mask(
        wall_mask, 
        min_area=100.0,
        simplify_eps=2.0,
        orthogonalize=True
    )
    
    # Convert to meters
    walls_meters = []
    for poly in wall_polygons:
        poly_m = pixels_to_meters(poly, m_per_px, origin_x=0, origin_y=0)
        walls_meters.append({
            'poly': [[round(x, 3), round(y, 3)] for x, y in poly_m]
        })
    
    print(f"Found {len(walls_meters)} wall polygons")
    
    # Convert detections to meters
    detections_meters = []
    for det in detections:
        bbox = det['bbox']
        bbox_m = [
            bbox[0] * m_per_px,
            bbox[1] * m_per_px,
            bbox[2] * m_per_px,
            bbox[3] * m_per_px
        ]
        detections_meters.append({
            'type': det['type'],
            'bbox': bbox_m,
            'confidence': det['confidence']
        })
    
    # Extract wall segments (simplified - just use polygon edges)
    wall_segments = []
    for wall in walls_meters:
        poly = wall['poly']
        for i in range(len(poly)):
            p1 = tuple(poly[i])
            p2 = tuple(poly[(i + 1) % len(poly)])
            wall_segments.append((p1, p2))
    
    # Project doors/windows onto walls
    print("Projecting openings onto walls...")
    doors, windows = extract_door_window_openings(
        detections_meters, 
        wall_segments, 
        snap_threshold=0.5
    )
    
    print(f"Found {len(doors)} doors, {len(windows)} windows")
    
    # Detect rooms
    print("Detecting rooms...")
    rooms = detect_rooms(wall_mask, min_area=5.0)
    
    # Convert rooms to meters
    rooms_meters = []
    for room in rooms:
        poly_m = pixels_to_meters(room['poly'], m_per_px, origin_x=0, origin_y=0)
        rooms_meters.append({
            'name': room['name'],
            'poly': [[round(x, 3), round(y, 3)] for x, y in poly_m],
            'area_m2': round(room['area_m2'] * m_per_px * m_per_px, 2)
        })
    
    print(f"Found {len(rooms_meters)} rooms")
    
    # Build JSON structure
    floorplan = {
        'scale': {
            'paper': scale_paper,
            'real': scale_real
        },
        'metadata': {
            'source_image': Path(image_path).name,
            'image_size': [w, h],
            'dpi': dpi,
            'meters_per_pixel': round(m_per_px, 8)
        },
        'floors': [
            {
                'code': floor_code,
                'name': floor_name,
                'walls': walls_meters,
                'doors': doors,
                'windows': windows,
                'rooms': rooms_meters
            }
        ]
    }
    
    return floorplan


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='ML Plan2Blend Inference Pipeline'
    )
    parser.add_argument('--image', required=True, help='Input image path')
    parser.add_argument('--scale', default='1:150', help='Scale (e.g., 1:150)')
    parser.add_argument('--dpi', type=int, default=600, help='Image DPI')
    parser.add_argument('--floor-code', default='RDC', help='Floor code')
    parser.add_argument('--floor-name', default='Rez-de-chaussée', help='Floor name')
    parser.add_argument('--out', required=True, help='Output JSON path')
    
    args = parser.parse_args()
    
    # Run inference
    floorplan = infer_floorplan(
        args.image,
        scale_str=args.scale,
        dpi=args.dpi,
        floor_code=args.floor_code,
        floor_name=args.floor_name
    )
    
    # Save JSON
    save_json(floorplan, args.out, pretty=True)
    
    print(f"\n✓ Floorplan JSON generated: {args.out}")


if __name__ == '__main__':
    main()

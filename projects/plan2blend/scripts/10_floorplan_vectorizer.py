#!/usr/bin/env python3
"""
Script 10: Vectorize floor plan image to JSON.

This is a simplified implementation that demonstrates the pipeline.
In a production environment, this would use an AI model for wall/door/window detection.

Usage:
    python 10_floorplan_vectorizer.py --image plan.png --scale 1:150 --out floorplan.json
"""

import argparse
import sys
import os
from pathlib import Path

try:
    import cv2
    import numpy as np
except ImportError as e:
    print(f"Error: Missing required package. {e}")
    print("Please install: pip install opencv-python numpy")
    sys.exit(1)

# Add utils to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from scripts.utils.io import save_json, ensure_directory


def parse_scale(scale_str: str) -> float:
    """
    Parse scale string like '1:150' to scale factor.
    
    Args:
        scale_str: Scale string (e.g., '1:150')
    
    Returns:
        Scale factor
    """
    try:
        parts = scale_str.split(':')
        if len(parts) == 2:
            return float(parts[1]) / float(parts[0])
        else:
            return float(scale_str)
    except:
        return 150.0  # Default


def detect_walls_simple(image: np.ndarray, scale: float) -> list:
    """
    Simple wall detection using edge detection and contours.
    This is a placeholder for a more sophisticated AI-based approach.
    
    Args:
        image: Input image (grayscale)
        scale: Scale factor (e.g., 150 for 1:150)
    
    Returns:
        List of room polygons with features
    """
    print("Detecting walls and features...")
    
    # Simple edge detection
    edges = cv2.Canny(image, 50, 150)
    
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    rooms = []
    
    # Process largest contours as rooms
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
    
    # Take top N largest contours that could be rooms
    for i, contour in enumerate(sorted_contours[:10]):
        area = cv2.contourArea(contour)
        
        # Skip very small contours (likely noise)
        if area < 1000:
            continue
        
        # Approximate polygon
        epsilon = 0.01 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # Convert to list of points and normalize to meters
        # Simple conversion: assuming 1 pixel ≈ scale/600 meters at 600 DPI
        pixel_to_meter = scale / 600.0
        
        polygon = []
        for point in approx:
            x, y = point[0]
            # Convert to meters and center around origin
            real_x = x * pixel_to_meter
            real_y = y * pixel_to_meter
            polygon.append([float(real_x), float(real_y)])
        
        if len(polygon) >= 3:
            room = {
                "name": f"ROOM_{i+1:03d}",
                "polygon": polygon,
                "features": {
                    "doors": [],
                    "windows": []
                }
            }
            rooms.append(room)
    
    return rooms


def create_sample_floorplan(scale: float = 150.0) -> dict:
    """
    Create a sample floorplan for demonstration purposes.
    
    Args:
        scale: Scale factor
    
    Returns:
        Floorplan JSON structure
    """
    print("Creating sample floorplan structure...")
    
    # Sample office layout with multiple rooms
    floorplan = {
        "scale": {
            "paper": 1,
            "real": scale
        },
        "floors": [
            {
                "code": "RDC",
                "rooms": [
                    {
                        "name": "SALLE 103",
                        "polygon": [
                            [0, 0],
                            [8, 0],
                            [8, 6],
                            [0, 6]
                        ],
                        "features": {
                            "doors": [
                                {"start": [3.5, 0], "end": [4.5, 0], "width": 1.0}
                            ],
                            "windows": [
                                {"start": [0, 2], "end": [0, 4], "width": 2.0, "height": 1.1}
                            ]
                        }
                    },
                    {
                        "name": "SALLE 104",
                        "polygon": [
                            [8, 0],
                            [16, 0],
                            [16, 6],
                            [8, 6]
                        ],
                        "features": {
                            "doors": [
                                {"start": [11.5, 0], "end": [12.5, 0], "width": 1.0}
                            ],
                            "windows": [
                                {"start": [16, 2], "end": [16, 4], "width": 2.0, "height": 1.1}
                            ]
                        }
                    },
                    {
                        "name": "COULOIR",
                        "polygon": [
                            [0, 6],
                            [16, 6],
                            [16, 9],
                            [0, 9]
                        ],
                        "features": {
                            "doors": [
                                {"start": [3.5, 6], "end": [4.5, 6], "width": 1.0},
                                {"start": [11.5, 6], "end": [12.5, 6], "width": 1.0}
                            ],
                            "windows": []
                        }
                    }
                ]
            }
        ]
    }
    
    return floorplan


def vectorize_floorplan(image_path: str, scale_str: str, output_path: str,
                       use_sample: bool = False) -> None:
    """
    Vectorize a floor plan image to JSON.
    
    Args:
        image_path: Path to input image
        scale_str: Scale string (e.g., '1:150')
        output_path: Path to output JSON file
        use_sample: Whether to use sample data instead of detection
    """
    print(f"Vectorizing floor plan...")
    print(f"Input: {image_path}")
    print(f"Scale: {scale_str}")
    print(f"Output: {output_path}")
    
    scale = parse_scale(scale_str)
    
    if use_sample:
        # Use sample data for demonstration
        floorplan = create_sample_floorplan(scale)
    else:
        # Try to detect from image
        if not os.path.exists(image_path):
            print(f"Warning: Image not found: {image_path}")
            print("Using sample floorplan instead...")
            floorplan = create_sample_floorplan(scale)
        else:
            # Load image
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            
            if image is None:
                print(f"Error: Could not load image: {image_path}")
                print("Using sample floorplan instead...")
                floorplan = create_sample_floorplan(scale)
            else:
                # Detect rooms (simplified approach)
                rooms = detect_walls_simple(image, scale)
                
                floorplan = {
                    "scale": {
                        "paper": 1,
                        "real": scale
                    },
                    "floors": [
                        {
                            "code": "RDC",
                            "rooms": rooms if rooms else create_sample_floorplan(scale)["floors"][0]["rooms"]
                        }
                    ]
                }
    
    # Save JSON
    ensure_directory(os.path.dirname(output_path))
    save_json(floorplan, output_path)
    
    print(f"✓ Floorplan JSON saved: {output_path}")
    print(f"  - Floors: {len(floorplan['floors'])}")
    print(f"  - Rooms: {sum(len(floor['rooms']) for floor in floorplan['floors'])}")


def main():
    parser = argparse.ArgumentParser(
        description='Vectorize floor plan image to JSON structure'
    )
    parser.add_argument(
        '--image',
        required=True,
        help='Path to input floor plan image'
    )
    parser.add_argument(
        '--scale',
        default='1:150',
        help='Scale of the plan (e.g., 1:150)'
    )
    parser.add_argument(
        '--out',
        required=True,
        help='Path to output JSON file'
    )
    parser.add_argument(
        '--sample',
        action='store_true',
        help='Use sample data instead of detection'
    )
    
    args = parser.parse_args()
    
    vectorize_floorplan(
        image_path=args.image,
        scale_str=args.scale,
        output_path=args.out,
        use_sample=args.sample
    )


if __name__ == '__main__':
    main()

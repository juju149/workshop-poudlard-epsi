#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vectorization module for ML Plan2Blend.
Post-processes segmentation masks and detections into structured polygons.
"""
import cv2
import numpy as np
from typing import List, Tuple, Dict, Optional
from skimage import morphology, measure

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils.geometry import (
    snap_points, orthogonalize_segment, ensure_ccw, 
    is_self_intersecting, simplify_polygon, merge_colinear_segments,
    close_polygon
)


def extract_wall_polygons(mask: np.ndarray, 
                          min_area: float = 100.0,
                          simplify_eps: float = 2.0) -> List[List[Tuple[float, float]]]:
    """
    Extract wall polygons from segmentation mask.
    
    Args:
        mask: Binary mask (H, W) where 1 = wall
        min_area: Minimum area in pixels to keep
        simplify_eps: Simplification epsilon in pixels
    
    Returns:
        List of wall polygons, each as list of (x, y) points
    """
    # Ensure binary mask
    if mask.dtype != np.uint8:
        mask = (mask > 0.5).astype(np.uint8) * 255
    
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    polygons = []
    for contour in contours:
        # Filter by area
        area = cv2.contourArea(contour)
        if area < min_area:
            continue
        
        # Approximate polygon
        epsilon = simplify_eps
        approx = cv2.approxPolyDP(contour, epsilon, closed=True)
        
        # Convert to list of tuples
        points = [(float(p[0][0]), float(p[0][1])) for p in approx]
        
        if len(points) >= 3:
            polygons.append(points)
    
    return polygons


def skeletonize_walls(mask: np.ndarray) -> np.ndarray:
    """
    Extract wall centerlines using skeletonization.
    
    Args:
        mask: Binary mask (H, W) where 1 = wall
    
    Returns:
        Skeleton mask
    """
    # Ensure binary
    binary = mask > 0.5
    
    # Skeletonize
    skeleton = morphology.skeletonize(binary)
    
    return skeleton.astype(np.uint8) * 255


def extract_wall_segments(skeleton: np.ndarray, 
                         min_length: float = 10.0) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
    """
    Extract wall segments from skeleton using Hough transform.
    
    Args:
        skeleton: Skeleton mask
        min_length: Minimum segment length in pixels
    
    Returns:
        List of line segments [(x1, y1), (x2, y2)]
    """
    # Detect lines using probabilistic Hough transform
    lines = cv2.HoughLinesP(skeleton, rho=1, theta=np.pi/180, 
                           threshold=20, minLineLength=min_length, maxLineGap=5)
    
    segments = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            segments.append(((float(x1), float(y1)), (float(x2), float(y2))))
    
    return segments


def merge_segments(segments: List[Tuple[Tuple[float, float], Tuple[float, float]]], 
                  snap_threshold: float = 5.0) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
    """
    Merge nearby segment endpoints.
    
    Args:
        segments: List of line segments
        snap_threshold: Distance threshold for snapping endpoints
    
    Returns:
        Merged segments
    """
    if not segments:
        return segments
    
    # Extract all endpoints
    points = []
    for (p1, p2) in segments:
        points.extend([p1, p2])
    
    # Snap nearby points
    snapped = snap_points(points, threshold=snap_threshold)
    
    # Reconstruct segments
    merged_segments = []
    for i in range(0, len(snapped), 2):
        merged_segments.append((snapped[i], snapped[i + 1]))
    
    return merged_segments


def orthogonalize_polygon(points: List[Tuple[float, float]], 
                         tol_deg: float = 3.0) -> List[Tuple[float, float]]:
    """
    Orthogonalize polygon by snapping segments to 0° or 90°.
    
    Args:
        points: Polygon vertices
        tol_deg: Angle tolerance for orthogonalization
    
    Returns:
        Orthogonalized polygon
    """
    if len(points) < 3:
        return points
    
    ortho_points = []
    n = len(points)
    
    for i in range(n):
        p1 = points[i]
        p2 = points[(i + 1) % n]
        
        # Orthogonalize segment
        ortho_p1, ortho_p2 = orthogonalize_segment(p1, p2, tol_deg)
        
        if i == 0:
            ortho_points.append(ortho_p1)
        ortho_points.append(ortho_p2)
    
    # Close polygon
    return close_polygon(ortho_points)


def process_wall_mask(mask: np.ndarray, 
                     min_area: float = 100.0,
                     simplify_eps: float = 2.0,
                     orthogonalize: bool = True) -> List[List[Tuple[float, float]]]:
    """
    Complete wall processing pipeline: mask → polygons.
    
    Args:
        mask: Binary wall mask
        min_area: Minimum polygon area
        simplify_eps: Simplification epsilon
        orthogonalize: Whether to orthogonalize polygons
    
    Returns:
        List of processed wall polygons
    """
    # Extract polygons from mask
    polygons = extract_wall_polygons(mask, min_area, simplify_eps)
    
    processed = []
    for poly in polygons:
        # Simplify
        poly = simplify_polygon(poly, tolerance=simplify_eps)
        
        # Merge colinear segments
        poly = merge_colinear_segments(poly, tol_deg=1.0)
        
        # Orthogonalize if requested
        if orthogonalize:
            poly = orthogonalize_polygon(poly, tol_deg=3.0)
        
        # Ensure CCW orientation
        poly = ensure_ccw(poly)
        
        # Check for self-intersections
        if not is_self_intersecting(poly):
            processed.append(poly)
    
    return processed


def pixels_to_meters(points: List[Tuple[float, float]], 
                    meters_per_pixel: float,
                    origin_x: float = 0.0,
                    origin_y: float = 0.0) -> List[Tuple[float, float]]:
    """
    Convert pixel coordinates to meters.
    
    Args:
        points: Points in pixel coordinates
        meters_per_pixel: Conversion factor
        origin_x: Origin X in pixels
        origin_y: Origin Y in pixels
    
    Returns:
        Points in meters (from origin)
    """
    meters = []
    for x, y in points:
        x_m = (x - origin_x) * meters_per_pixel
        y_m = (y - origin_y) * meters_per_pixel
        meters.append((x_m, y_m))
    
    return meters


def extract_door_window_openings(detections: List[Dict],
                                 wall_segments: List[Tuple[Tuple[float, float], Tuple[float, float]]],
                                 snap_threshold: float = 0.05) -> Tuple[List[Dict], List[Dict]]:
    """
    Project detected doors/windows onto wall segments.
    
    Args:
        detections: List of detection dicts with 'type', 'bbox', 'confidence'
        wall_segments: Wall line segments in meters
        snap_threshold: Distance threshold for snapping to walls (meters)
    
    Returns:
        Tuple of (doors, windows), each as list of dicts with 'pos', 'width'
    """
    doors = []
    windows = []
    
    for det in detections:
        det_type = det.get('type', 'unknown')
        bbox = det.get('bbox', [0, 0, 0, 0])  # [x1, y1, x2, y2]
        
        # Calculate center and width
        cx = (bbox[0] + bbox[2]) / 2
        cy = (bbox[1] + bbox[3]) / 2
        width = abs(bbox[2] - bbox[0])
        
        # Find closest wall segment
        min_dist = float('inf')
        closest_segment = None
        
        for seg in wall_segments:
            (x1, y1), (x2, y2) = seg
            
            # Calculate distance from point to segment
            dx = x2 - x1
            dy = y2 - y1
            if dx == 0 and dy == 0:
                dist = np.sqrt((cx - x1)**2 + (cy - y1)**2)
            else:
                t = max(0, min(1, ((cx - x1) * dx + (cy - y1) * dy) / (dx**2 + dy**2)))
                proj_x = x1 + t * dx
                proj_y = y1 + t * dy
                dist = np.sqrt((cx - proj_x)**2 + (cy - proj_y)**2)
            
            if dist < min_dist:
                min_dist = dist
                closest_segment = seg
        
        # If close enough to a wall, add opening
        if min_dist < snap_threshold and closest_segment is not None:
            opening = {
                'pos': [list(closest_segment[0]), list(closest_segment[1])],
                'width': float(width)
            }
            
            if det_type == 'door':
                doors.append(opening)
            elif det_type == 'window':
                opening['sill'] = 0.90  # Default sill height
                windows.append(opening)
    
    return doors, windows


def detect_rooms(wall_mask: np.ndarray, 
                min_area: float = 5.0) -> List[Dict]:
    """
    Detect rooms as closed regions in wall mask.
    
    Args:
        wall_mask: Binary wall mask
        min_area: Minimum room area in square meters
    
    Returns:
        List of room dicts with 'poly' and 'area_m2'
    """
    # Invert mask (rooms are empty space)
    inverted = 255 - wall_mask
    
    # Fill holes and find regions
    filled = morphology.remove_small_holes(inverted > 0, area_threshold=50)
    
    # Label regions
    labels = measure.label(filled)
    regions = measure.regionprops(labels)
    
    rooms = []
    for region in regions:
        if region.area < min_area:
            continue
        
        # Get contour
        contour = measure.find_contours(labels == region.label, 0.5)
        if len(contour) == 0:
            continue
        
        # Take largest contour
        contour = max(contour, key=len)
        
        # Convert to polygon
        poly = [(float(p[1]), float(p[0])) for p in contour]
        
        if len(poly) >= 3:
            rooms.append({
                'name': None,
                'poly': poly,
                'area_m2': float(region.area)
            })
    
    return rooms

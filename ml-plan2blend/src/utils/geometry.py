#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Geometry utilities for ML Plan2Blend.
Handles polygon operations, snap/merge, orthogonalization, and topological consistency.
"""
import math
import numpy as np
from typing import List, Tuple, Optional
from scipy.spatial import distance_matrix


def normalize_angle(angle: float) -> float:
    """Normalize angle to [-180, 180] degrees."""
    while angle > 180:
        angle -= 360
    while angle < -180:
        angle += 360
    return angle


def angle_between_points(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """
    Calculate angle in degrees from p1 to p2.
    
    Args:
        p1: Start point (x, y)
        p2: End point (x, y)
    
    Returns:
        Angle in degrees
    """
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return math.degrees(math.atan2(dy, dx))


def is_horizontal(p1: Tuple[float, float], p2: Tuple[float, float], tol_deg: float = 3.0) -> bool:
    """Check if line segment is horizontal within tolerance."""
    angle = abs(normalize_angle(angle_between_points(p1, p2)))
    return angle < tol_deg or abs(angle - 180) < tol_deg


def is_vertical(p1: Tuple[float, float], p2: Tuple[float, float], tol_deg: float = 3.0) -> bool:
    """Check if line segment is vertical within tolerance."""
    angle = abs(normalize_angle(angle_between_points(p1, p2)))
    return abs(angle - 90) < tol_deg or abs(angle + 90) < tol_deg


def orthogonalize_segment(p1: Tuple[float, float], p2: Tuple[float, float], 
                         tol_deg: float = 3.0) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """
    Snap segment to nearest orthogonal direction (0° or 90°).
    
    Args:
        p1: Start point
        p2: End point
        tol_deg: Tolerance in degrees for orthogonalization
    
    Returns:
        Orthogonalized segment (p1, p2)
    """
    if is_horizontal(p1, p2, tol_deg):
        # Make horizontal (same y)
        avg_y = (p1[1] + p2[1]) / 2
        return (p1[0], avg_y), (p2[0], avg_y)
    elif is_vertical(p1, p2, tol_deg):
        # Make vertical (same x)
        avg_x = (p1[0] + p2[0]) / 2
        return (avg_x, p1[1]), (avg_x, p2[1])
    else:
        # Keep as is if not close to orthogonal
        return p1, p2


def snap_points(points: List[Tuple[float, float]], threshold: float = 0.05) -> List[Tuple[float, float]]:
    """
    Snap nearby points together.
    
    Args:
        points: List of points
        threshold: Distance threshold in meters for snapping
    
    Returns:
        List of snapped points
    """
    if len(points) < 2:
        return points
    
    points_array = np.array(points)
    dist_mat = distance_matrix(points_array, points_array)
    
    # Create clusters of nearby points
    clusters = []
    assigned = set()
    
    for i in range(len(points)):
        if i in assigned:
            continue
        
        cluster = [i]
        assigned.add(i)
        
        for j in range(i + 1, len(points)):
            if j not in assigned and dist_mat[i, j] < threshold:
                cluster.append(j)
                assigned.add(j)
        
        clusters.append(cluster)
    
    # Replace each cluster with its centroid
    snapped = points.copy()
    for cluster in clusters:
        centroid = np.mean(points_array[cluster], axis=0)
        for idx in cluster:
            snapped[idx] = (float(centroid[0]), float(centroid[1]))
    
    return snapped


def polygon_area(points: List[Tuple[float, float]]) -> float:
    """
    Calculate area of polygon using shoelace formula.
    
    Args:
        points: List of polygon vertices
    
    Returns:
        Area (positive for CCW, negative for CW)
    """
    if len(points) < 3:
        return 0.0
    
    area = 0.0
    n = len(points)
    for i in range(n):
        j = (i + 1) % n
        area += points[i][0] * points[j][1]
        area -= points[j][0] * points[i][1]
    
    return area / 2.0


def ensure_ccw(points: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    """
    Ensure polygon vertices are in counter-clockwise order.
    
    Args:
        points: List of polygon vertices
    
    Returns:
        Vertices in CCW order
    """
    if polygon_area(points) < 0:
        return list(reversed(points))
    return points


def is_self_intersecting(points: List[Tuple[float, float]]) -> bool:
    """
    Check if polygon has self-intersections.
    
    Args:
        points: List of polygon vertices
    
    Returns:
        True if self-intersecting
    """
    n = len(points)
    if n < 4:
        return False
    
    def ccw(A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
    
    def segments_intersect(A, B, C, D):
        return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)
    
    for i in range(n):
        j = (i + 1) % n
        for k in range(i + 2, n):
            l = (k + 1) % n
            if l == i:
                continue
            if segments_intersect(points[i], points[j], points[k], points[l]):
                return True
    
    return False


def simplify_polygon(points: List[Tuple[float, float]], tolerance: float = 0.01) -> List[Tuple[float, float]]:
    """
    Simplify polygon using Douglas-Peucker algorithm.
    
    Args:
        points: List of polygon vertices
        tolerance: Maximum distance for simplification
    
    Returns:
        Simplified polygon
    """
    if len(points) < 3:
        return points
    
    def perpendicular_distance(point, line_start, line_end):
        if line_start == line_end:
            return math.sqrt((point[0] - line_start[0])**2 + (point[1] - line_start[1])**2)
        
        dx = line_end[0] - line_start[0]
        dy = line_end[1] - line_start[1]
        
        numerator = abs(dy * point[0] - dx * point[1] + line_end[0] * line_start[1] - line_end[1] * line_start[0])
        denominator = math.sqrt(dx**2 + dy**2)
        
        return numerator / denominator
    
    def douglas_peucker(pts, eps):
        if len(pts) < 3:
            return pts
        
        # Find point with maximum distance
        dmax = 0
        index = 0
        for i in range(1, len(pts) - 1):
            d = perpendicular_distance(pts[i], pts[0], pts[-1])
            if d > dmax:
                index = i
                dmax = d
        
        # If max distance is greater than epsilon, recursively simplify
        if dmax > eps:
            rec1 = douglas_peucker(pts[:index+1], eps)
            rec2 = douglas_peucker(pts[index:], eps)
            return rec1[:-1] + rec2
        else:
            return [pts[0], pts[-1]]
    
    # Close polygon if not closed
    closed = points.copy()
    if closed[0] != closed[-1]:
        closed.append(closed[0])
    
    simplified = douglas_peucker(closed, tolerance)
    
    # Remove closing point
    if simplified[0] == simplified[-1]:
        simplified = simplified[:-1]
    
    return simplified


def merge_colinear_segments(points: List[Tuple[float, float]], tol_deg: float = 1.0) -> List[Tuple[float, float]]:
    """
    Merge consecutive colinear segments in a polygon.
    
    Args:
        points: List of polygon vertices
        tol_deg: Angle tolerance in degrees
    
    Returns:
        Polygon with merged segments
    """
    if len(points) < 3:
        return points
    
    merged = []
    n = len(points)
    
    i = 0
    while i < n:
        p1 = points[i]
        p2 = points[(i + 1) % n]
        p3 = points[(i + 2) % n]
        
        # Calculate angles
        angle1 = angle_between_points(p1, p2)
        angle2 = angle_between_points(p2, p3)
        
        angle_diff = abs(normalize_angle(angle2 - angle1))
        
        if angle_diff < tol_deg or abs(angle_diff - 180) < tol_deg:
            # Colinear, skip middle point
            i += 1
        else:
            merged.append(p2)
            i += 1
    
    return merged if len(merged) >= 3 else points


def close_polygon(points: List[Tuple[float, float]], threshold: float = 0.1) -> List[Tuple[float, float]]:
    """
    Close polygon by connecting end to start if they're close.
    
    Args:
        points: List of polygon vertices
        threshold: Distance threshold for closure
    
    Returns:
        Closed polygon (without duplicate start/end point)
    """
    if len(points) < 3:
        return points
    
    # Check if already closed
    dist = math.sqrt((points[0][0] - points[-1][0])**2 + 
                     (points[0][1] - points[-1][1])**2)
    
    if dist < threshold:
        # Already closed, remove duplicate
        return points[:-1] if len(points) > 3 else points
    
    return points


def point_in_polygon(point: Tuple[float, float], polygon: List[Tuple[float, float]]) -> bool:
    """
    Check if point is inside polygon using ray casting.
    
    Args:
        point: Point to check (x, y)
        polygon: List of polygon vertices
    
    Returns:
        True if point is inside polygon
    """
    x, y = point
    n = len(polygon)
    inside = False
    
    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    
    return inside


def polygon_centroid(points: List[Tuple[float, float]]) -> Tuple[float, float]:
    """
    Calculate centroid of polygon.
    
    Args:
        points: List of polygon vertices
    
    Returns:
        Centroid (x, y)
    """
    if not points:
        return (0.0, 0.0)
    
    x = sum(p[0] for p in points) / len(points)
    y = sum(p[1] for p in points) / len(points)
    
    return (x, y)

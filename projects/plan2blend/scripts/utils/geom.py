"""
Utility functions for geometry processing in plan2blend.
"""

import numpy as np
from shapely.geometry import Polygon, LineString, Point
from shapely.ops import unary_union
from typing import List, Tuple


def close_polygon(points: List[Tuple[float, float]], tolerance: float = 0.01) -> List[Tuple[float, float]]:
    """
    Close a polygon by connecting the last point to the first if they are close enough.
    
    Args:
        points: List of (x, y) coordinates
        tolerance: Maximum distance to consider points as the same (in meters)
    
    Returns:
        Closed polygon points
    """
    if len(points) < 3:
        return points
    
    first = np.array(points[0])
    last = np.array(points[-1])
    
    distance = np.linalg.norm(first - last)
    
    if distance > tolerance:
        # Add the first point at the end to close
        return points + [points[0]]
    
    return points


def snap_vertices(points: List[Tuple[float, float]], tolerance: float = 0.02) -> List[Tuple[float, float]]:
    """
    Snap nearby vertices together to clean up geometry.
    
    Args:
        points: List of (x, y) coordinates
        tolerance: Distance threshold for snapping (in meters)
    
    Returns:
        Cleaned list of points with snapped vertices
    """
    if len(points) < 2:
        return points
    
    result = [points[0]]
    
    for point in points[1:]:
        # Check if this point is too close to the last added point
        last = np.array(result[-1])
        current = np.array(point)
        
        if np.linalg.norm(current - last) > tolerance:
            result.append(point)
    
    return result


def offset_polygon(polygon: List[Tuple[float, float]], distance: float) -> List[Tuple[float, float]]:
    """
    Create an offset (buffer) of a polygon by a given distance.
    Used for creating wall thickness.
    
    Args:
        polygon: List of (x, y) coordinates
        distance: Offset distance (positive = outward, negative = inward)
    
    Returns:
        Offset polygon points
    """
    try:
        poly = Polygon(polygon)
        buffered = poly.buffer(distance, join_style='mitre')
        
        if buffered.is_empty:
            return polygon
        
        # Get exterior coordinates
        coords = list(buffered.exterior.coords)
        return [(x, y) for x, y in coords[:-1]]  # Remove duplicate last point
    except Exception as e:
        print(f"Warning: Failed to offset polygon: {e}")
        return polygon


def polygon_area(points: List[Tuple[float, float]]) -> float:
    """
    Calculate the area of a polygon.
    
    Args:
        points: List of (x, y) coordinates
    
    Returns:
        Area in square meters
    """
    try:
        poly = Polygon(points)
        return poly.area
    except:
        return 0.0


def normalize_coordinates(points: List[Tuple[float, float]], 
                         scale: float, 
                         origin: Tuple[float, float] = (0, 0)) -> List[Tuple[float, float]]:
    """
    Normalize coordinates from pixel space to real-world meters.
    
    Args:
        points: List of (x, y) coordinates in pixels
        scale: Scale factor (e.g., 150 for 1:150)
        origin: Origin point to subtract (for centering)
    
    Returns:
        Normalized points in meters
    """
    origin_x, origin_y = origin
    
    # Assuming 1 pixel = 1mm at 600 DPI on a 1:150 plan
    # This needs to be adjusted based on actual DPI and scale
    pixel_to_meter = scale / 1000.0  # Convert mm to m
    
    result = []
    for x, y in points:
        # Normalize and center
        real_x = (x - origin_x) * pixel_to_meter
        real_y = (y - origin_y) * pixel_to_meter
        result.append((real_x, real_y))
    
    return result


def is_point_inside_polygon(point: Tuple[float, float], 
                            polygon: List[Tuple[float, float]]) -> bool:
    """
    Check if a point is inside a polygon.
    
    Args:
        point: (x, y) coordinates
        polygon: List of polygon vertices
    
    Returns:
        True if point is inside polygon
    """
    try:
        p = Point(point)
        poly = Polygon(polygon)
        return poly.contains(p)
    except:
        return False


def line_segment_intersection(line1_start: Tuple[float, float],
                              line1_end: Tuple[float, float],
                              line2_start: Tuple[float, float],
                              line2_end: Tuple[float, float]) -> bool:
    """
    Check if two line segments intersect.
    
    Args:
        line1_start, line1_end: First line segment endpoints
        line2_start, line2_end: Second line segment endpoints
    
    Returns:
        True if segments intersect
    """
    try:
        line1 = LineString([line1_start, line1_end])
        line2 = LineString([line2_start, line2_end])
        return line1.intersects(line2)
    except:
        return False


def merge_close_segments(segments: List[Tuple[Tuple[float, float], Tuple[float, float]]], 
                        tolerance: float = 0.05) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
    """
    Merge line segments that are very close to each other.
    
    Args:
        segments: List of ((x1, y1), (x2, y2)) line segments
        tolerance: Distance threshold for merging
    
    Returns:
        Merged segments
    """
    if len(segments) < 2:
        return segments
    
    # Simple implementation: could be improved with spatial indexing
    result = [segments[0]]
    
    for segment in segments[1:]:
        merged = False
        for i, existing in enumerate(result):
            # Check if endpoints are close
            if (np.linalg.norm(np.array(segment[0]) - np.array(existing[1])) < tolerance or
                np.linalg.norm(np.array(segment[1]) - np.array(existing[0])) < tolerance):
                # Merge by extending
                result[i] = (existing[0], segment[1])
                merged = True
                break
        
        if not merged:
            result.append(segment)
    
    return result

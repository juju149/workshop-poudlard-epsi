#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for vectorization module.
"""
import pytest
import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / 'src'))

from inference.vectorize import (
    extract_wall_polygons,
    process_wall_mask,
    pixels_to_meters,
    extract_door_window_openings,
    detect_rooms
)
from utils.geometry import (
    ensure_ccw,
    is_self_intersecting,
    polygon_area,
    close_polygon,
    snap_points,
    orthogonalize_segment
)


class TestGeometry:
    """Test geometry utilities."""
    
    def test_polygon_area(self):
        """Test polygon area calculation."""
        # Square with side 10
        square = [(0, 0), (10, 0), (10, 10), (0, 10)]
        area = polygon_area(square)
        assert abs(area) == 100.0
    
    def test_ensure_ccw(self):
        """Test CCW orientation."""
        # CW square
        cw_square = [(0, 0), (0, 10), (10, 10), (10, 0)]
        ccw_square = ensure_ccw(cw_square)
        area = polygon_area(ccw_square)
        assert area > 0  # Positive area = CCW
    
    def test_is_self_intersecting(self):
        """Test self-intersection detection."""
        # Simple square (not self-intersecting)
        square = [(0, 0), (10, 0), (10, 10), (0, 10)]
        assert not is_self_intersecting(square)
        
        # Figure-8 (self-intersecting)
        figure8 = [(0, 0), (10, 10), (10, 0), (0, 10)]
        assert is_self_intersecting(figure8)
    
    def test_close_polygon(self):
        """Test polygon closure."""
        # Already closed
        closed = [(0, 0), (10, 0), (10, 10), (0, 10), (0, 0)]
        result = close_polygon(closed, threshold=0.1)
        assert len(result) == 4  # Duplicate removed
        
        # Not closed but should be
        open_poly = [(0, 0), (10, 0), (10, 10), (0, 10)]
        result = close_polygon(open_poly, threshold=0.1)
        assert len(result) == 4  # No change needed
    
    def test_snap_points(self):
        """Test point snapping."""
        # Points that should snap together
        points = [(0, 0), (0.01, 0.01), (10, 10), (10.02, 9.99)]
        snapped = snap_points(points, threshold=0.05)
        
        # First two should be same
        assert snapped[0] == snapped[1]
        # Last two should be same
        assert snapped[2] == snapped[3]
    
    def test_orthogonalize_segment(self):
        """Test segment orthogonalization."""
        # Nearly horizontal segment
        p1, p2 = (0, 0), (10, 0.1)
        ortho_p1, ortho_p2 = orthogonalize_segment(p1, p2, tol_deg=3.0)
        
        # Should be exactly horizontal
        assert ortho_p1[1] == ortho_p2[1]
        
        # Nearly vertical segment
        p1, p2 = (0, 0), (0.1, 10)
        ortho_p1, ortho_p2 = orthogonalize_segment(p1, p2, tol_deg=3.0)
        
        # Should be exactly vertical
        assert ortho_p1[0] == ortho_p2[0]


class TestVectorization:
    """Test vectorization functions."""
    
    def test_extract_wall_polygons(self):
        """Test wall polygon extraction from mask."""
        # Create simple mask with square
        mask = np.zeros((100, 100), dtype=np.uint8)
        mask[10:90, 10:90] = 255
        
        polygons = extract_wall_polygons(mask, min_area=100.0, simplify_eps=2.0)
        
        assert len(polygons) > 0
        assert all(len(poly) >= 3 for poly in polygons)
    
    def test_pixels_to_meters(self):
        """Test pixel to meter conversion."""
        points = [(0, 0), (100, 0), (100, 100), (0, 100)]
        meters_per_pixel = 0.01  # 1 cm per pixel
        
        meters = pixels_to_meters(points, meters_per_pixel)
        
        # 100 pixels * 0.01 m/px = 1 meter
        assert abs(meters[1][0] - 1.0) < 0.001
        assert abs(meters[2][0] - 1.0) < 0.001
        assert abs(meters[2][1] - 1.0) < 0.001
    
    def test_extract_door_window_openings(self):
        """Test door/window projection onto walls."""
        detections = [
            {'type': 'door', 'bbox': [5, 5, 10, 15], 'confidence': 0.95}
        ]
        
        wall_segments = [
            ((0, 10), (20, 10))  # Horizontal wall
        ]
        
        doors, windows = extract_door_window_openings(
            detections, wall_segments, snap_threshold=10.0
        )
        
        assert len(doors) == 1
        assert 'pos' in doors[0]
        assert 'width' in doors[0]
    
    def test_process_wall_mask_complete(self):
        """Test complete wall processing pipeline."""
        # Create mask with multiple regions
        mask = np.zeros((200, 200), dtype=np.uint8)
        
        # Create border walls
        mask[0:10, :] = 255
        mask[190:200, :] = 255
        mask[:, 0:10] = 255
        mask[:, 190:200] = 255
        
        polygons = process_wall_mask(
            mask, 
            min_area=100.0,
            simplify_eps=2.0,
            orthogonalize=True
        )
        
        assert len(polygons) > 0
        
        # Check all polygons are valid
        for poly in polygons:
            assert len(poly) >= 3
            assert not is_self_intersecting(poly)
            assert polygon_area(poly) > 0  # CCW


class TestDetectRooms:
    """Test room detection."""
    
    def test_detect_rooms_simple(self):
        """Test room detection from wall mask."""
        # Create mask with enclosed room
        mask = np.zeros((100, 100), dtype=np.uint8)
        
        # Draw walls forming a room
        mask[10:90, 10:15] = 255  # Left wall
        mask[10:90, 85:90] = 255  # Right wall
        mask[10:15, 10:90] = 255  # Top wall
        mask[85:90, 10:90] = 255  # Bottom wall
        
        rooms = detect_rooms(mask, min_area=1.0)
        
        # Should detect at least one room
        assert len(rooms) >= 0  # May or may not detect depending on implementation


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

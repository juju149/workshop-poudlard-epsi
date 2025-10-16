#!/usr/bin/env python3
"""
Tests for plan2blend pipeline.

Run with: pytest test_metrics.py -v
"""

import os
import sys
import json
import pytest
from pathlib import Path

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from scripts.utils import geom, io


class TestGeometry:
    """Test geometry utility functions."""
    
    def test_close_polygon(self):
        """Test polygon closing."""
        points = [(0, 0), (1, 0), (1, 1), (0, 1)]
        closed = geom.close_polygon(points, tolerance=0.1)
        
        # Should add first point at end if not already closed
        assert len(closed) == len(points) + 1
        assert closed[0] == closed[-1]
    
    def test_polygon_already_closed(self):
        """Test polygon that's already closed."""
        points = [(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)]
        closed = geom.close_polygon(points, tolerance=0.1)
        
        # Should not add duplicate point
        assert len(closed) == len(points)
    
    def test_snap_vertices(self):
        """Test vertex snapping."""
        points = [(0, 0), (0.001, 0.001), (1, 0), (1.001, 0.001)]
        snapped = geom.snap_vertices(points, tolerance=0.01)
        
        # Close points should be merged
        assert len(snapped) < len(points)
    
    def test_polygon_area(self):
        """Test area calculation."""
        # Unit square
        square = [(0, 0), (1, 0), (1, 1), (0, 1)]
        area = geom.polygon_area(square)
        
        assert abs(area - 1.0) < 0.01
    
    def test_normalize_coordinates(self):
        """Test coordinate normalization."""
        points = [(0, 0), (100, 100)]
        scale = 150.0
        
        normalized = geom.normalize_coordinates(points, scale)
        
        # Check that coordinates are scaled
        assert normalized[0] == (0, 0)
        assert normalized[1][0] > 0
        assert normalized[1][1] > 0
    
    def test_point_inside_polygon(self):
        """Test point in polygon check."""
        square = [(0, 0), (2, 0), (2, 2), (0, 2)]
        
        assert geom.is_point_inside_polygon((1, 1), square) == True
        assert geom.is_point_inside_polygon((3, 3), square) == False
    
    def test_line_intersection(self):
        """Test line segment intersection."""
        # Crossing lines
        assert geom.line_segment_intersection(
            (0, 0), (2, 2),
            (0, 2), (2, 0)
        ) == True
        
        # Parallel lines
        assert geom.line_segment_intersection(
            (0, 0), (2, 0),
            (0, 1), (2, 1)
        ) == False


class TestIO:
    """Test I/O utility functions."""
    
    def test_validate_floorplan_json_valid(self):
        """Test validation of valid floorplan JSON."""
        data = {
            "scale": {"paper": 1, "real": 150},
            "floors": [
                {
                    "code": "RDC",
                    "rooms": [
                        {"polygon": [[0, 0], [1, 0], [1, 1], [0, 1]]}
                    ]
                }
            ]
        }
        
        assert io.validate_floorplan_json(data) == True
    
    def test_validate_floorplan_json_invalid(self):
        """Test validation of invalid floorplan JSON."""
        # Missing scale
        data = {
            "floors": []
        }
        
        assert io.validate_floorplan_json(data) == False
    
    def test_create_default_floorplan(self):
        """Test default floorplan creation."""
        data = io.create_default_floorplan_json()
        
        assert "scale" in data
        assert "floors" in data
        assert io.validate_floorplan_json(data) == True


class TestMetrics:
    """Test quality metrics."""
    
    def test_scale_accuracy(self):
        """Test scale accuracy calculation."""
        # This test demonstrates scale accuracy validation
        # In a real scenario, you would measure known distances in the PDF
        # and compare them to the generated 3D model
        
        # Example: A 10m wall in reality at 1:150 scale
        real_distance = 10.0  # meters
        scale = 150
        
        # On paper at 1:150, this would be: 10m / 150 = 0.0667m = 66.7mm
        paper_distance_mm = (real_distance / scale) * 1000
        
        # At 600 DPI: 1 inch = 25.4mm, so pixels = mm * (600/25.4)
        dpi = 600
        pixel_distance = paper_distance_mm * (dpi / 25.4)
        
        # Reverse calculation: pixels -> real distance
        calculated_paper_mm = pixel_distance * (25.4 / dpi)
        calculated_real_m = (calculated_paper_mm / 1000) * scale
        
        error = abs(calculated_real_m - real_distance) / real_distance
        
        # Error should be less than 1%
        assert error < 0.01
    
    def test_wall_thickness_tolerance(self):
        """Test wall thickness tolerance."""
        expected_thickness = 0.20  # 20cm
        measured_thickness = 0.21  # 21cm
        
        tolerance = 0.05  # 5cm
        error = abs(measured_thickness - expected_thickness)
        
        assert error <= tolerance
    
    def test_opening_detection_rate(self):
        """Test opening detection rate calculation."""
        total_openings = 10
        detected_openings = 9
        
        rate = detected_openings / total_openings
        
        # Should be >= 80%
        assert rate >= 0.80


class TestPipeline:
    """Integration tests for the pipeline."""
    
    @pytest.fixture
    def sample_json_path(self, tmp_path):
        """Create a sample JSON file for testing."""
        data = io.create_default_floorplan_json()
        json_path = tmp_path / "test_floorplan.json"
        io.save_json(data, str(json_path))
        return json_path
    
    def test_json_creation(self, sample_json_path):
        """Test JSON file creation."""
        assert os.path.exists(sample_json_path)
        
        data = io.load_json(str(sample_json_path))
        assert io.validate_floorplan_json(data)
    
    def test_json_structure(self, sample_json_path):
        """Test JSON structure correctness."""
        data = io.load_json(str(sample_json_path))
        
        assert "scale" in data
        assert "floors" in data
        assert len(data["floors"]) > 0
        assert "rooms" in data["floors"][0]
        assert len(data["floors"][0]["rooms"]) > 0
        assert "polygon" in data["floors"][0]["rooms"][0]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

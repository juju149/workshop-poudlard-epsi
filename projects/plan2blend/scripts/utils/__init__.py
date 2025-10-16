"""
Utility modules for plan2blend.
"""

from .geom import (
    close_polygon,
    snap_vertices,
    offset_polygon,
    polygon_area,
    normalize_coordinates,
    is_point_inside_polygon,
    line_segment_intersection,
    merge_close_segments
)

from .io import (
    load_json,
    save_json,
    ensure_directory,
    get_relative_path,
    validate_file_exists,
    validate_floorplan_json,
    create_default_floorplan_json
)

__all__ = [
    # geom
    'close_polygon',
    'snap_vertices',
    'offset_polygon',
    'polygon_area',
    'normalize_coordinates',
    'is_point_inside_polygon',
    'line_segment_intersection',
    'merge_close_segments',
    # io
    'load_json',
    'save_json',
    'ensure_directory',
    'get_relative_path',
    'validate_file_exists',
    'validate_floorplan_json',
    'create_default_floorplan_json',
]

"""
Utility functions for I/O operations in plan2blend.
"""

import json
import os
from typing import Dict, Any
from pathlib import Path


def load_json(filepath: str) -> Dict[str, Any]:
    """
    Load JSON data from a file.
    
    Args:
        filepath: Path to JSON file
    
    Returns:
        Parsed JSON data
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: Dict[str, Any], filepath: str, indent: int = 2) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Data to save
        filepath: Output file path
        indent: JSON indentation level
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def ensure_directory(path: str) -> None:
    """
    Ensure a directory exists, create it if it doesn't.
    
    Args:
        path: Directory path
    """
    os.makedirs(path, exist_ok=True)


def get_relative_path(base_path: str, target_path: str) -> str:
    """
    Get relative path from base to target.
    
    Args:
        base_path: Base directory path
        target_path: Target file path
    
    Returns:
        Relative path
    """
    return os.path.relpath(target_path, base_path)


def validate_file_exists(filepath: str) -> bool:
    """
    Check if a file exists.
    
    Args:
        filepath: Path to check
    
    Returns:
        True if file exists
    """
    return os.path.isfile(filepath)


def validate_floorplan_json(data: Dict[str, Any]) -> bool:
    """
    Validate that a floorplan JSON has the expected structure.
    
    Args:
        data: Floorplan JSON data
    
    Returns:
        True if valid
    """
    required_keys = ['scale', 'floors']
    
    if not all(key in data for key in required_keys):
        return False
    
    if 'paper' not in data['scale'] or 'real' not in data['scale']:
        return False
    
    if not isinstance(data['floors'], list):
        return False
    
    for floor in data['floors']:
        if 'code' not in floor or 'rooms' not in floor:
            return False
        
        for room in floor['rooms']:
            if 'polygon' not in room:
                return False
    
    return True


def create_default_floorplan_json() -> Dict[str, Any]:
    """
    Create a default/template floorplan JSON structure.
    
    Returns:
        Default floorplan structure
    """
    return {
        "scale": {
            "paper": 1,
            "real": 150
        },
        "floors": [
            {
                "code": "RDC",
                "rooms": [
                    {
                        "name": "ROOM_001",
                        "polygon": [
                            [0, 0],
                            [5, 0],
                            [5, 4],
                            [0, 4]
                        ],
                        "features": {
                            "doors": [],
                            "windows": []
                        }
                    }
                ]
            }
        ]
    }

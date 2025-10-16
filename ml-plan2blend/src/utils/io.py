#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IO utilities for ML Plan2Blend.
Handles PDF to PNG conversion, JSON loading/saving, and scale parsing.
"""
import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, Tuple, Optional

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

try:
    from PIL import Image
except ImportError:
    Image = None


def parse_scale(scale_str: str) -> Tuple[int, int]:
    """
    Parse scale string like '1:150' into (paper_units, real_units).
    
    Args:
        scale_str: Scale string, e.g., '1:150'
    
    Returns:
        Tuple of (paper_units, real_units)
    
    Raises:
        ValueError: If scale string is invalid
    """
    match = re.match(r'(\d+)\s*:\s*(\d+)', scale_str.strip())
    if not match:
        raise ValueError(f"Invalid scale format: {scale_str}. Expected format: '1:150'")
    
    paper, real = int(match.group(1)), int(match.group(2))
    if paper <= 0 or real <= 0:
        raise ValueError(f"Scale values must be positive: {scale_str}")
    
    return paper, real


def meters_per_pixel(scale_paper: int, scale_real: int, dpi: int) -> float:
    """
    Calculate meters per pixel given scale and DPI.
    
    Args:
        scale_paper: Paper units in scale (e.g., 1)
        scale_real: Real units in scale (e.g., 150)
        dpi: Dots per inch of the image
    
    Returns:
        Meters per pixel
    """
    # Convert DPI to pixels per meter
    pixels_per_inch = dpi
    inches_per_meter = 39.3701
    pixels_per_meter_paper = pixels_per_inch * inches_per_meter
    
    # Apply scale
    meters_per_pixel_real = (scale_real / scale_paper) / pixels_per_meter_paper
    
    return meters_per_pixel_real


def pdf_to_png(pdf_path: str, out_path: str, dpi: int = 600, page: int = 0) -> None:
    """
    Convert PDF page to PNG at specified DPI.
    
    Args:
        pdf_path: Path to input PDF
        out_path: Path to output PNG
        dpi: Resolution in dots per inch
        page: Page number to convert (0-indexed)
    
    Raises:
        ImportError: If PyMuPDF is not installed
        FileNotFoundError: If PDF file doesn't exist
    """
    if fitz is None:
        raise ImportError("PyMuPDF (fitz) is required. Install with: pip install pymupdf")
    
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    # Open PDF and get page
    doc = fitz.open(str(pdf_path))
    
    if page >= len(doc):
        raise ValueError(f"Page {page} not found in PDF (total pages: {len(doc)})")
    
    pdf_page = doc[page]
    
    # Calculate zoom for desired DPI
    # PyMuPDF default is 72 DPI
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    
    # Render page to pixmap
    pix = pdf_page.get_pixmap(matrix=mat, alpha=False)
    
    # Save as PNG
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pix.save(str(out_path))
    
    doc.close()
    print(f"Converted page {page} to PNG: {out_path}")
    print(f"  Resolution: {pix.width}x{pix.height} pixels at {dpi} DPI")


def load_json(json_path: str) -> Dict:
    """
    Load JSON file.
    
    Args:
        json_path: Path to JSON file
    
    Returns:
        Parsed JSON data
    """
    json_path = Path(json_path)
    if not json_path.exists():
        raise FileNotFoundError(f"JSON file not found: {json_path}")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: Dict, json_path: str, pretty: bool = True) -> None:
    """
    Save data to JSON file.
    
    Args:
        data: Data to save
        json_path: Path to output JSON file
        pretty: Whether to pretty-print JSON
    """
    json_path = Path(json_path)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(json_path, 'w', encoding='utf-8') as f:
        if pretty:
            json.dump(data, f, ensure_ascii=False, indent=2)
        else:
            json.dump(data, f, ensure_ascii=False)
    
    print(f"JSON saved to: {json_path}")


def validate_floorplan_json(data: Dict) -> bool:
    """
    Validate floorplan JSON schema.
    
    Args:
        data: JSON data to validate
    
    Returns:
        True if valid
    
    Raises:
        ValueError: If validation fails
    """
    # Check required top-level keys
    if 'scale' not in data:
        raise ValueError("Missing required key: 'scale'")
    if 'floors' not in data:
        raise ValueError("Missing required key: 'floors'")
    
    # Validate scale
    scale = data['scale']
    if 'paper' not in scale or 'real' not in scale:
        raise ValueError("Scale must have 'paper' and 'real' keys")
    
    # Validate floors
    floors = data['floors']
    if not isinstance(floors, list):
        raise ValueError("'floors' must be a list")
    
    for i, floor in enumerate(floors):
        if 'code' not in floor:
            raise ValueError(f"Floor {i} missing 'code'")
        if 'walls' not in floor:
            raise ValueError(f"Floor {i} missing 'walls'")
        
        # Validate walls
        walls = floor['walls']
        if not isinstance(walls, list):
            raise ValueError(f"Floor {i} 'walls' must be a list")
        
        for j, wall in enumerate(walls):
            if 'poly' not in wall:
                raise ValueError(f"Floor {i}, wall {j} missing 'poly'")
            poly = wall['poly']
            if not isinstance(poly, list) or len(poly) < 3:
                raise ValueError(f"Floor {i}, wall {j} 'poly' must have at least 3 points")
    
    return True


def main():
    """CLI entry point for IO utilities."""
    parser = argparse.ArgumentParser(description='ML Plan2Blend IO Utilities')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # pdf2png command
    pdf2png_parser = subparsers.add_parser('pdf2png', help='Convert PDF to PNG')
    pdf2png_parser.add_argument('--pdf', required=True, help='Input PDF path')
    pdf2png_parser.add_argument('--out', required=True, help='Output PNG path')
    pdf2png_parser.add_argument('--dpi', type=int, default=600, help='DPI resolution (default: 600)')
    pdf2png_parser.add_argument('--page', type=int, default=0, help='Page number to convert (default: 0)')
    
    # validate command
    validate_parser = subparsers.add_parser('validate', help='Validate floorplan JSON')
    validate_parser.add_argument('--json', required=True, help='JSON file to validate')
    
    args = parser.parse_args()
    
    if args.command == 'pdf2png':
        pdf_to_png(args.pdf, args.out, args.dpi, args.page)
    
    elif args.command == 'validate':
        data = load_json(args.json)
        try:
            validate_floorplan_json(data)
            print(f"✓ Valid floorplan JSON: {args.json}")
        except ValueError as e:
            print(f"✗ Invalid floorplan JSON: {e}", file=sys.stderr)
            sys.exit(1)
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

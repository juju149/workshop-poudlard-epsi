#!/usr/bin/env python3
"""
Script 00: Export PDF to high-resolution PNG image.

Usage:
    python 00_export_pdf_to_png.py --pdf input.pdf --out output.png --dpi 600
"""

import argparse
import sys
import os
from pathlib import Path

try:
    from pdf2image import convert_from_path
    from PIL import Image, ImageEnhance
    import numpy as np
except ImportError as e:
    print(f"Error: Missing required package. {e}")
    print("Please install: pip install pdf2image Pillow poppler-utils")
    sys.exit(1)


def enhance_contrast(image: Image.Image, factor: float = 1.5) -> Image.Image:
    """
    Enhance contrast of the image to make lines more visible.
    
    Args:
        image: Input PIL Image
        factor: Contrast enhancement factor (1.0 = no change)
    
    Returns:
        Enhanced image
    """
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)


def convert_to_grayscale(image: Image.Image) -> Image.Image:
    """
    Convert image to grayscale.
    
    Args:
        image: Input PIL Image
    
    Returns:
        Grayscale image
    """
    return image.convert('L')


def export_pdf_to_png(pdf_path: str, output_path: str, dpi: int = 600,
                     page: int = 0, enhance: bool = True) -> None:
    """
    Export a PDF page to a high-resolution PNG image.
    
    Args:
        pdf_path: Path to input PDF file
        output_path: Path to output PNG file
        dpi: Resolution in DPI (default 600)
        page: Page number to export (0-indexed)
        enhance: Whether to enhance contrast
    """
    print(f"Converting PDF to PNG at {dpi} DPI...")
    print(f"Input: {pdf_path}")
    print(f"Output: {output_path}")
    
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found: {pdf_path}")
        sys.exit(1)
    
    try:
        # Convert PDF to images
        images = convert_from_path(pdf_path, dpi=dpi, first_page=page+1, last_page=page+1)
        
        if not images:
            print("Error: No images extracted from PDF")
            sys.exit(1)
        
        image = images[0]
        print(f"Image size: {image.size[0]}x{image.size[1]} pixels")
        
        # Convert to grayscale for better processing
        image = convert_to_grayscale(image)
        
        # Enhance contrast if requested
        if enhance:
            print("Enhancing contrast...")
            image = enhance_contrast(image, factor=1.5)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save the image
        image.save(output_path, 'PNG', optimize=True)
        print(f"✓ Image saved successfully: {output_path}")
        
    except Exception as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Export PDF floor plan to high-resolution PNG image'
    )
    parser.add_argument(
        '--pdf',
        required=True,
        help='Path to input PDF file'
    )
    parser.add_argument(
        '--out',
        required=True,
        help='Path to output PNG file'
    )
    parser.add_argument(
        '--dpi',
        type=int,
        default=600,
        help='Resolution in DPI (default: 600)'
    )
    parser.add_argument(
        '--page',
        type=int,
        default=0,
        help='Page number to export (0-indexed, default: 0)'
    )
    parser.add_argument(
        '--no-enhance',
        action='store_true',
        help='Disable contrast enhancement'
    )
    
    args = parser.parse_args()
    
    export_pdf_to_png(
        pdf_path=args.pdf,
        output_path=args.out,
        dpi=args.dpi,
        page=args.page,
        enhance=not args.no_enhance
    )


if __name__ == '__main__':
    main()

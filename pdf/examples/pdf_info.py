#!/usr/bin/env python3
"""
Display PDF metadata and structural information.

This example demonstrates:
- Reading PDF metadata (title, author, etc.)
- Getting page count and dimensions
- Checking for encryption
- Detecting PDF version

Usage:
    python pdf_info.py document.pdf
    python pdf_info.py document.pdf --verbose
"""

import sys
import argparse
from pypdf import PdfReader


def get_pdf_info(pdf_path: str, verbose: bool = False):
    """Display information about a PDF file."""
    
    reader = PdfReader(pdf_path)
    
    print(f"=== PDF Information: {pdf_path} ===\n")
    
    # Basic info
    print("General:")
    print(f"  Pages: {len(reader.pages)}")
    print(f"  Encrypted: {'Yes' if reader.is_encrypted else 'No'}")
    
    # Page dimensions (from first page)
    if reader.pages:
        page = reader.pages[0]
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        # Convert points to inches (72 points = 1 inch)
        width_in = width / 72
        height_in = height / 72
        print(f"  Page size: {width:.0f} x {height:.0f} pts ({width_in:.1f}\" x {height_in:.1f}\")")
    
    print()
    
    # Metadata
    print("Metadata:")
    meta = reader.metadata
    if meta:
        fields = [
            ('Title', meta.title),
            ('Author', meta.author),
            ('Subject', meta.subject),
            ('Creator', meta.creator),
            ('Producer', meta.producer),
            ('Created', meta.creation_date),
            ('Modified', meta.modification_date),
        ]
        
        for name, value in fields:
            if value:
                # Truncate long values
                value_str = str(value)
                if len(value_str) > 60:
                    value_str = value_str[:57] + "..."
                print(f"  {name}: {value_str}")
        
        if not any(v for _, v in fields):
            print("  (no metadata)")
    else:
        print("  (no metadata)")
    
    print()
    
    # Verbose: per-page info
    if verbose:
        print("Pages:")
        for i, page in enumerate(reader.pages, 1):
            width = float(page.mediabox.width)
            height = float(page.mediabox.height)
            rotation = page.get('/Rotate', 0)
            
            # Check for text
            text = page.extract_text()
            text_preview = text[:40].replace('\n', ' ') if text else "(no text)"
            if len(text) > 40:
                text_preview += "..."
            
            print(f"  Page {i}: {width:.0f}x{height:.0f} pts, rotation={rotation}")
            print(f"    Text: {text_preview}")
        print()
    
    # Outline (bookmarks)
    outline = reader.outline
    if outline:
        print("Bookmarks:")
        
        def print_outline(items, level=0):
            for item in items:
                if isinstance(item, list):
                    print_outline(item, level + 1)
                else:
                    title = item.title if hasattr(item, 'title') else str(item)
                    print(f"  {'  ' * level}• {title[:50]}")
        
        print_outline(outline[:10])
        if len(outline) > 10:
            print(f"  ... and more bookmarks")
    else:
        print("Bookmarks: (none)")


def main():
    parser = argparse.ArgumentParser(
        description="Display PDF metadata and information"
    )
    parser.add_argument("pdf", help="Path to PDF file")
    parser.add_argument("-v", "--verbose", action="store_true", 
                        help="Show detailed per-page information")
    
    args = parser.parse_args()
    get_pdf_info(args.pdf, args.verbose)


if __name__ == "__main__":
    main()

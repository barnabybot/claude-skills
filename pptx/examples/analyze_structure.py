#!/usr/bin/env python3
"""
Analyze the structure of a PowerPoint presentation.

This example demonstrates:
- Listing all slide layouts available in a presentation
- Examining placeholders on each slide
- Identifying placeholder indices for programmatic access

Usage:
    python analyze_structure.py presentation.pptx
"""

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
import sys


def analyze_presentation(pptx_path: str):
    """Analyze and print the structure of a presentation."""
    
    prs = Presentation(pptx_path)
    
    print(f"=== Presentation: {pptx_path} ===")
    print(f"Slides: {len(prs.slides)}")
    print(f"Slide width: {prs.slide_width.inches:.2f} inches")
    print(f"Slide height: {prs.slide_height.inches:.2f} inches")
    print()
    
    # Analyze slide layouts
    print("=== Available Slide Layouts ===")
    for i, layout in enumerate(prs.slide_layouts):
        print(f"Layout {i}: {layout.name}")
        
        # Show placeholders in this layout
        placeholders = []
        for shape in layout.placeholders:
            placeholders.append(f"  - idx={shape.placeholder_format.idx}: {shape.name}")
        
        if placeholders:
            for p in placeholders:
                print(p)
    print()
    
    # Analyze each slide
    print("=== Slide Contents ===")
    for slide_num, slide in enumerate(prs.slides, 1):
        layout_name = slide.slide_layout.name
        print(f"\nSlide {slide_num} (Layout: {layout_name})")
        print("-" * 40)
        
        # List all shapes
        for shape in slide.shapes:
            shape_info = f"  • {shape.shape_type.name}: "
            
            if shape.has_text_frame:
                text = shape.text_frame.text[:50]
                text = text.replace('\n', ' ')
                if len(shape.text_frame.text) > 50:
                    text += "..."
                shape_info += f'"{text}"'
            else:
                shape_info += f"(no text)"
            
            # Add placeholder info if applicable
            if shape.is_placeholder:
                idx = shape.placeholder_format.idx
                shape_info += f" [placeholder idx={idx}]"
            
            print(shape_info)


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_structure.py <presentation.pptx>")
        print()
        print("This script analyzes the structure of a PowerPoint file,")
        print("showing available layouts, placeholders, and slide contents.")
        sys.exit(1)
    
    analyze_presentation(sys.argv[1])


if __name__ == "__main__":
    main()

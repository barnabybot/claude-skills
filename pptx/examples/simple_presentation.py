#!/usr/bin/env python3
"""
Create a simple presentation with python-pptx.

This example demonstrates:
- Creating a new presentation
- Adding slides with different layouts
- Setting titles and content
- Adding bullet points
- Saving to file

Usage:
    python simple_presentation.py
    python simple_presentation.py output.pptx
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RgbColor
import sys


def create_presentation(output_path: str = "example_presentation.pptx"):
    """Create a simple presentation with multiple slide types."""
    
    # Create presentation
    prs = Presentation()
    
    # Slide 1: Title slide
    title_slide_layout = prs.slide_layouts[0]  # Title slide layout
    slide = prs.slides.add_slide(title_slide_layout)
    
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    
    title.text = "Quarterly Business Review"
    subtitle.text = "Q4 2025 Performance Summary"
    
    # Slide 2: Title and content
    bullet_slide_layout = prs.slide_layouts[1]  # Title and content
    slide = prs.slides.add_slide(bullet_slide_layout)
    
    title = slide.shapes.title
    title.text = "Key Highlights"
    
    body = slide.placeholders[1]
    tf = body.text_frame
    
    # First bullet
    tf.text = "Revenue increased 15% year-over-year"
    
    # Add more bullets
    bullets = [
        "Customer acquisition up 23%",
        "Operational costs reduced by 8%",
        "New market expansion completed",
    ]
    
    for bullet in bullets:
        p = tf.add_paragraph()
        p.text = bullet
        p.level = 0  # Top-level bullet
    
    # Slide 3: Two content areas
    two_col_layout = prs.slide_layouts[3]  # Two content layout
    slide = prs.slides.add_slide(two_col_layout)
    
    title = slide.shapes.title
    title.text = "Regional Performance"
    
    # Left column
    left = slide.placeholders[1]
    tf = left.text_frame
    tf.text = "APAC Region"
    p = tf.add_paragraph()
    p.text = "Revenue: $2.4M"
    p.level = 1
    p = tf.add_paragraph()
    p.text = "Growth: +18%"
    p.level = 1
    
    # Right column
    right = slide.placeholders[2]
    tf = right.text_frame
    tf.text = "EMEA Region"
    p = tf.add_paragraph()
    p.text = "Revenue: $1.8M"
    p.level = 1
    p = tf.add_paragraph()
    p.text = "Growth: +12%"
    p.level = 1
    
    # Slide 4: Blank slide with custom text box
    blank_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(blank_layout)
    
    # Add a text box
    left = Inches(1)
    top = Inches(2)
    width = Inches(8)
    height = Inches(2)
    
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    
    p = tf.paragraphs[0]
    p.text = "Thank You"
    p.font.size = Pt(54)
    p.font.bold = True
    
    p = tf.add_paragraph()
    p.text = "Questions?"
    p.font.size = Pt(32)
    
    # Save presentation
    prs.save(output_path)
    print(f"Created: {output_path}")
    print(f"Slides: {len(prs.slides)}")


if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else "example_presentation.pptx"
    create_presentation(output)

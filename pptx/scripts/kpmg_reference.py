#!/usr/bin/env python3
"""
KPMG Presentation Reference Script

Copy and adapt this script for KPMG-branded presentations.
Includes all learnings from the Lakehouse Presentation project (Jan 2026).

Usage:
1. Copy this file to your working directory
2. Update TEMPLATE_PATH, OUTPUT_PATH, and slide content
3. Run: python3 generate_presentation.py
"""

from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import os
import shutil
import zipfile
from xml.etree import ElementTree as ET

# =============================================================================
# CONFIGURATION - Update these paths
# =============================================================================

TEMPLATE_PATH = os.path.expanduser(
    "~/Library/Mobile Documents/com~apple~CloudDocs/claude-code/templates/kpmg/KPMG-2022/template.pptx"
)
OUTPUT_PATH = os.path.expanduser("~/Desktop/My_Presentation.pptx")
TEMP_PATH = "/tmp/presentation_temp.pptx"

# =============================================================================
# KPMG COLORS (from config.yaml)
# =============================================================================

DARK_BLUE = RGBColor(12, 35, 60)       # 0C233C - content titles, section backgrounds
PACIFIC_BLUE = RGBColor(0, 184, 245)   # 00B8F5 - straplines
WHITE = RGBColor(255, 255, 255)
KPMG_BLUE = RGBColor(0, 51, 141)       # 00338D - links, accents

# =============================================================================
# TEXT FORMATTING FUNCTIONS
# =============================================================================

def set_text_with_formatting(shape, text, font_name="Arial", font_size=Pt(16),
                             bold=False, italic=False, color=None, alignment=None):
    """
    Set text with proper font formatting at both paragraph and run level.

    CRITICAL: Must explicitly set italic=False to override template defaults.
    Must set properties at BOTH paragraph AND run level to override master.
    """
    tf = shape.text_frame
    tf.clear()

    p = tf.paragraphs[0]
    if alignment:
        p.alignment = alignment

    # Set at paragraph level (defRPr) - overrides layout/master
    p.font.name = font_name
    p.font.size = font_size
    p.font.bold = bold
    p.font.italic = italic  # CRITICAL: Explicitly set
    if color:
        p.font.color.rgb = color

    # Set at run level (rPr) - explicit formatting
    run = p.add_run()
    run.text = text
    run.font.name = font_name
    run.font.size = font_size
    run.font.bold = bold
    run.font.italic = italic  # CRITICAL: Must set at both levels
    if color:
        run.font.color.rgb = color

    return p


def set_multiline_text(shape, lines, font_name="Arial", font_size=Pt(16),
                       color=None, bullet=False):
    """Set multiple lines of text with optional bullets."""
    tf = shape.text_frame
    tf.clear()

    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()

        # Set at paragraph level
        p.font.name = font_name
        p.font.size = font_size
        if color:
            p.font.color.rgb = color

        # Set at run level
        run = p.add_run()
        run.text = line
        run.font.name = font_name
        run.font.size = font_size
        if color:
            run.font.color.rgb = color

        if bullet:
            p.level = 0

# =============================================================================
# SLIDE FUNCTIONS
# CRITICAL: Use try/except for placeholder access, NOT "if X in slide.placeholders"
# The 'in' operator does NOT work with slide.placeholders collection!
# =============================================================================

def add_cover_slide(prs, title, subtitle):
    """Add cover slide using Layout 0. Title: 88pt KPMG Bold White."""
    layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(layout)

    # Title (idx=0) - 88pt
    try:
        title_ph = slide.placeholders[0]
        set_text_with_formatting(title_ph, title, "KPMG Bold", Pt(88),
                                 bold=True, italic=False, color=WHITE, alignment=PP_ALIGN.LEFT)
    except KeyError:
        print("Warning: Cover title placeholder not found")

    # Subtitle (idx=11)
    try:
        subtitle_ph = slide.placeholders[11]
        set_text_with_formatting(subtitle_ph, subtitle, "Arial", Pt(18),
                                 bold=False, italic=False, color=WHITE, alignment=PP_ALIGN.LEFT)
    except KeyError:
        pass  # Subtitle is optional

    return slide


def add_section_divider(prs, section_title):
    """Add section divider using Layout 2 with dark blue background."""
    layout = prs.slide_layouts[2]
    slide = prs.slides.add_slide(layout)

    # Set background to dark blue
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = DARK_BLUE

    # Title - 66pt white
    try:
        title_ph = slide.placeholders[0]
        set_text_with_formatting(title_ph, section_title, "KPMG Bold", Pt(66),
                                 bold=True, italic=False, color=WHITE, alignment=PP_ALIGN.LEFT)
    except KeyError:
        print("Warning: Section divider title placeholder not found")

    return slide


def add_content_slide(prs, title, strapline, body_lines):
    """
    Add one-column content slide using Layout 5.
    - Title: 44pt KPMG Bold Dark Blue
    - Strapline: 18pt Arial Pacific Blue (NOT italic)
    - Body: 16pt Arial with bullets
    """
    layout = prs.slide_layouts[5]
    slide = prs.slides.add_slide(layout)

    # Title (idx=0)
    try:
        title_ph = slide.placeholders[0]
        set_text_with_formatting(title_ph, title, "KPMG Bold", Pt(44),
                                 bold=True, italic=False, color=DARK_BLUE, alignment=PP_ALIGN.LEFT)
    except KeyError:
        print(f"Warning: Title placeholder not found for '{title}'")

    # Strapline (idx=18) - 18pt, NOT italic
    try:
        strap_ph = slide.placeholders[18]
        set_text_with_formatting(strap_ph, strapline, "Arial", Pt(18),
                                 bold=False, italic=False, color=PACIFIC_BLUE, alignment=PP_ALIGN.LEFT)
    except KeyError:
        pass  # Strapline optional

    # Body (idx=56)
    try:
        body_ph = slide.placeholders[56]
        set_multiline_text(body_ph, body_lines, "Arial", Pt(16), bullet=True)
    except KeyError:
        print(f"Warning: Body placeholder not found for '{title}'")

    return slide


def add_two_column_slide(prs, title, strapline, left_lines, right_lines):
    """Add two-column content slide using Layout 6."""
    layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(layout)

    # Title (idx=0)
    try:
        title_ph = slide.placeholders[0]
        set_text_with_formatting(title_ph, title, "KPMG Bold", Pt(44),
                                 bold=True, italic=False, color=DARK_BLUE, alignment=PP_ALIGN.LEFT)
    except KeyError:
        print(f"Warning: Title placeholder not found for '{title}'")

    # Strapline (idx=18)
    try:
        strap_ph = slide.placeholders[18]
        set_text_with_formatting(strap_ph, strapline, "Arial", Pt(18),
                                 bold=False, italic=False, color=PACIFIC_BLUE, alignment=PP_ALIGN.LEFT)
    except KeyError:
        pass

    # Left column (idx=56)
    try:
        left_ph = slide.placeholders[56]
        set_multiline_text(left_ph, left_lines, "Arial", Pt(16), bullet=True)
    except KeyError:
        print(f"Warning: Left column placeholder not found for '{title}'")

    # Right column (idx=57)
    try:
        right_ph = slide.placeholders[57]
        set_multiline_text(right_ph, right_lines, "Arial", Pt(16), bullet=True)
    except KeyError:
        print(f"Warning: Right column placeholder not found for '{title}'")

    return slide


def add_quote_slide(prs, quote, attribution):
    """Add a quote slide using Layout 5 styled as quote."""
    layout = prs.slide_layouts[5]
    slide = prs.slides.add_slide(layout)

    try:
        body_ph = slide.placeholders[56]
        tf = body_ph.text_frame
        tf.clear()

        # Quote text
        p = tf.paragraphs[0]
        p.font.name = "Arial"
        p.font.size = Pt(24)
        p.font.italic = True
        p.font.color.rgb = DARK_BLUE

        run = p.add_run()
        run.text = f'"{quote}"'
        run.font.name = "Arial"
        run.font.size = Pt(24)
        run.font.italic = True
        run.font.color.rgb = DARK_BLUE

        # Attribution
        p2 = tf.add_paragraph()
        p2.font.name = "Arial"
        p2.font.size = Pt(16)
        p2.font.color.rgb = PACIFIC_BLUE

        run2 = p2.add_run()
        run2.text = f"— {attribution}"
        run2.font.name = "Arial"
        run2.font.size = Pt(16)
        run2.font.color.rgb = PACIFIC_BLUE
    except KeyError:
        print("Warning: Quote placeholder not found")

    return slide


def add_back_cover(prs):
    """Add back cover using Layout 21."""
    layout = prs.slide_layouts[21]
    slide = prs.slides.add_slide(layout)
    return slide


def remove_draft_watermark(prs):
    """Remove DRAFT watermark from slide masters."""
    for master in prs.slide_masters:
        for shape in list(master.shapes):
            if hasattr(shape, 'text') and 'DRAFT' in shape.text.upper():
                sp = shape._element
                sp.getparent().remove(sp)

# =============================================================================
# POST-PROCESSING
# Required because python-pptx creates duplicate ZIP entries when deleting slides
# =============================================================================

def postprocess_remove_template_slides(input_path, output_path, num_template_slides=30):
    """
    Remove original template slides from PPTX via ZIP/XML manipulation.

    This is necessary because:
    1. We add new slides at END of presentation
    2. python-pptx can't reliably delete slides (creates corrupt ZIP)
    3. Post-processing at ZIP level avoids corruption
    """
    temp_dir = "/tmp/pptx_postprocess"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    # Extract PPTX (handling duplicates by keeping last)
    with zipfile.ZipFile(input_path, 'r') as zf:
        for name in zf.namelist():
            target = os.path.join(temp_dir, name)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, 'wb') as f:
                f.write(zf.read(name))

    # Parse presentation.xml
    pres_path = os.path.join(temp_dir, "ppt", "presentation.xml")
    ET.register_namespace('', 'http://schemas.openxmlformats.org/presentationml/2006/main')
    ET.register_namespace('a', 'http://schemas.openxmlformats.org/drawingml/2006/main')
    ET.register_namespace('r', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships')
    ET.register_namespace('p', 'http://schemas.openxmlformats.org/presentationml/2006/main')

    tree = ET.parse(pres_path)
    root = tree.getroot()

    ns = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
          'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}

    sldIdLst = root.find('.//p:sldIdLst', ns)
    if sldIdLst is None:
        sldIdLst = root.find('.//{http://schemas.openxmlformats.org/presentationml/2006/main}sldIdLst')

    slide_ids = list(sldIdLst)
    total_slides = len(slide_ids)

    # Remove first N template slides
    slides_to_remove = list(range(1, min(num_template_slides + 1, total_slides + 1)))

    # Parse relationships
    rels_path = os.path.join(temp_dir, "ppt", "_rels", "presentation.xml.rels")
    rels_tree = ET.parse(rels_path)
    rels_root = rels_tree.getroot()

    # Remove slide references
    rids_to_remove = []
    for i, sld in enumerate(slide_ids):
        slide_num = i + 1
        if slide_num in slides_to_remove:
            rid = sld.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
            rids_to_remove.append(rid)
            sldIdLst.remove(sld)

    tree.write(pres_path, xml_declaration=True, encoding='UTF-8')

    # Remove relationships and slide files
    for rid in rids_to_remove:
        for rel in list(rels_root):
            if rel.get('Id') == rid:
                target = rel.get('Target')
                rels_root.remove(rel)
                if target:
                    slide_file = os.path.join(temp_dir, "ppt", target)
                    if os.path.exists(slide_file):
                        os.remove(slide_file)
                    slide_name = os.path.basename(target)
                    slide_rels = os.path.join(temp_dir, "ppt", "slides", "_rels", slide_name + ".rels")
                    if os.path.exists(slide_rels):
                        os.remove(slide_rels)

    rels_tree.write(rels_path, xml_declaration=True, encoding='UTF-8')

    # Update [Content_Types].xml
    ct_path = os.path.join(temp_dir, "[Content_Types].xml")
    ct_tree = ET.parse(ct_path)
    ct_root = ct_tree.getroot()

    for override in list(ct_root):
        part = override.get('PartName', '')
        if part.startswith('/ppt/slides/slide'):
            slide_file = part.split('/')[-1]
            slide_path = os.path.join(temp_dir, "ppt", "slides", slide_file)
            if not os.path.exists(slide_path):
                ct_root.remove(override)

    ct_tree.write(ct_path, xml_declaration=True, encoding='UTF-8')

    # Repack
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root_dir, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root_dir, file)
                arcname = os.path.relpath(file_path, temp_dir)
                zf.write(file_path, arcname)

    shutil.rmtree(temp_dir)
    print(f"Post-processing complete: {output_path}")

# =============================================================================
# MAIN - CUSTOMIZE YOUR SLIDES HERE
# =============================================================================

def create_presentation():
    """Create the presentation. Customize slide content below."""
    print("Loading KPMG template...")
    prs = Presentation(TEMPLATE_PATH)
    remove_draft_watermark(prs)

    initial_count = len(prs.slides)
    print(f"Template has {initial_count} slides")

    # =========================================================================
    # ADD YOUR SLIDES HERE
    # =========================================================================

    # Cover slide
    add_cover_slide(prs,
        "Your Presentation Title",
        "Subtitle  |  Date")

    # Section divider (use \n for line breaks)
    add_section_divider(prs, "Part 1\nSection Name")

    # Content slide
    add_content_slide(prs,
        "Slide Title",
        "Strapline summarizing the key message",
        [
            "First bullet point",
            "Second bullet point",
            "Third bullet point",
        ])

    # Two-column slide
    add_two_column_slide(prs,
        "Two Column Title",
        "Comparing two concepts",
        ["Left point 1", "Left point 2", "Left point 3"],
        ["Right point 1", "Right point 2", "Right point 3"])

    # Quote slide
    add_quote_slide(prs,
        "Your quote text here.",
        "Attribution Name")

    # Back cover
    add_back_cover(prs)

    # =========================================================================
    # SAVE AND POST-PROCESS
    # =========================================================================

    print("Saving to temp file...")
    prs.save(TEMP_PATH)

    final_count = len(prs.slides)
    slides_added = final_count - initial_count
    print(f"Added {slides_added} new slides (total: {final_count})")

    print("Post-processing to remove template slides...")
    postprocess_remove_template_slides(TEMP_PATH, OUTPUT_PATH, num_template_slides=initial_count)

    if os.path.exists(TEMP_PATH):
        os.remove(TEMP_PATH)

    print(f"\nPresentation saved to: {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == "__main__":
    create_presentation()

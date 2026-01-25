#!/usr/bin/env python3
"""
KPMG Presentation Reference Script (v2)

Enhanced version with:
- Properly styled tables (dark blue headers, alternating rows, borders)
- Better quote formatting (left accent bar style)
- Speaker notes support
- Content overflow management

Usage:
1. Copy this file to your working directory
2. Update TEMPLATE_PATH, OUTPUT_PATH, and slide content
3. Run: python3 generate_presentation.py
"""

from pptx import Presentation
from pptx.util import Pt, Inches
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os
import shutil
import zipfile
from xml.etree import ElementTree as ET

# =============================================================================
# CONFIGURATION - Update these paths
# =============================================================================

TEMPLATE_PATH = os.path.expanduser(
    "~/Library/Mobile Documents/com~apple~CloudDocs/claude-code/templates/kpmg/KPMG-2022/template-clean.pptx"
)
OUTPUT_PATH = os.path.expanduser("~/Desktop/My_Presentation.pptx")
TEMP_PATH = "/tmp/presentation_temp.pptx"

# =============================================================================
# KPMG COLORS (from config.yaml)
# =============================================================================

DARK_BLUE = RGBColor(12, 35, 60)       # 0C233C - headers, titles, section backgrounds
PACIFIC_BLUE = RGBColor(0, 184, 245)   # 00B8F5 - straplines, accents
WHITE = RGBColor(255, 255, 255)
KPMG_BLUE = RGBColor(0, 51, 141)       # 00338D - links, accents
LIGHT_GRAY = RGBColor(242, 242, 242)   # F2F2F2 - alternating rows
BLACK = RGBColor(0, 0, 0)

# =============================================================================
# LAYOUT INDICES (template-clean.pptx - 15 layouts, indices 0-14)
# =============================================================================
# Layout 0: Cover page
# Layout 3: 1_Subsection divider (dark blue background)
# Layout 10: One Column Text (title=0, strapline=18, body=56)
# Layout 11: Two Columns Text (title=0, strapline=18, left=56, right=57)
# Layout 13: 1_Back Cover light gradient

LAYOUT_COVER = 0
LAYOUT_SECTION = 3
LAYOUT_ONE_COLUMN = 10
LAYOUT_TWO_COLUMN = 11
LAYOUT_BACK_COVER = 13

# =============================================================================
# TEXT FORMATTING
# =============================================================================

def set_text_with_formatting(shape, text, font_name="Arial", font_size=Pt(16),
                             bold=False, italic=False, color=None, alignment=None):
    """
    Set text with proper font formatting at both paragraph and run level.

    CRITICAL: Must set properties at BOTH paragraph AND run level to override master.
    """
    tf = shape.text_frame
    tf.clear()

    p = tf.paragraphs[0]
    if alignment:
        p.alignment = alignment

    # Paragraph level
    p.font.name = font_name
    p.font.size = font_size
    p.font.bold = bold
    p.font.italic = italic
    if color:
        p.font.color.rgb = color

    # Run level
    run = p.add_run()
    run.text = text
    run.font.name = font_name
    run.font.size = font_size
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = color

    return p


def set_multiline_text(shape, lines, font_name="Arial", font_size=Pt(16),
                       color=None, bullet=False, line_spacing=1.15):
    """Set multiple lines of text with optional bullets and line spacing."""
    tf = shape.text_frame
    tf.clear()
    tf.word_wrap = True

    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()

        p.line_spacing = line_spacing

        # Paragraph level
        p.font.name = font_name
        p.font.size = font_size
        p.font.italic = False
        if color:
            p.font.color.rgb = color

        # Run level
        run = p.add_run()
        run.text = line
        run.font.name = font_name
        run.font.size = font_size
        run.font.italic = False
        if color:
            run.font.color.rgb = color

        if bullet:
            p.level = 0


# =============================================================================
# TABLE STYLING
# =============================================================================

def style_table_cell(cell, text, font_name="Arial", font_size=Pt(12),
                     bold=False, bg_color=None, text_color=BLACK,
                     alignment=PP_ALIGN.LEFT, vertical_anchor=MSO_ANCHOR.MIDDLE):
    """Style a single table cell with proper formatting."""
    if bg_color:
        cell.fill.solid()
        cell.fill.fore_color.rgb = bg_color

    tf = cell.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.anchor = vertical_anchor

    # Cell margins
    tf.margin_left = Inches(0.1)
    tf.margin_right = Inches(0.1)
    tf.margin_top = Inches(0.05)
    tf.margin_bottom = Inches(0.05)

    p = tf.paragraphs[0]
    p.alignment = alignment

    # Paragraph font
    p.font.name = font_name
    p.font.size = font_size
    p.font.bold = bold
    p.font.italic = False
    p.font.color.rgb = text_color

    # Run font
    run = p.add_run()
    run.text = text
    run.font.name = font_name
    run.font.size = font_size
    run.font.bold = bold
    run.font.italic = False
    run.font.color.rgb = text_color


def add_styled_table(slide, data, left, top, width, height,
                     header_bg=DARK_BLUE, header_text=WHITE,
                     alt_row_colors=(WHITE, LIGHT_GRAY),
                     font_size=Pt(11), header_font_size=Pt(12),
                     col_widths=None):
    """
    Add a professionally styled table to a slide.

    Args:
        slide: PowerPoint slide object
        data: List of lists - first row is headers, rest are data rows
        left, top, width, height: Position and size (Inches objects)
        header_bg: Header row background color
        header_text: Header row text color
        alt_row_colors: Tuple of (even_row_color, odd_row_color)
        font_size: Font size for data cells
        header_font_size: Font size for header cells
        col_widths: Optional list of column widths as fractions (must sum to 1.0)

    Returns:
        The created table shape
    """
    if not data or not data[0]:
        return None

    rows = len(data)
    cols = len(data[0])

    table_shape = slide.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    # Column widths
    if col_widths:
        total_width = width
        for i, ratio in enumerate(col_widths):
            table.columns[i].width = int(total_width * ratio)
    else:
        col_width = int(width / cols)
        for i in range(cols):
            table.columns[i].width = col_width

    # Header row
    for j, header_val in enumerate(data[0]):
        cell = table.cell(0, j)
        style_table_cell(
            cell, str(header_val),
            font_name="Arial", font_size=header_font_size,
            bold=True, bg_color=header_bg, text_color=header_text,
            alignment=PP_ALIGN.LEFT
        )

    # Data rows with alternating colors
    for i in range(1, rows):
        row_color = alt_row_colors[(i - 1) % 2]
        for j, cell_text in enumerate(data[i]):
            cell = table.cell(i, j)
            style_table_cell(
                cell, str(cell_text),
                font_name="Arial", font_size=font_size,
                bold=False, bg_color=row_color, text_color=BLACK,
                alignment=PP_ALIGN.LEFT
            )

    return table_shape


def add_compact_table(slide, data, left, top, width,
                      row_height=Inches(0.4), header_row_height=Inches(0.45)):
    """
    Add a compact table optimized for dense data.
    Height is calculated based on number of rows.
    """
    rows = len(data)
    total_height = header_row_height + (row_height * (rows - 1))

    table_shape = add_styled_table(
        slide, data, left, top, width, total_height,
        font_size=Pt(14), header_font_size=Pt(14)
    )

    if table_shape:
        table = table_shape.table
        table.rows[0].height = header_row_height
        for i in range(1, rows):
            table.rows[i].height = row_height

    return table_shape


# =============================================================================
# QUOTE STYLING
# =============================================================================

def add_quote_with_accent_bar(slide, quote_text, attribution,
                              left=Inches(1.07), top=Inches(1.6),
                              width=Inches(11.0), bar_color=PACIFIC_BLUE):
    """
    Add a quote with a left vertical accent bar (professional style).
    """
    # Accent bar
    bar_width = Inches(0.15)
    bar_height = Inches(1.5)

    bar_shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        left, top, bar_width, bar_height
    )
    bar_shape.fill.solid()
    bar_shape.fill.fore_color.rgb = bar_color
    bar_shape.line.fill.background()

    # Quote text box
    text_left = left + bar_width + Inches(0.25)
    text_width = width - bar_width - Inches(0.25)

    quote_box = slide.shapes.add_textbox(text_left, top, text_width, bar_height)
    tf = quote_box.text_frame
    tf.word_wrap = True

    # Quote text
    p = tf.paragraphs[0]
    p.font.name = "Arial"
    p.font.size = Pt(20)
    p.font.italic = True
    p.font.color.rgb = DARK_BLUE
    p.line_spacing = 1.3

    run = p.add_run()
    run.text = f'"{quote_text}"'
    run.font.name = "Arial"
    run.font.size = Pt(20)
    run.font.italic = True
    run.font.color.rgb = DARK_BLUE

    # Attribution
    p2 = tf.add_paragraph()
    p2.space_before = Pt(12)
    p2.font.name = "Arial"
    p2.font.size = Pt(14)
    p2.font.italic = False
    p2.font.color.rgb = PACIFIC_BLUE

    run2 = p2.add_run()
    run2.text = f"— {attribution}"
    run2.font.name = "Arial"
    run2.font.size = Pt(14)
    run2.font.italic = False
    run2.font.color.rgb = PACIFIC_BLUE

    return quote_box, bar_shape


def add_quote_box(slide, quote_text, attribution,
                  left=Inches(1.07), top=Inches(1.6),
                  width=Inches(11.0), bg_color=None):
    """
    Add a quote in a styled box (alternative to accent bar).
    """
    chars_per_line = 60
    lines = len(quote_text) // chars_per_line + 2
    height = Inches(0.5 + lines * 0.4)

    quote_box = slide.shapes.add_textbox(left, top, width, height)
    tf = quote_box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.2)
    tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.15)
    tf.margin_bottom = Inches(0.15)

    if bg_color:
        quote_box.fill.solid()
        quote_box.fill.fore_color.rgb = bg_color

    # Quote text
    p = tf.paragraphs[0]
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.italic = True
    p.font.color.rgb = DARK_BLUE
    p.line_spacing = 1.25

    run = p.add_run()
    run.text = f'"{quote_text}"'
    run.font.name = "Arial"
    run.font.size = Pt(18)
    run.font.italic = True
    run.font.color.rgb = DARK_BLUE

    # Attribution
    p2 = tf.add_paragraph()
    p2.space_before = Pt(8)
    p2.alignment = PP_ALIGN.RIGHT
    p2.font.name = "Arial"
    p2.font.size = Pt(12)
    p2.font.italic = False
    p2.font.color.rgb = PACIFIC_BLUE

    run2 = p2.add_run()
    run2.text = f"— {attribution}"
    run2.font.name = "Arial"
    run2.font.size = Pt(12)
    run2.font.italic = False
    run2.font.color.rgb = PACIFIC_BLUE

    return quote_box


# =============================================================================
# SPEAKER NOTES
# =============================================================================

def add_speaker_notes(slide, notes_text):
    """Add speaker notes to a slide."""
    notes_slide = slide.notes_slide
    notes_tf = notes_slide.notes_text_frame
    notes_tf.text = notes_text


def extract_speaker_notes(source_prs, slide_index):
    """Extract speaker notes from a source presentation slide."""
    try:
        slide = source_prs.slides[slide_index]
        notes_slide = slide.notes_slide
        notes_tf = notes_slide.notes_text_frame
        return notes_tf.text
    except (IndexError, AttributeError):
        return ""


# =============================================================================
# SLIDE CREATION FUNCTIONS
# CRITICAL: Use try/except for placeholder access, NOT "if X in slide.placeholders"
# =============================================================================

def add_cover_slide(prs, title, subtitle, notes=None):
    """Add cover slide using Layout 0. Title: 88pt KPMG Bold White."""
    layout = prs.slide_layouts[LAYOUT_COVER]
    slide = prs.slides.add_slide(layout)

    try:
        title_ph = slide.placeholders[0]
        set_text_with_formatting(title_ph, title, "KPMG Bold", Pt(88),
                                 bold=True, italic=False, color=WHITE, alignment=PP_ALIGN.LEFT)
    except KeyError:
        print("Warning: Cover title placeholder not found")

    try:
        subtitle_ph = slide.placeholders[11]
        set_text_with_formatting(subtitle_ph, subtitle, "Arial", Pt(18),
                                 bold=False, italic=False, color=WHITE, alignment=PP_ALIGN.LEFT)
    except KeyError:
        pass

    if notes:
        add_speaker_notes(slide, notes)

    return slide


def add_section_divider(prs, section_title, notes=None):
    """Add section divider using Layout 5 with dark blue background."""
    layout = prs.slide_layouts[LAYOUT_SECTION]
    slide = prs.slides.add_slide(layout)

    # Set background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = DARK_BLUE

    try:
        title_ph = slide.placeholders[0]
        set_text_with_formatting(title_ph, section_title, "KPMG Bold", Pt(66),
                                 bold=True, italic=False, color=WHITE, alignment=PP_ALIGN.LEFT)
    except KeyError:
        print("Warning: Section divider title placeholder not found")

    if notes:
        add_speaker_notes(slide, notes)

    return slide


def add_content_slide(prs, title, strapline, body_lines, notes=None):
    """
    Add one-column content slide using Layout 12.
    - Title: 44pt KPMG Bold Dark Blue
    - Strapline: 18pt Arial Pacific Blue
    - Body: 16pt Arial with bullets
    """
    layout = prs.slide_layouts[LAYOUT_ONE_COLUMN]
    slide = prs.slides.add_slide(layout)

    try:
        title_ph = slide.placeholders[0]
        set_text_with_formatting(title_ph, title, "KPMG Bold", Pt(44),
                                 bold=True, italic=False, color=DARK_BLUE, alignment=PP_ALIGN.LEFT)
    except KeyError:
        print(f"Warning: Title placeholder not found for '{title}'")

    try:
        strap_ph = slide.placeholders[18]
        set_text_with_formatting(strap_ph, strapline, "Arial", Pt(18),
                                 bold=False, italic=False, color=PACIFIC_BLUE, alignment=PP_ALIGN.LEFT)
    except KeyError:
        pass

    try:
        body_ph = slide.placeholders[56]
        set_multiline_text(body_ph, body_lines, "Arial", Pt(16), bullet=True)
    except KeyError:
        print(f"Warning: Body placeholder not found for '{title}'")

    if notes:
        add_speaker_notes(slide, notes)

    return slide


def add_content_slide_with_table(prs, title, strapline, table_data, notes=None,
                                 col_widths=None):
    """Add content slide with a styled table instead of bullet points."""
    layout = prs.slide_layouts[LAYOUT_ONE_COLUMN]
    slide = prs.slides.add_slide(layout)

    try:
        title_ph = slide.placeholders[0]
        set_text_with_formatting(title_ph, title, "KPMG Bold", Pt(44),
                                 bold=True, italic=False, color=DARK_BLUE, alignment=PP_ALIGN.LEFT)
    except KeyError:
        print(f"Warning: Title placeholder not found for '{title}'")

    try:
        strap_ph = slide.placeholders[18]
        set_text_with_formatting(strap_ph, strapline, "Arial", Pt(18),
                                 bold=False, italic=False, color=PACIFIC_BLUE, alignment=PP_ALIGN.LEFT)
    except KeyError:
        pass

    # Add table in body area (matches placeholder 56 position)
    table_left = Inches(1.07)
    table_top = Inches(1.6)
    table_width = Inches(11.0)

    add_compact_table(slide, table_data, table_left, table_top, table_width)

    if notes:
        add_speaker_notes(slide, notes)

    return slide


def add_content_slide_with_quote(prs, title, strapline, quote_text, attribution, notes=None):
    """Add content slide with a styled quote using accent bar."""
    layout = prs.slide_layouts[LAYOUT_ONE_COLUMN]
    slide = prs.slides.add_slide(layout)

    try:
        title_ph = slide.placeholders[0]
        set_text_with_formatting(title_ph, title, "KPMG Bold", Pt(44),
                                 bold=True, italic=False, color=DARK_BLUE, alignment=PP_ALIGN.LEFT)
    except KeyError:
        print(f"Warning: Title placeholder not found for '{title}'")

    try:
        strap_ph = slide.placeholders[18]
        set_text_with_formatting(strap_ph, strapline, "Arial", Pt(18),
                                 bold=False, italic=False, color=PACIFIC_BLUE, alignment=PP_ALIGN.LEFT)
    except KeyError:
        pass

    add_quote_with_accent_bar(slide, quote_text, attribution)

    if notes:
        add_speaker_notes(slide, notes)

    return slide


def add_two_column_slide(prs, title, strapline, left_lines, right_lines, notes=None):
    """Add two-column content slide using Layout 13."""
    layout = prs.slide_layouts[LAYOUT_TWO_COLUMN]
    slide = prs.slides.add_slide(layout)

    try:
        title_ph = slide.placeholders[0]
        set_text_with_formatting(title_ph, title, "KPMG Bold", Pt(44),
                                 bold=True, italic=False, color=DARK_BLUE, alignment=PP_ALIGN.LEFT)
    except KeyError:
        print(f"Warning: Title placeholder not found for '{title}'")

    try:
        strap_ph = slide.placeholders[18]
        set_text_with_formatting(strap_ph, strapline, "Arial", Pt(18),
                                 bold=False, italic=False, color=PACIFIC_BLUE, alignment=PP_ALIGN.LEFT)
    except KeyError:
        pass

    try:
        left_ph = slide.placeholders[56]
        set_multiline_text(left_ph, left_lines, "Arial", Pt(14), bullet=True)
    except KeyError:
        print(f"Warning: Left column placeholder not found for '{title}'")

    try:
        right_ph = slide.placeholders[57]
        set_multiline_text(right_ph, right_lines, "Arial", Pt(14), bullet=True)
    except KeyError:
        print(f"Warning: Right column placeholder not found for '{title}'")

    if notes:
        add_speaker_notes(slide, notes)

    return slide


def add_back_cover(prs):
    """Add back cover using Layout 17."""
    layout = prs.slide_layouts[LAYOUT_BACK_COVER]
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
# UTILITY FUNCTIONS
# =============================================================================

def estimate_text_lines(text, chars_per_line=60):
    """Estimate number of lines text will occupy."""
    lines = text.split('\n')
    total = 0
    for line in lines:
        total += max(1, len(line) // chars_per_line + 1)
    return total


def truncate_for_slide(text, max_chars=500):
    """Truncate text to fit on a slide, ending at sentence boundary if possible."""
    if len(text) <= max_chars:
        return text

    truncated = text[:max_chars]
    last_period = truncated.rfind('.')
    if last_period > max_chars * 0.6:
        return truncated[:last_period + 1]

    last_space = truncated.rfind(' ')
    if last_space > 0:
        return truncated[:last_space] + "..."

    return truncated + "..."


# =============================================================================
# POST-PROCESSING
# =============================================================================

def postprocess_remove_template_slides(input_path, output_path, num_template_slides=0):
    """Remove original template slides from PPTX via ZIP/XML manipulation."""
    if num_template_slides == 0:
        shutil.copy(input_path, output_path)
        return

    temp_dir = "/tmp/pptx_postprocess"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    with zipfile.ZipFile(input_path, 'r') as zf:
        for name in zf.namelist():
            target = os.path.join(temp_dir, name)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, 'wb') as f:
                f.write(zf.read(name))

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

    slides_to_remove = list(range(1, min(num_template_slides + 1, total_slides + 1)))

    rels_path = os.path.join(temp_dir, "ppt", "_rels", "presentation.xml.rels")
    rels_tree = ET.parse(rels_path)
    rels_root = rels_tree.getroot()

    rids_to_remove = []
    for i, sld in enumerate(slide_ids):
        slide_num = i + 1
        if slide_num in slides_to_remove:
            rid = sld.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
            rids_to_remove.append(rid)
            sldIdLst.remove(sld)

    tree.write(pres_path, xml_declaration=True, encoding='UTF-8')

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
        "Subtitle  |  Date",
        notes="Opening remarks for this slide...")

    # Section divider
    add_section_divider(prs, "Part 1\nSection Name",
        notes="Transition to first section...")

    # Content slide
    add_content_slide(prs,
        "Slide Title",
        "Strapline summarizing the key message",
        [
            "First bullet point",
            "Second bullet point",
            "Third bullet point",
        ],
        notes="Key talking points for this slide...")

    # Table slide
    table_data = [
        ["Header 1", "Header 2", "Header 3"],
        ["Row 1 A", "Row 1 B", "Row 1 C"],
        ["Row 2 A", "Row 2 B", "Row 2 C"],
    ]
    add_content_slide_with_table(prs,
        "Table Example",
        "Comparing key metrics",
        table_data,
        notes="Explain the table data...")

    # Quote slide
    add_content_slide_with_quote(prs,
        "Industry Insight",
        "What experts are saying",
        "Your quote text here.",
        "Attribution Name",
        notes="Context for this quote...")

    # Two-column slide
    add_two_column_slide(prs,
        "Two Column Title",
        "Comparing two concepts",
        ["Left point 1", "Left point 2", "Left point 3"],
        ["Right point 1", "Right point 2", "Right point 3"],
        notes="Compare left and right...")

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

    print("Post-processing...")
    postprocess_remove_template_slides(TEMP_PATH, OUTPUT_PATH, num_template_slides=initial_count)

    if os.path.exists(TEMP_PATH):
        os.remove(TEMP_PATH)

    print(f"\nPresentation saved to: {OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == "__main__":
    create_presentation()

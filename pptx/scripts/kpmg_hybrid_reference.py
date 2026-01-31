#!/usr/bin/env python3
"""
KPMG Hybrid Approach Trial v2

Uses python-pptx with KPMG template to preserve:
- KPMG logo from slide master
- Footer elements
- Cover and section divider layouts

Then adds creative content (shapes, callout boxes) in the body area.
"""

from pptx import Presentation
from pptx.util import Pt, Inches
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

# =============================================================================
# CONFIGURATION
# =============================================================================

TEMPLATE_PATH = os.path.expanduser(
    "~/Library/Mobile Documents/com~apple~CloudDocs/claude-code/templates/kpmg/KPMG-2022/template-clean.pptx"
)
OUTPUT_PATH = os.path.expanduser("~/Desktop/KPMG_Hybrid_Trial_v2.pptx")

# =============================================================================
# KPMG COLORS
# =============================================================================

DARK_BLUE = RGBColor(12, 35, 60)
PACIFIC_BLUE = RGBColor(0, 184, 245)
KPMG_BLUE = RGBColor(0, 51, 141)
WHITE = RGBColor(255, 255, 255)
GREY_5 = RGBColor(229, 229, 229)
BLUE_GRAY = RGBColor(52, 85, 109)
AQUA = RGBColor(119, 168, 190)
LIGHT_TURQUOISE = RGBColor(150, 206, 228)

# =============================================================================
# LAYOUT INDICES (from config.yaml)
# =============================================================================

LAYOUT_COVER = 0
LAYOUT_SECTION = 3
LAYOUT_ONE_COLUMN = 10
LAYOUT_TWO_COLUMN = 11
LAYOUT_BACK_COVER = 13

# =============================================================================
# CONTENT SAFE ZONE (from config.yaml)
# =============================================================================

SAFE_ZONE = {
    'content_y': 1.47,      # Below strapline
    'content_h': 4.7,       # To footer (reduced from 4.96 for safety)
    'left': 1.07,
    'width': 11.0,          # Reduced from 11.18 for safety margin
}

# =============================================================================
# TEXT FORMATTING (from reference script)
# =============================================================================

def set_text_with_formatting(shape, text, font_name="Arial", font_size=Pt(16),
                             bold=False, italic=False, color=None, alignment=None):
    """Set text with proper font formatting at both paragraph and run level."""
    tf = shape.text_frame
    tf.clear()

    p = tf.paragraphs[0]
    if alignment:
        p.alignment = alignment

    p.font.name = font_name
    p.font.size = font_size
    p.font.bold = bold
    p.font.italic = italic
    if color:
        p.font.color.rgb = color

    run = p.add_run()
    run.text = text
    run.font.name = font_name
    run.font.size = font_size
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = color


# =============================================================================
# SLIDE CREATION - RIGID TEMPLATE SLIDES
# =============================================================================

def add_cover_slide(prs, title, subtitle):
    """Add cover using template Layout 0 - preserves logo, format."""
    layout = prs.slide_layouts[LAYOUT_COVER]
    slide = prs.slides.add_slide(layout)

    try:
        title_ph = slide.placeholders[0]
        set_text_with_formatting(title_ph, title, "KPMG Bold", Pt(88),
                                bold=True, italic=False, color=WHITE)
    except KeyError:
        print("Warning: Cover title placeholder not found")

    try:
        subtitle_ph = slide.placeholders[11]
        set_text_with_formatting(subtitle_ph, subtitle, "Arial", Pt(18),
                                bold=False, italic=False, color=WHITE)
    except KeyError:
        pass

    return slide


def add_section_divider(prs, section_title):
    """Add section divider using template Layout 3 - preserves format."""
    layout = prs.slide_layouts[LAYOUT_SECTION]
    slide = prs.slides.add_slide(layout)

    # Set dark blue background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = DARK_BLUE

    try:
        title_ph = slide.placeholders[0]
        set_text_with_formatting(title_ph, section_title, "KPMG Bold", Pt(66),
                                bold=True, italic=False, color=WHITE)
    except KeyError:
        print("Warning: Section title placeholder not found")

    return slide


def add_back_cover(prs):
    """Add back cover using template Layout 13 - preserves format."""
    layout = prs.slide_layouts[LAYOUT_BACK_COVER]
    slide = prs.slides.add_slide(layout)
    return slide


# =============================================================================
# SLIDE CREATION - CREATIVE CONTENT SLIDES
# =============================================================================

def add_content_slide_with_callouts(prs, title, strapline, callouts):
    """
    Add content slide with creative callout boxes.
    - Title and strapline use template placeholders
    - Body area has creative callout boxes
    """
    layout = prs.slide_layouts[LAYOUT_ONE_COLUMN]
    slide = prs.slides.add_slide(layout)

    # Title (template placeholder)
    try:
        title_ph = slide.placeholders[0]
        set_text_with_formatting(title_ph, title, "KPMG Bold", Pt(44),
                                bold=True, italic=False, color=DARK_BLUE)
    except KeyError:
        print(f"Warning: Title placeholder not found for '{title}'")

    # Strapline (template placeholder)
    try:
        strap_ph = slide.placeholders[18]
        set_text_with_formatting(strap_ph, strapline, "Arial", Pt(18),
                                bold=False, italic=False, color=PACIFIC_BLUE)
    except KeyError:
        pass

    # Clear body placeholder (we'll add custom shapes instead)
    try:
        body_ph = slide.placeholders[56]
        body_ph.text_frame.clear()
    except KeyError:
        pass

    # CREATIVE CONTENT: Three callout boxes
    box_width = Inches(3.4)
    box_height = Inches(3.0)
    gap = Inches(0.4)
    colors = [BLUE_GRAY, AQUA, PACIFIC_BLUE]

    for i, callout in enumerate(callouts):
        x = Inches(SAFE_ZONE['left']) + (box_width + gap) * i
        y = Inches(SAFE_ZONE['content_y'])

        # Number circle
        circle = slide.shapes.add_shape(
            MSO_SHAPE.OVAL,
            x + box_width/2 - Inches(0.25),
            y,
            Inches(0.5), Inches(0.5)
        )
        circle.fill.solid()
        circle.fill.fore_color.rgb = colors[i]
        circle.line.fill.background()

        # Number text
        tf = circle.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = str(i + 1)
        run.font.name = "Arial"
        run.font.size = Pt(20)
        run.font.bold = True
        run.font.color.rgb = WHITE
        tf.anchor = MSO_ANCHOR.MIDDLE

        # Callout box
        box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            x, y + Inches(0.6),
            box_width, box_height - Inches(0.6)
        )
        box.fill.solid()
        box.fill.fore_color.rgb = GREY_5
        box.line.color.rgb = colors[i]
        box.line.width = Pt(2)
        box.adjustments[0] = 0.05  # Corner radius

        # Title textbox
        title_box = slide.shapes.add_textbox(
            x + Inches(0.15), y + Inches(0.75),
            box_width - Inches(0.3), Inches(0.4)
        )
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.font.name = "Arial"
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = DARK_BLUE
        run = p.add_run()
        run.text = callout['title']
        run.font.name = "Arial"
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = DARK_BLUE

        # Body textbox
        body_box = slide.shapes.add_textbox(
            x + Inches(0.15), y + Inches(1.2),
            box_width - Inches(0.3), Inches(1.8)
        )
        tf = body_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.font.name = "Arial"
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_BLUE
        run = p.add_run()
        run.text = callout['body']
        run.font.name = "Arial"
        run.font.size = Pt(11)
        run.font.color.rgb = DARK_BLUE

    return slide


def add_content_slide_with_table(prs, title, strapline, table_data):
    """
    Add content slide with styled table.
    - Title and strapline use template placeholders
    - Body area has creative table
    """
    layout = prs.slide_layouts[LAYOUT_ONE_COLUMN]
    slide = prs.slides.add_slide(layout)

    # Title (template placeholder)
    try:
        title_ph = slide.placeholders[0]
        set_text_with_formatting(title_ph, title, "KPMG Bold", Pt(44),
                                bold=True, italic=False, color=DARK_BLUE)
    except KeyError:
        print(f"Warning: Title placeholder not found for '{title}'")

    # Strapline (template placeholder)
    try:
        strap_ph = slide.placeholders[18]
        set_text_with_formatting(strap_ph, strapline, "Arial", Pt(18),
                                bold=False, italic=False, color=PACIFIC_BLUE)
    except KeyError:
        pass

    # Clear body placeholder
    try:
        body_ph = slide.placeholders[56]
        body_ph.text_frame.clear()
    except KeyError:
        pass

    # CREATIVE CONTENT: Styled table
    rows = len(table_data)
    cols = len(table_data[0])

    table_shape = slide.shapes.add_table(
        rows, cols,
        Inches(SAFE_ZONE['left']),
        Inches(SAFE_ZONE['content_y']),
        Inches(SAFE_ZONE['width']),
        Inches(min(rows * 0.5, SAFE_ZONE['content_h']))
    )
    table = table_shape.table

    # Style cells
    for i, row_data in enumerate(table_data):
        for j, cell_text in enumerate(row_data):
            cell = table.cell(i, j)

            # Background
            if i == 0:  # Header row
                cell.fill.solid()
                cell.fill.fore_color.rgb = DARK_BLUE
            elif i % 2 == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = GREY_5
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = WHITE

            # Text
            tf = cell.text_frame
            tf.clear()
            tf.word_wrap = True
            tf.anchor = MSO_ANCHOR.MIDDLE

            p = tf.paragraphs[0]
            p.font.name = "Arial"
            p.font.size = Pt(12)
            p.font.bold = (i == 0)
            p.font.color.rgb = WHITE if i == 0 else DARK_BLUE

            run = p.add_run()
            run.text = str(cell_text)
            run.font.name = "Arial"
            run.font.size = Pt(12)
            run.font.bold = (i == 0)
            run.font.color.rgb = WHITE if i == 0 else DARK_BLUE

    return slide


def add_content_slide_with_bullets(prs, title, strapline, bullets):
    """Standard bullet slide using template placeholder (simple approach)."""
    layout = prs.slide_layouts[LAYOUT_ONE_COLUMN]
    slide = prs.slides.add_slide(layout)

    try:
        title_ph = slide.placeholders[0]
        set_text_with_formatting(title_ph, title, "KPMG Bold", Pt(44),
                                bold=True, italic=False, color=DARK_BLUE)
    except KeyError:
        pass

    try:
        strap_ph = slide.placeholders[18]
        set_text_with_formatting(strap_ph, strapline, "Arial", Pt(18),
                                bold=False, italic=False, color=PACIFIC_BLUE)
    except KeyError:
        pass

    try:
        body_ph = slide.placeholders[56]
        tf = body_ph.text_frame
        tf.clear()

        for i, bullet in enumerate(bullets):
            if i == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()

            p.level = 0
            p.font.name = "Arial"
            p.font.size = Pt(16)
            p.font.italic = False

            run = p.add_run()
            run.text = bullet
            run.font.name = "Arial"
            run.font.size = Pt(16)
            run.font.italic = False
    except KeyError:
        pass

    return slide


# =============================================================================
# MAIN
# =============================================================================

def create_presentation():
    print("Loading KPMG template...")
    prs = Presentation(TEMPLATE_PATH)

    # Remove DRAFT watermark if present
    for master in prs.slide_masters:
        for shape in list(master.shapes):
            if hasattr(shape, 'text') and 'DRAFT' in shape.text.upper():
                sp = shape._element
                sp.getparent().remove(sp)

    print(f"Template loaded. Creating slides...")

    # 1. Cover slide (RIGID - uses template layout)
    add_cover_slide(prs,
        "Hybrid Approach Trial v2",
        "Template Structure + Creative Content"
    )

    # 2. Section divider (RIGID - uses template layout)
    add_section_divider(prs, "Part 1\nCreative Content")

    # 3. Callout boxes slide (HYBRID - template header + creative body)
    add_content_slide_with_callouts(prs,
        "Three Key Insights",
        "Strategic priorities for the next fiscal year",
        [
            {'title': 'Market Expansion',
             'body': 'Targeting 3 new geographic regions with established distribution partnerships.'},
            {'title': 'Digital Transformation',
             'body': 'Modernizing core systems to improve operational efficiency by 25%.'},
            {'title': 'Talent Development',
             'body': 'Investing in upskilling programs to build future leadership pipeline.'}
        ]
    )

    # 4. Table slide (HYBRID - template header + creative body)
    add_content_slide_with_table(prs,
        "Competitive Analysis",
        "Market positioning across key dimensions",
        [
            ['Dimension', 'Company A', 'Company B', 'Our Position'],
            ['Market Share', '35%', '28%', '22%'],
            ['Growth Rate', '8%', '12%', '18%'],
            ['Customer NPS', '42', '38', '56'],
            ['Innovation Index', 'Medium', 'High', 'High']
        ]
    )

    # 5. Simple bullet slide (for comparison)
    add_content_slide_with_bullets(prs,
        "Simple Bullet Slide",
        "Comparison with placeholder-only approach",
        [
            "This slide uses the template body placeholder",
            "Results in simple bulleted text",
            "Less visual sophistication than creative slides",
            "But faster to implement for basic content"
        ]
    )

    # 6. Back cover (RIGID - uses template layout)
    add_back_cover(prs)

    # Save
    prs.save(OUTPUT_PATH)
    print(f"\nPresentation saved to: {OUTPUT_PATH}")
    print("\nSlides created:")
    print("1. Cover (template layout - should have KPMG logo)")
    print("2. Section divider (template layout)")
    print("3. Callout boxes (hybrid - creative content)")
    print("4. Table (hybrid - creative content)")
    print("5. Simple bullets (placeholder-only, for comparison)")
    print("6. Back cover (template layout)")


if __name__ == "__main__":
    create_presentation()

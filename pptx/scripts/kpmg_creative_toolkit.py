#!/usr/bin/env python3
"""
KPMG Creative Toolkit - Anthropic-Inspired Patterns

Design principles borrowed from Anthropic presentations:
- No strapline (title only, clean headers)
- Generous whitespace
- Accent color highlights
- Two/three column layouts
- Clean tables with accent headers
- Quote boxes with accent borders

All patterns use KPMG colors and preserve template branding.
"""

from pptx import Presentation
from pptx.util import Pt, Inches, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import nsmap
import os

# =============================================================================
# KPMG COLORS
# =============================================================================

# Primary
DARK_BLUE = RGBColor(12, 35, 60)
PACIFIC_BLUE = RGBColor(0, 184, 245)
KPMG_BLUE = RGBColor(0, 51, 141)
LIGHT_BLUE = RGBColor(172, 234, 255)
WHITE = RGBColor(255, 255, 255)

# Chart / Callouts
BLUE_GRAY = RGBColor(52, 85, 109)
AQUA = RGBColor(119, 168, 190)
LIGHT_TURQUOISE = RGBColor(150, 206, 228)
GREY_5 = RGBColor(229, 229, 229)
BLUE_ACCENT_1 = RGBColor(210, 219, 249)

# RAG
RAG_RED = RGBColor(237, 33, 36)
RAG_YELLOW = RGBColor(241, 196, 77)
RAG_GREEN = RGBColor(38, 153, 36)

# =============================================================================
# LAYOUT INDICES (13 layouts, indices 0-12)
# =============================================================================

LAYOUT_COVER = 0
LAYOUT_SECTION = 1
LAYOUT_ONE_COLUMN = 3
LAYOUT_TWO_COLUMN = 4
LAYOUT_BACK_COVER = 5

# =============================================================================
# CONTENT SAFE ZONE (no strapline - starts right below title)
# =============================================================================

SAFE_ZONE = {
    'y': 1.07,          # Below title (no strapline)
    'h': 5.1,           # To footer (with margin)
    'left': 1.07,
    'right': 12.25,
    'width': 11.0,      # With safety margin
}

# =============================================================================
# TEXT UTILITIES
# =============================================================================

def set_text_formatting(shape, text, font_name="Arial", font_size=Pt(16),
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


def add_multiline_text(text_frame, lines, font_name="Arial", font_size=Pt(14),
                       color=DARK_BLUE, line_spacing=1.2):
    """Add multiple lines of text to a text frame."""
    text_frame.clear()
    text_frame.word_wrap = True

    for i, line in enumerate(lines):
        if i == 0:
            p = text_frame.paragraphs[0]
        else:
            p = text_frame.add_paragraph()

        p.font.name = font_name
        p.font.size = font_size
        p.font.color.rgb = color
        p.font.italic = False
        p.space_after = Pt(font_size.pt * (line_spacing - 1))

        run = p.add_run()
        run.text = line
        run.font.name = font_name
        run.font.size = font_size
        run.font.color.rgb = color
        run.font.italic = False


def add_bullet_text(text_frame, bullets, font_name="Arial", font_size=Pt(14),
                    color=DARK_BLUE, bullet_color=PACIFIC_BLUE):
    """Add bulleted text to a text frame."""
    text_frame.clear()
    text_frame.word_wrap = True

    for i, bullet in enumerate(bullets):
        if i == 0:
            p = text_frame.paragraphs[0]
        else:
            p = text_frame.add_paragraph()

        p.level = 0
        p.font.name = font_name
        p.font.size = font_size
        p.font.color.rgb = color
        p.font.italic = False

        run = p.add_run()
        run.text = bullet
        run.font.name = font_name
        run.font.size = font_size
        run.font.color.rgb = color
        run.font.italic = False


# =============================================================================
# SLIDE COMPONENTS - RIGID (from template)
# =============================================================================

def add_cover_slide(prs, title, subtitle=""):
    """Add cover using template Layout 0."""
    layout = prs.slide_layouts[LAYOUT_COVER]
    slide = prs.slides.add_slide(layout)

    try:
        title_ph = slide.placeholders[0]
        set_text_formatting(title_ph, title, "KPMG Bold", Pt(88),
                           bold=True, italic=False, color=WHITE)
    except KeyError:
        pass

    if subtitle:
        try:
            subtitle_ph = slide.placeholders[11]
            set_text_formatting(subtitle_ph, subtitle, "Arial", Pt(18),
                               bold=False, italic=False, color=WHITE)
        except KeyError:
            pass

    return slide


def add_section_divider(prs, section_title):
    """Add section divider using template Layout 3."""
    layout = prs.slide_layouts[LAYOUT_SECTION]
    slide = prs.slides.add_slide(layout)

    # Set dark blue background
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = DARK_BLUE

    try:
        title_ph = slide.placeholders[0]
        set_text_formatting(title_ph, section_title, "KPMG Bold", Pt(66),
                           bold=True, italic=False, color=WHITE)
    except KeyError:
        pass

    return slide


def add_back_cover(prs):
    """Add back cover using template Layout 13."""
    layout = prs.slide_layouts[LAYOUT_BACK_COVER]
    slide = prs.slides.add_slide(layout)
    return slide


def prepare_content_slide(prs, title):
    """
    Create a content slide with title, clearing body placeholder.
    Returns slide ready for creative content.
    """
    layout = prs.slide_layouts[LAYOUT_ONE_COLUMN]
    slide = prs.slides.add_slide(layout)

    # Title (template placeholder - type="title", no idx)
    try:
        title_ph = slide.placeholders[0]
        set_text_formatting(title_ph, title, "KPMG Bold", Pt(44),
                           bold=True, italic=False, color=DARK_BLUE)
    except KeyError:
        pass

    # Clear body placeholder (idx 10)
    try:
        body_ph = slide.placeholders[10]
        body_ph.text_frame.clear()
    except KeyError:
        pass

    return slide


# =============================================================================
# CREATIVE COMPONENTS - Anthropic-Inspired Patterns
# =============================================================================

def add_two_column_text(slide, left_content, right_content,
                        left_title=None, right_title=None):
    """
    Two-column layout with optional headers.
    Anthropic pattern: generous spacing, clean separation.
    """
    col_width = Inches(5.0)
    col_height = Inches(SAFE_ZONE['h'] - 0.5)
    gap = Inches(0.5)

    left_x = Inches(SAFE_ZONE['left'])
    right_x = Inches(SAFE_ZONE['left']) + col_width + gap
    y = Inches(SAFE_ZONE['y'] + 0.2)

    # Left column
    if left_title:
        left_header = slide.shapes.add_textbox(left_x, y, col_width, Inches(0.4))
        set_text_formatting(left_header, left_title, "Arial", Pt(18),
                           bold=True, color=PACIFIC_BLUE)
        left_body_y = y + Inches(0.5)
    else:
        left_body_y = y

    left_box = slide.shapes.add_textbox(left_x, left_body_y, col_width, col_height)
    left_box.text_frame.word_wrap = True
    if isinstance(left_content, list):
        add_bullet_text(left_box.text_frame, left_content)
    else:
        add_multiline_text(left_box.text_frame, [left_content])

    # Right column
    if right_title:
        right_header = slide.shapes.add_textbox(right_x, y, col_width, Inches(0.4))
        set_text_formatting(right_header, right_title, "Arial", Pt(18),
                           bold=True, color=PACIFIC_BLUE)
        right_body_y = y + Inches(0.5)
    else:
        right_body_y = y

    right_box = slide.shapes.add_textbox(right_x, right_body_y, col_width, col_height)
    right_box.text_frame.word_wrap = True
    if isinstance(right_content, list):
        add_bullet_text(right_box.text_frame, right_content)
    else:
        add_multiline_text(right_box.text_frame, [right_content])

    return slide


def add_three_column_cards(slide, cards):
    """
    Three-column card layout with icons/numbers.
    Anthropic pattern: numbered cards, accent borders, generous padding.

    cards: list of {'title': str, 'body': str, 'icon': str (optional)}
    """
    card_width = Inches(3.4)
    card_height = Inches(3.5)
    gap = Inches(0.3)

    colors = [BLUE_GRAY, AQUA, PACIFIC_BLUE]

    for i, card in enumerate(cards[:3]):
        x = Inches(SAFE_ZONE['left']) + (card_width + gap) * i
        y = Inches(SAFE_ZONE['y'] + 0.2)

        # Number circle (Anthropic uses icons, we use numbers)
        circle = slide.shapes.add_shape(
            MSO_SHAPE.OVAL,
            x + card_width/2 - Inches(0.3),
            y,
            Inches(0.6), Inches(0.6)
        )
        circle.fill.solid()
        circle.fill.fore_color.rgb = colors[i]
        circle.line.fill.background()

        # Number in circle
        tf = circle.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = card.get('icon', str(i + 1))
        run.font.name = "Arial"
        run.font.size = Pt(22)
        run.font.bold = True
        run.font.color.rgb = WHITE
        tf.anchor = MSO_ANCHOR.MIDDLE

        # Card background
        box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            x, y + Inches(0.7),
            card_width, card_height - Inches(0.7)
        )
        box.fill.solid()
        box.fill.fore_color.rgb = GREY_5
        box.line.color.rgb = colors[i]
        box.line.width = Pt(2)
        if hasattr(box, 'adjustments') and len(box.adjustments) > 0:
            box.adjustments[0] = 0.05

        # Card title
        title_box = slide.shapes.add_textbox(
            x + Inches(0.2), y + Inches(0.9),
            card_width - Inches(0.4), Inches(0.5)
        )
        set_text_formatting(title_box, card['title'], "Arial", Pt(16),
                           bold=True, color=DARK_BLUE, alignment=PP_ALIGN.CENTER)

        # Card body
        body_box = slide.shapes.add_textbox(
            x + Inches(0.2), y + Inches(1.5),
            card_width - Inches(0.4), Inches(2.0)
        )
        body_box.text_frame.word_wrap = True
        add_multiline_text(body_box.text_frame, [card['body']], font_size=Pt(12))

    return slide


def add_accent_table(slide, headers, rows, accent_color=DARK_BLUE):
    """
    Clean table with accent header row.
    Anthropic pattern: minimal borders, strong header, alternating rows.
    """
    num_rows = len(rows) + 1
    num_cols = len(headers)

    table_width = Inches(SAFE_ZONE['width'])
    row_height = Inches(0.5)
    table_height = Inches(min(num_rows * 0.5, SAFE_ZONE['h'] - 0.3))

    table_shape = slide.shapes.add_table(
        num_rows, num_cols,
        Inches(SAFE_ZONE['left']),
        Inches(SAFE_ZONE['y'] + 0.2),
        table_width,
        table_height
    )
    table = table_shape.table

    # Style header row
    for j, header in enumerate(headers):
        cell = table.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = accent_color

        tf = cell.text_frame
        tf.clear()
        tf.anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.font.name = "Arial"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = WHITE
        run = p.add_run()
        run.text = header
        run.font.name = "Arial"
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = WHITE

    # Style data rows
    for i, row_data in enumerate(rows):
        for j, cell_text in enumerate(row_data):
            cell = table.cell(i + 1, j)

            # Alternating row colors
            if i % 2 == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = WHITE
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = GREY_5

            tf = cell.text_frame
            tf.clear()
            tf.anchor = MSO_ANCHOR.MIDDLE
            p = tf.paragraphs[0]
            p.font.name = "Arial"
            p.font.size = Pt(11)
            p.font.color.rgb = DARK_BLUE
            run = p.add_run()
            run.text = str(cell_text)
            run.font.name = "Arial"
            run.font.size = Pt(11)
            run.font.color.rgb = DARK_BLUE

    return slide


def add_quote_box(slide, quote, attribution=None, y_offset=0):
    """
    Quote with accent left border.
    Anthropic pattern: large quote, accent border, attribution below.
    """
    box_width = Inches(9.0)
    box_height = Inches(2.5)
    x = Inches(SAFE_ZONE['left'] + 1.0)
    y = Inches(SAFE_ZONE['y'] + 0.5 + y_offset)

    # Accent border (left side bar)
    border = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        x - Inches(0.15),
        y,
        Inches(0.08),
        box_height
    )
    border.fill.solid()
    border.fill.fore_color.rgb = PACIFIC_BLUE
    border.line.fill.background()

    # Quote text
    quote_box = slide.shapes.add_textbox(x + Inches(0.1), y + Inches(0.2),
                                         box_width, box_height - Inches(0.6))
    quote_box.text_frame.word_wrap = True
    set_text_formatting(quote_box, f'"{quote}"', "Arial", Pt(20),
                       italic=True, color=DARK_BLUE)

    # Attribution
    if attribution:
        attr_box = slide.shapes.add_textbox(x + Inches(0.1), y + box_height - Inches(0.5),
                                            box_width, Inches(0.4))
        set_text_formatting(attr_box, f"— {attribution}", "Arial", Pt(14),
                           color=BLUE_GRAY)

    return slide


def add_highlight_stat(slide, stats, y_offset=0):
    """
    Large highlighted statistics.
    Anthropic pattern: big numbers with accent color, description below.

    stats: list of {'value': str, 'label': str}
    """
    num_stats = len(stats)
    stat_width = Inches(SAFE_ZONE['width'] / num_stats)
    y = Inches(SAFE_ZONE['y'] + 0.5 + y_offset)

    for i, stat in enumerate(stats):
        x = Inches(SAFE_ZONE['left']) + stat_width * i

        # Large value
        value_box = slide.shapes.add_textbox(x, y, stat_width, Inches(1.0))
        set_text_formatting(value_box, stat['value'], "KPMG Bold", Pt(60),
                           bold=True, color=PACIFIC_BLUE, alignment=PP_ALIGN.CENTER)

        # Label below
        label_box = slide.shapes.add_textbox(x, y + Inches(1.0), stat_width, Inches(0.6))
        label_box.text_frame.word_wrap = True
        set_text_formatting(label_box, stat['label'], "Arial", Pt(14),
                           color=DARK_BLUE, alignment=PP_ALIGN.CENTER)

    return slide


def add_icon_list(slide, items, y_offset=0):
    """
    List with accent icons/checkmarks.
    Anthropic pattern: clean list with visual markers.

    items: list of {'icon': str (optional, default checkmark), 'text': str}
    """
    y = Inches(SAFE_ZONE['y'] + 0.3 + y_offset)
    item_height = Inches(0.6)

    for i, item in enumerate(items):
        item_y = y + item_height * i

        # Icon circle
        icon = slide.shapes.add_shape(
            MSO_SHAPE.OVAL,
            Inches(SAFE_ZONE['left']),
            item_y,
            Inches(0.35), Inches(0.35)
        )
        icon.fill.solid()
        icon.fill.fore_color.rgb = PACIFIC_BLUE
        icon.line.fill.background()

        # Icon text (checkmark or custom)
        tf = icon.text_frame
        tf.clear()
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = item.get('icon', '✓')
        run.font.name = "Arial"
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = WHITE
        tf.anchor = MSO_ANCHOR.MIDDLE

        # Item text
        text_box = slide.shapes.add_textbox(
            Inches(SAFE_ZONE['left'] + 0.5),
            item_y,
            Inches(SAFE_ZONE['width'] - 0.5),
            Inches(0.5)
        )
        text_box.text_frame.word_wrap = True
        set_text_formatting(text_box, item['text'], "Arial", Pt(16),
                           color=DARK_BLUE)

    return slide


def add_comparison_boxes(slide, left_box, right_box):
    """
    Side-by-side comparison boxes with accent headers.
    Anthropic pattern: clear visual comparison, accent differentiation.

    left_box/right_box: {'title': str, 'items': list, 'accent': RGBColor (optional)}
    """
    box_width = Inches(5.0)
    box_height = Inches(4.0)
    gap = Inches(0.5)

    left_x = Inches(SAFE_ZONE['left'])
    right_x = Inches(SAFE_ZONE['left']) + box_width + gap
    y = Inches(SAFE_ZONE['y'] + 0.2)

    for i, box_data in enumerate([left_box, right_box]):
        x = left_x if i == 0 else right_x
        accent = box_data.get('accent', PACIFIC_BLUE if i == 0 else AQUA)

        # Header bar
        header = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            x, y,
            box_width, Inches(0.5)
        )
        header.fill.solid()
        header.fill.fore_color.rgb = accent
        header.line.fill.background()

        # Header text
        header_text = slide.shapes.add_textbox(x, y + Inches(0.08), box_width, Inches(0.4))
        set_text_formatting(header_text, box_data['title'], "Arial", Pt(16),
                           bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)

        # Content box
        content = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            x, y + Inches(0.5),
            box_width, box_height - Inches(0.5)
        )
        content.fill.solid()
        content.fill.fore_color.rgb = GREY_5
        content.line.color.rgb = accent
        content.line.width = Pt(1)

        # Content text
        content_box = slide.shapes.add_textbox(
            x + Inches(0.2), y + Inches(0.7),
            box_width - Inches(0.4), box_height - Inches(0.9)
        )
        content_box.text_frame.word_wrap = True
        add_bullet_text(content_box.text_frame, box_data['items'])

    return slide


# =============================================================================
# DEMONSTRATION - Creates sample presentation
# =============================================================================

def create_demo_presentation(template_path, output_path):
    """Create a demonstration presentation showing all components."""
    print(f"Loading template: {template_path}")
    prs = Presentation(template_path)

    # Remove DRAFT watermark if present
    for master in prs.slide_masters:
        for shape in list(master.shapes):
            if hasattr(shape, 'text') and 'DRAFT' in shape.text.upper():
                sp = shape._element
                sp.getparent().remove(sp)

    print("Creating slides...")

    # 1. Cover
    add_cover_slide(prs, "Creative Toolkit Demo", "Anthropic-Inspired Patterns with KPMG Colors")

    # 2. Section: Layouts
    add_section_divider(prs, "Layout Patterns")

    # 3. Three-column cards
    slide = prepare_content_slide(prs, "Three Key Priorities")
    add_three_column_cards(slide, [
        {'title': 'Digital Transformation',
         'body': 'Modernize core systems and processes to improve operational efficiency and customer experience.'},
        {'title': 'Market Expansion',
         'body': 'Enter three new geographic markets through strategic partnerships and localized offerings.'},
        {'title': 'Talent Development',
         'body': 'Invest in upskilling programs to build leadership pipeline and retain top performers.'}
    ])

    # 4. Two-column layout
    slide = prepare_content_slide(prs, "Current State vs Future State")
    add_two_column_text(slide,
        left_content=[
            "Manual processes across departments",
            "Siloed data in legacy systems",
            "Reactive customer service model",
            "Limited analytics capabilities"
        ],
        right_content=[
            "Automated end-to-end workflows",
            "Unified data platform",
            "Proactive customer engagement",
            "AI-powered insights and predictions"
        ],
        left_title="Current State",
        right_title="Future State"
    )

    # 5. Section: Data & Stats
    add_section_divider(prs, "Data & Statistics")

    # 6. Highlight stats
    slide = prepare_content_slide(prs, "Key Performance Indicators")
    add_highlight_stat(slide, [
        {'value': '47%', 'label': 'Increase in operational efficiency'},
        {'value': '3.2x', 'label': 'Return on investment'},
        {'value': '89', 'label': 'Net Promoter Score'}
    ])

    # 7. Table
    slide = prepare_content_slide(prs, "Competitive Analysis")
    add_accent_table(slide,
        headers=['Dimension', 'Company A', 'Company B', 'Our Position'],
        rows=[
            ['Market Share', '35%', '28%', '22%'],
            ['Growth Rate', '8%', '12%', '18%'],
            ['Customer NPS', '42', '38', '56'],
            ['Innovation Index', 'Medium', 'High', 'High'],
            ['Cost Position', 'Low', 'Medium', 'Medium']
        ]
    )

    # 8. Section: Qualitative
    add_section_divider(prs, "Qualitative Elements")

    # 9. Quote
    slide = prepare_content_slide(prs, "Leadership Perspective")
    add_quote_box(slide,
        "The greatest danger in times of turbulence is not the turbulence itself, but to act with yesterday's logic.",
        "Peter Drucker"
    )

    # 10. Icon list
    slide = prepare_content_slide(prs, "Implementation Checklist")
    add_icon_list(slide, [
        {'text': 'Complete stakeholder alignment sessions'},
        {'text': 'Finalize technology vendor selection'},
        {'text': 'Develop detailed project timeline'},
        {'text': 'Establish governance framework'},
        {'text': 'Launch pilot program in Q2'},
        {'text': 'Scale successful pilots enterprise-wide'}
    ])

    # 11. Comparison boxes
    slide = prepare_content_slide(prs, "Build vs Buy Analysis")
    add_comparison_boxes(slide,
        left_box={
            'title': 'Build In-House',
            'items': [
                'Full customization to requirements',
                'Complete ownership of IP',
                'Higher upfront investment',
                'Longer time to market',
                'Requires specialized talent'
            ],
            'accent': BLUE_GRAY
        },
        right_box={
            'title': 'Buy Solution',
            'items': [
                'Faster deployment timeline',
                'Proven, battle-tested solution',
                'Predictable licensing costs',
                'Vendor dependency risk',
                'May require customization'
            ],
            'accent': PACIFIC_BLUE
        }
    )

    # 12. Back cover
    add_back_cover(prs)

    # Save
    prs.save(output_path)
    print(f"\nPresentation saved to: {output_path}")
    print("\nSlides created:")
    print("1. Cover")
    print("2. Section: Layout Patterns")
    print("3. Three-column cards")
    print("4. Two-column layout")
    print("5. Section: Data & Statistics")
    print("6. Highlight stats")
    print("7. Accent table")
    print("8. Section: Qualitative Elements")
    print("9. Quote box")
    print("10. Icon list")
    print("11. Comparison boxes")
    print("12. Back cover")


if __name__ == "__main__":
    TEMPLATE_PATH = os.path.expanduser(
        "~/Library/Mobile Documents/com~apple~CloudDocs/claude-code/templates/kpmg/KPMG-2022/template-clean.pptx"
    )
    OUTPUT_PATH = os.path.expanduser("~/Desktop/KPMG_Creative_Toolkit_Demo.pptx")

    create_demo_presentation(TEMPLATE_PATH, OUTPUT_PATH)

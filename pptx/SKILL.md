---
name: pptx
description: "Presentation creation, editing, and analysis. When Claude needs to work with presentations (.pptx files) for: (1) Creating new presentations, (2) Modifying or editing content, (3) Working with layouts, (4) Adding comments or speaker notes, or any other presentation tasks. Also triggers on: KPMG presentation, KPMG slides, KPMG format, KPMG PowerPoint, KPMG branded"
license: Proprietary. LICENSE.txt has complete terms
---

# PPTX creation, editing, and analysis

## Overview

A user may ask you to create, edit, or analyze the contents of a .pptx file. A .pptx file is essentially a ZIP archive containing XML files and other resources that you can read or edit. You have different tools and workflows available for different tasks.

## KPMG Presentations (IMPORTANT - READ FIRST)

### Three Approaches

**Approach 1: Simple (Placeholder-Only)** — For straightforward bullet-point content
- Use python-pptx with template placeholders only
- Fast, but limited to simple bulleted text in body area
- Results look "dull" - just text in boxes

**Approach 2: python-pptx Shapes (Template + Creative Content)** — For moderate visual sophistication
- Use python-pptx with KPMG template (preserves logo, footers, masters)
- Template placeholder for title only
- python-pptx `add_shape()`, `add_table()`, `add_textbox()` for body content
- Use `kpmg_creative_toolkit.py` for pre-built patterns
- Limited by python-pptx's shape capabilities

**Approach 3: Shape Transplant (RECOMMENDED)** — For maximum visual impact
- Combines PptxGenJS creative power with KPMG template branding
- python-pptx creates slide from template (preserves logo, footers, masters)
- PptxGenJS creates creative content (cards, stats, tables, etc.)
- **Transplant shapes** from PptxGenJS slide into template slide
- Best of both worlds: full PptxGenJS/html2pptx creativity + full template branding

```
Template (python-pptx)          PptxGenJS
┌─────────────────────┐         ┌─────────────────────┐
│ KPMG Logo    Footer │         │  ┌───┐ ┌───┐ ┌───┐ │
│ ─────────────────── │    +    │  │   │ │   │ │   │ │  →  Combined
│ Title placeholder   │         │  └───┘ └───┘ └───┘ │
│ [body area empty]   │         │  Stats, tables...  │
└─────────────────────┘         └─────────────────────┘
```

### Rules for KPMG Presentations

**ALWAYS:**
- ✅ Use python-pptx to load KPMG template (preserves branding)
- ✅ Use template layouts for cover, section dividers, back cover
- ✅ Use template placeholder for title (idx 0)
- ✅ Use KPMG typography (KPMG Bold for titles, Arial for body)
- ✅ Use ONLY KPMG colors in all elements (see color list below)
- ✅ Read the template's config.yaml for settings

**FOR CREATIVE CONTENT (Shape Transplant - RECOMMENDED):**
- ✅ Create content slides with PptxGenJS (full creative freedom)
- ✅ Transplant shapes into template slides (see workflow below)
- ✅ Position content in body safe zone (Y: 1.07" to 6.17")
- ✅ Use KPMG colors in PptxGenJS (hex without #: `0C233C`, `00B8F5`)

**FOR SIMPLE CONTENT (python-pptx only):**
- ✅ Use `kpmg_creative_toolkit.py` for pre-built patterns
- ✅ Use python-pptx `add_shape()`, `add_table()`, `add_textbox()`
- ✅ Clear body placeholder (idx 10) before adding custom shapes

**DO NOT:**
- ❌ Do NOT use PptxGenJS alone (loses template branding)
- ❌ Do NOT use non-KPMG colors
- ❌ Do NOT cover template footer/logo areas
- ❌ Do NOT search for templates (use the fixed paths below)
- ❌ **NEVER edit template XML directly** — corrupts file structure

### KPMG Templates Location
```
~/Library/Mobile Documents/com~apple~CloudDocs/claude-code/templates/kpmg/
```

**Available templates:**
| Template | Path | Use For |
|----------|------|---------|
| KPMG 2022 | `KPMG-2022/template-clean.pptx` | Standard KPMG presentations |

Each template folder contains:
- `template-clean.pptx` - The PowerPoint template (0 slides, 13 layouts)
- `config.yaml` - Typography, colors, layouts, placeholder indices

**Read config.yaml first** to get the correct settings for that template.

### KPMG Font Installation

KPMG fonts must be installed for presentations to render correctly:

```bash
# Font files are synced via iCloud at:
~/Library/Mobile Documents/com~apple~CloudDocs/claude-code/templates/kpmg/KPMG-2022/

# Install to user fonts:
cp ~/Library/Mobile\ Documents/com~apple~CloudDocs/claude-code/templates/kpmg/KPMG-2022/*.ttf ~/Library/Fonts/
```

**Required fonts**: KPMG-Bold.ttf, KPMG-Light.ttf, KPMG-Regular.ttf

### KPMG Theme Installation for PowerPoint

To use KPMG themes in PowerPoint itself (for manual editing after generation):

```bash
# Theme file location:
~/Library/Mobile Documents/com~apple~CloudDocs/claude-code/templates/kpmg/KPMG-2022/KPMG\ Theme.thmx

# Install to PowerPoint themes folder:
cp "~/Library/Mobile Documents/com~apple~CloudDocs/claude-code/templates/kpmg/KPMG-2022/KPMG Theme.thmx" \
   ~/Library/Group\ Containers/UBF8T346G9.Office/User\ Content/Themes/
```

**Note**: To remove DRAFT watermark from theme, edit the `slideMaster1.xml` inside the .thmx file.

### Reference Scripts
Complete working scripts are available at:
```
skills/pptx/scripts/kpmg_reference.py          # Simple placeholder-only approach
skills/pptx/scripts/kpmg_creative_toolkit.py   # Hybrid with Anthropic-inspired patterns
```

**Creative Toolkit Components** (Anthropic-inspired, KPMG colors):
| Function | Use For |
|----------|---------|
| `add_three_column_cards()` | Key priorities, pillars, phases |
| `add_two_column_text()` | Current/future state, comparisons |
| `add_highlight_stat()` | KPIs, big numbers with labels |
| `add_accent_table()` | Data tables with accent header |
| `add_quote_box()` | Leadership quotes, testimonials |
| `add_icon_list()` | Checklists, action items |
| `add_comparison_boxes()` | Build vs buy, pros/cons |

Copy and adapt these scripts rather than writing from scratch.

### Visual Variety Patterns (CRITICAL for Engaging Presentations)

**Problem Solved**: The "Shape Transplant" approach alone produces monotonous presentations - same bullet pattern on every slide. The original PptxGenJS presentations had visual variety that was lost.

**Solution**: Match content type to visual pattern. Don't just use bullet lists for everything.

**Pattern Catalog** (documented in Obsidian Core vault: `2026-01-25 KPMG Presentation Visual Variety Patterns.md`):

| Content Type | Pattern to Use | Function |
|--------------|----------------|----------|
| Agenda/TOC with 4-6 items | Numbered list with colored circles | `add_numbered_list()` |
| Can/Can't do lists | Green ✓ / Red ✗ checklist | `add_checklist()` |
| Old vs New / Current vs Future | Two-column with accent headers | `add_two_column_comparison()` |
| Quotes with attribution | Quote box with Pacific Blue accent bar | `add_quote_box()` |
| Data comparisons | Accent table with dark blue header | `add_accent_table()` |
| 3 key points/phases/priorities | Three-column cards with numbered circles | `add_three_column_cards()` |
| Key statistics/KPIs | Large highlight numbers | `add_highlight_stat()` |
| Section dividers | Dark blue background + numbered circle | `add_section_divider(section_number=N)` |
| Images with context | Image + text side by side | `add_image_with_text()` |
| Standard bullets | Accent bar + bullet list | `add_bullet_slide()` |

**Key Learnings from Lakehouse Presentation (Jan 2026)**:

1. **Extract images from source**: Unzip the original PPTX, images are in `ppt/media/`. Copy them to workspace for embedding.

2. **Content-type detection**: Before creating each slide, identify the content type:
   - Lists with numbers → numbered list pattern
   - Yes/No items → checklist pattern
   - Comparisons → two-column pattern
   - Quotes → quote box pattern
   - Tables → accent table pattern

3. **Section dividers with numbers**: Use numbered circles (1, 2, 3...) on section dividers to help audience track progress through presentation.

4. **Embed images properly**: Use `slide.shapes.add_picture(path, x, y, width=Inches(N))` - don't leave as raw wikilinks or markdown.

5. **Reference documentation**: See Obsidian Core vault `2026-01-25 KPMG Presentation Visual Variety Patterns.md` for documented learnings. The `kpmg_creative_toolkit.py` script in this skill contains the base patterns.

### Vault Documentation Cross-References

Detailed learnings from KPMG presentation projects are documented in the Obsidian Core vault:
- `2026-01-25 KPMG Presentation Visual Variety Patterns.md` - Pattern catalog and technical learnings
- `KPMG PowerPoint Workflow Guide.md` - Full workflow, color codes, typography specs, bugs to avoid

Always check these vault notes for the latest learnings before starting a KPMG presentation project.

### Shape Transplant Workflow (RECOMMENDED)

This approach gives you PptxGenJS's full creative power while preserving KPMG template branding.

**Step 1: Create template slide with python-pptx**
```python
from pptx import Presentation
from pptx.util import Pt
from pptx.dml.color import RGBColor
from copy import deepcopy

TEMPLATE = "~/...claude-code/templates/kpmg/KPMG-2022/template-clean.pptx"
template_prs = Presentation(TEMPLATE)
layout = template_prs.slide_layouts[3]  # One column
slide = template_prs.slides.add_slide(layout)

# Set title using template placeholder
title_ph = slide.placeholders[0]
title_ph.text = "Slide Title Here"
for p in title_ph.text_frame.paragraphs:
    p.font.name = "KPMG Bold"
    p.font.size = Pt(44)
    p.font.color.rgb = RGBColor(12, 35, 60)
```

**Step 2: Create creative content with PptxGenJS**
```javascript
const pptxgen = require('pptxgenjs');
const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';
const slide = pptx.addSlide();

// Position content for KPMG body area (below title)
// Safe zone: X: 1.07", Y: 1.2" to 6.17", Width: 11.0"

// Three-column cards
const cards = [
    { title: 'Card 1', color: '0C233C', items: ['Item A', 'Item B'] },
    { title: 'Card 2', color: '34556D', items: ['Item C', 'Item D'] },
    { title: 'Card 3', color: '00338D', items: ['Item E', 'Item F'] }
];

cards.forEach((card, i) => {
    const x = 1.07 + (3.5 * i);
    slide.addShape('rect', { x, y: 1.3, w: 3.4, h: 2.5, fill: { color: card.color } });
    slide.addText(card.title, { x: x + 0.2, y: 1.4, w: 3.0, h: 0.4, fontSize: 18, bold: true, color: 'FFFFFF' });
    card.items.forEach((item, j) => {
        slide.addText('• ' + item, { x: x + 0.2, y: 1.9 + (j * 0.4), w: 3.0, h: 0.3, fontSize: 14, color: 'FFFFFF' });
    });
});

pptx.writeFile({ fileName: 'creative_content.pptx' });
```

**Step 3: Transplant shapes into template slide**
```python
# Load the PptxGenJS output
creative_prs = Presentation("creative_content.pptx")
creative_slide = creative_prs.slides[0]

# Transplant all shapes from creative slide to template slide
for shape in creative_slide.shapes:
    new_shape = deepcopy(shape._element)
    slide.shapes._spTree.append(new_shape)

template_prs.save("output.pptx")
```

**Result:** KPMG logo, footer, and master styles preserved + PptxGenJS creative content.

### Example Prompt That Works
```
Create a KPMG presentation using the KPMG-2022 template from [source file].
Use the Shape Transplant approach for visually rich slides.
```

### KPMG Quick Workflow

1. **Load template** with python-pptx
2. **Add slides at END** using template layouts (never delete during session)
3. **Use try/except for placeholders**: Never use `if X in slide.placeholders:` (broken)
4. **Set ALL font properties at BOTH levels** (paragraph + run) including `italic=False`
5. **For section dividers**: Use Layout 1, set `slide.background.fill` to dark blue
6. **Save presentation**
7. **Validate visually**: Generate thumbnails with `python scripts/thumbnail.py output.pptx` and inspect for layout issues

**Note:** KPMG-2022 template is empty (0 slides), so no post-processing needed to remove template slides.

### KPMG Layout Reference (KPMG-2022: 13 layouts, indices 0-12)
| Layout | Use For |
|--------|---------|
| 0 | Cover |
| 1 | Section dividers (set background to dark blue #0C233C) |
| 3 | One column content (placeholders: title=0, body=10) |
| 4 | Two column content (placeholders: title=0, left=10, right=11) |
| 5 | Back cover |

### KPMG Content Safe Zone (for Hybrid approach)
```
Title area:     Y = 0.48" to 1.07"   ← Use template placeholder (idx 0)
Content area:   Y = 1.07" to 6.43"   ← CREATIVE ZONE (no strapline - starts here)
Footer area:    Y = 6.43" to 7.50"   ← Reserved for template master

Left margin:   1.07"
Right edge:    12.25"
Content width: 11.18"
```

**Note:** No strapline - cleaner, modern design (Anthropic-inspired). Clear placeholder idx 18 if present.

### KPMG Colors for Creative Elements
When adding shapes/tables in the content area, use ONLY these colors:

```python
# python-pptx RGBColor definitions
from pptx.dml.color import RGBColor

# Primary
DARK_BLUE = RGBColor(12, 35, 60)       # 0C233C - Backgrounds, titles
PACIFIC_BLUE = RGBColor(0, 184, 245)   # 00B8F5 - Accents, straplines
KPMG_BLUE = RGBColor(0, 51, 141)       # 00338D - Links, secondary accents

# Charts / Callouts
BLUE_GRAY = RGBColor(52, 85, 109)      # 34556D - Series 1
AQUA = RGBColor(119, 168, 190)         # 77A8BE - Series 2
LIGHT_TURQUOISE = RGBColor(150, 206, 228)  # 96CEE4 - Series 3
BLUE_ACCENT_1 = RGBColor(210, 219, 249)    # D2DBF9 - Series 4
BLUE = RGBColor(118, 210, 255)         # 76D2FF - Series 5

# Utility
GREY_5 = RGBColor(229, 229, 229)       # E5E5E5 - Backgrounds, dividers
LIGHT_BLUE = RGBColor(172, 234, 255)   # ACEAFF - Light backgrounds (sparingly)
WHITE = RGBColor(255, 255, 255)

# RAG only
RED = RGBColor(237, 33, 36)            # ED2124
YELLOW = RGBColor(241, 196, 77)        # F1C44D
GREEN = RGBColor(38, 153, 36)          # 269924
```

### KPMG Typography
| Element | Font | Size | Color | Notes |
|---------|------|------|-------|-------|
| Cover title | KPMG Bold | 88pt | White | |
| Content titles | KPMG Bold | 44pt | Dark Blue #0C233C | |
| Body | Arial | 16pt | Default | |
| Section dividers | KPMG Bold | 66pt | White on Dark Blue | |
| Accent text | Arial | 16pt | Pacific Blue #00B8F5 | For emphasis |

**Note:** No strapline - cleaner, modern design.

See "KPMG Template-Specific Notes" section below for full details.

## Reading and analyzing content

### Text extraction
If you just need to read the text contents of a presentation, you should convert the document to markdown:

```bash
# Convert document to markdown
python -m markitdown path-to-file.pptx
```

### Raw XML access
You need raw XML access for: comments, speaker notes, slide layouts, animations, design elements, and complex formatting. For any of these features, you'll need to unpack a presentation and read its raw XML contents.

#### Unpacking a file
`python ooxml/scripts/unpack.py <office_file> <output_dir>`

**Note**: The unpack.py script is located at `skills/pptx/ooxml/scripts/unpack.py` relative to the project root. If the script doesn't exist at this path, use `find . -name "unpack.py"` to locate it.

#### Key file structures
* `ppt/presentation.xml` - Main presentation metadata and slide references
* `ppt/slides/slide{N}.xml` - Individual slide contents (slide1.xml, slide2.xml, etc.)
* `ppt/notesSlides/notesSlide{N}.xml` - Speaker notes for each slide
* `ppt/comments/modernComment_*.xml` - Comments for specific slides
* `ppt/slideLayouts/` - Layout templates for slides
* `ppt/slideMasters/` - Master slide templates
* `ppt/theme/` - Theme and styling information
* `ppt/media/` - Images and other media files

#### Typography and color extraction
**When given an example design to emulate**: Always analyze the presentation's typography and colors first using the methods below:
1. **Read theme file**: Check `ppt/theme/theme1.xml` for colors (`<a:clrScheme>`) and fonts (`<a:fontScheme>`)
2. **Sample slide content**: Examine `ppt/slides/slide1.xml` for actual font usage (`<a:rPr>`) and colors
3. **Search for patterns**: Use grep to find color (`<a:solidFill>`, `<a:srgbClr>`) and font references across all XML files

## Creating a new PowerPoint presentation **without a template**

There are two approaches for creating presentations from scratch:

### Option A: Direct PptxGenJS Approach (For NON-branded presentations only)

**WARNING: Do NOT use for KPMG or other branded presentations.** PptxGenJS creates from scratch and cannot use existing templates with fonts/masters/logos. For KPMG, see "KPMG Presentations" section above.

When you have structured content with speaker notes and NO branding requirements, use PptxGenJS directly with a type-based slide system.

**When to use this approach:**
- NO corporate branding required (no KPMG, no templates)
- Content comes from markdown with clear slide structure
- Speaker notes are a primary requirement
- Slides follow repeatable patterns (title, bullets, two-column, quote, etc.)

**Architecture:**
```javascript
const pptxgen = require('pptxgenjs');

// Define slides as typed objects
const slides = [
  { type: 'title', title: 'Main Title', subtitle: 'Subtitle', notes: 'Speaker notes here...' },
  { type: 'bullets', title: 'Agenda', items: [...], notes: '...' },
  { type: 'twoColumn', title: '...', leftItems: [...], rightItems: [...], notes: '...' },
  { type: 'section', number: 'PART 1', title: 'SECTION NAME', notes: '' },
  // ... more slides
];

// Switch-based renderer
function addSlide(pptx, data, idx) {
  const slide = pptx.addSlide();
  if (data.notes) slide.addNotes(data.notes);  // Add speaker notes

  switch (data.type) {
    case 'title':
      slide.background = { color: '1C2833' };
      slide.addText(data.title, { x: 0.5, y: 1.5, w: 9, h: 1.5, fontSize: 28, bold: true, color: 'FFFFFF' });
      break;
    case 'bullets':
      // ... bullet layout
      break;
    // ... other types
  }
}

// Generate presentation
const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';
slides.forEach((s, i) => addSlide(pptx, s, i));
pptx.writeFile({ fileName: 'output.pptx' });
```

**Common slide types to implement:**
- `title` - Opening slide with title, subtitle, footer
- `section` - Section divider with part number and title
- `bullets` - Numbered or bulleted list with descriptions
- `twoColumn` - Side-by-side comparison
- `table` - Data in table format with headers
- `quote` / `bigQuote` - Quotation with attribution
- `comparison` - Old vs New / Before vs After layouts
- `timeline` - Phased timeline with periods
- `closing` - Final slide with call to action

**Speaker Notes:**
Use `slide.addNotes(text)` to add speaker notes. Notes support multiline strings:
```javascript
slide.addNotes('First paragraph of notes.\n\nSecond paragraph with more detail.');
```

### Option B: html2pptx Workflow (For complex visual designs)

When creating a new PowerPoint presentation from scratch, use the **html2pptx** workflow to convert HTML slides to PowerPoint with accurate positioning.

### Design Principles

**CRITICAL**: Before creating any presentation, analyze the content and choose appropriate design elements:
1. **Consider the subject matter**: What is this presentation about? What tone, industry, or mood does it suggest?
2. **Check for branding**: If the user mentions a company/organization, consider their brand colors and identity
3. **Match palette to content**: Select colors that reflect the subject
4. **State your approach**: Explain your design choices before writing code

**Requirements**:
- ✅ State your content-informed design approach BEFORE writing code
- ✅ Use web-safe fonts only: Arial, Helvetica, Times New Roman, Georgia, Courier New, Verdana, Tahoma, Trebuchet MS, Impact
- ✅ Create clear visual hierarchy through size, weight, and color
- ✅ Ensure readability: strong contrast, appropriately sized text, clean alignment
- ✅ Be consistent: repeat patterns, spacing, and visual language across slides

#### Color Palette Selection

**Choosing colors creatively**:
- **Think beyond defaults**: What colors genuinely match this specific topic? Avoid autopilot choices.
- **Consider multiple angles**: Topic, industry, mood, energy level, target audience, brand identity (if mentioned)
- **Be adventurous**: Try unexpected combinations - a healthcare presentation doesn't have to be green, finance doesn't have to be navy
- **Build your palette**: Pick 3-5 colors that work together (dominant colors + supporting tones + accent)
- **Ensure contrast**: Text must be clearly readable on backgrounds

**Example color palettes** (use these to spark creativity - choose one, adapt it, or create your own):

1. **Classic Blue**: Deep navy (#1C2833), slate gray (#2E4053), silver (#AAB7B8), off-white (#F4F6F6)
2. **Teal & Coral**: Teal (#5EA8A7), deep teal (#277884), coral (#FE4447), white (#FFFFFF)
3. **Bold Red**: Red (#C0392B), bright red (#E74C3C), orange (#F39C12), yellow (#F1C40F), green (#2ECC71)
4. **Warm Blush**: Mauve (#A49393), blush (#EED6D3), rose (#E8B4B8), cream (#FAF7F2)
5. **Burgundy Luxury**: Burgundy (#5D1D2E), crimson (#951233), rust (#C15937), gold (#997929)
6. **Deep Purple & Emerald**: Purple (#B165FB), dark blue (#181B24), emerald (#40695B), white (#FFFFFF)
7. **Cream & Forest Green**: Cream (#FFE1C7), forest green (#40695B), white (#FCFCFC)
8. **Pink & Purple**: Pink (#F8275B), coral (#FF574A), rose (#FF737D), purple (#3D2F68)
9. **Lime & Plum**: Lime (#C5DE82), plum (#7C3A5F), coral (#FD8C6E), blue-gray (#98ACB5)
10. **Black & Gold**: Gold (#BF9A4A), black (#000000), cream (#F4F6F6)
11. **Sage & Terracotta**: Sage (#87A96B), terracotta (#E07A5F), cream (#F4F1DE), charcoal (#2C2C2C)
12. **Charcoal & Red**: Charcoal (#292929), red (#E33737), light gray (#CCCBCB)
13. **Vibrant Orange**: Orange (#F96D00), light gray (#F2F2F2), charcoal (#222831)
14. **Forest Green**: Black (#191A19), green (#4E9F3D), dark green (#1E5128), white (#FFFFFF)
15. **Retro Rainbow**: Purple (#722880), pink (#D72D51), orange (#EB5C18), amber (#F08800), gold (#DEB600)
16. **Vintage Earthy**: Mustard (#E3B448), sage (#CBD18F), forest green (#3A6B35), cream (#F4F1DE)
17. **Coastal Rose**: Old rose (#AD7670), beaver (#B49886), eggshell (#F3ECDC), ash gray (#BFD5BE)
18. **Orange & Turquoise**: Light orange (#FC993E), grayish turquoise (#667C6F), white (#FCFCFC)

#### Visual Details Options

**Geometric Patterns**:
- Diagonal section dividers instead of horizontal
- Asymmetric column widths (30/70, 40/60, 25/75)
- Rotated text headers at 90° or 270°
- Circular/hexagonal frames for images
- Triangular accent shapes in corners
- Overlapping shapes for depth

**Border & Frame Treatments**:
- Thick single-color borders (10-20pt) on one side only
- Double-line borders with contrasting colors
- Corner brackets instead of full frames
- L-shaped borders (top+left or bottom+right)
- Underline accents beneath headers (3-5pt thick)

**Typography Treatments**:
- Extreme size contrast (72pt headlines vs 11pt body)
- All-caps headers with wide letter spacing
- Numbered sections in oversized display type
- Monospace (Courier New) for data/stats/technical content
- Condensed fonts (Arial Narrow) for dense information
- Outlined text for emphasis

**Chart & Data Styling**:
- Monochrome charts with single accent color for key data
- Horizontal bar charts instead of vertical
- Dot plots instead of bar charts
- Minimal gridlines or none at all
- Data labels directly on elements (no legends)
- Oversized numbers for key metrics

**Layout Innovations**:
- Full-bleed images with text overlays
- Sidebar column (20-30% width) for navigation/context
- Modular grid systems (3×3, 4×4 blocks)
- Z-pattern or F-pattern content flow
- Floating text boxes over colored shapes
- Magazine-style multi-column layouts

**Background Treatments**:
- Solid color blocks occupying 40-60% of slide
- Gradient fills (vertical or diagonal only)
- Split backgrounds (two colors, diagonal or vertical)
- Edge-to-edge color bands
- Negative space as a design element

### Layout Tips
**When creating slides with charts or tables:**
- **Two-column layout (PREFERRED)**: Use a header spanning the full width, then two columns below - text/bullets in one column and the featured content in the other. This provides better balance and makes charts/tables more readable. Use flexbox with unequal column widths (e.g., 40%/60% split) to optimize space for each content type.
- **Full-slide layout**: Let the featured content (chart/table) take up the entire slide for maximum impact and readability
- **NEVER vertically stack**: Do not place charts/tables below text in a single column - this causes poor readability and layout issues

### Workflow
1. **MANDATORY - READ ENTIRE FILE**: Read [`html2pptx.md`](html2pptx.md) completely from start to finish. **NEVER set any range limits when reading this file.** Read the full file content for detailed syntax, critical formatting rules, and best practices before proceeding with presentation creation.
2. Create an HTML file for each slide with proper dimensions (e.g., 720pt × 405pt for 16:9)
   - Use `<p>`, `<h1>`-`<h6>`, `<ul>`, `<ol>` for all text content
   - Use `class="placeholder"` for areas where charts/tables will be added (render with gray background for visibility)
   - **CRITICAL**: Rasterize gradients and icons as PNG images FIRST using Sharp, then reference in HTML
   - **LAYOUT**: For slides with charts/tables/images, use either full-slide layout or two-column layout for better readability
3. Create and run a JavaScript file using the [`html2pptx.js`](scripts/html2pptx.js) library to convert HTML slides to PowerPoint and save the presentation
   - Use the `html2pptx()` function to process each HTML file
   - Add charts and tables to placeholder areas using PptxGenJS API
   - Save the presentation using `pptx.writeFile()`
4. **Visual validation**: Generate thumbnails and inspect for layout issues
   - Create thumbnail grid: `python scripts/thumbnail.py output.pptx workspace/thumbnails --cols 4`
   - Read and carefully examine the thumbnail image for:
     - **Text cutoff**: Text being cut off by header bars, shapes, or slide edges
     - **Text overlap**: Text overlapping with other text or shapes
     - **Positioning issues**: Content too close to slide boundaries or other elements
     - **Contrast issues**: Insufficient contrast between text and backgrounds
   - If issues found, adjust HTML margins/spacing/colors and regenerate the presentation
   - Repeat until all slides are visually correct

## Editing an existing PowerPoint presentation

When edit slides in an existing PowerPoint presentation, you need to work with the raw Office Open XML (OOXML) format. This involves unpacking the .pptx file, editing the XML content, and repacking it.

### Workflow
1. **MANDATORY - READ ENTIRE FILE**: Read [`ooxml.md`](ooxml.md) (~500 lines) completely from start to finish.  **NEVER set any range limits when reading this file.**  Read the full file content for detailed guidance on OOXML structure and editing workflows before any presentation editing.
2. Unpack the presentation: `python ooxml/scripts/unpack.py <office_file> <output_dir>`
3. Edit the XML files (primarily `ppt/slides/slide{N}.xml` and related files)
4. **CRITICAL**: Validate immediately after each edit and fix any validation errors before proceeding: `python ooxml/scripts/validate.py <dir> --original <file>`
5. Pack the final presentation: `python ooxml/scripts/pack.py <input_directory> <office_file>`

## Creating a new PowerPoint presentation **using a template**

When you need to create a presentation that follows an existing template's design, you'll need to duplicate and re-arrange template slides before then replacing placeholder context.

### Workflow
1. **Extract template text AND create visual thumbnail grid**:
   * Extract text: `python -m markitdown template.pptx > template-content.md`
   * Read `template-content.md`: Read the entire file to understand the contents of the template presentation. **NEVER set any range limits when reading this file.**
   * Create thumbnail grids: `python scripts/thumbnail.py template.pptx`
   * See [Creating Thumbnail Grids](#creating-thumbnail-grids) section for more details

2. **Analyze template and save inventory to a file**:
   * **Visual Analysis**: Review thumbnail grid(s) to understand slide layouts, design patterns, and visual structure
   * Create and save a template inventory file at `template-inventory.md` containing:
     ```markdown
     # Template Inventory Analysis
     **Total Slides: [count]**
     **IMPORTANT: Slides are 0-indexed (first slide = 0, last slide = count-1)**

     ## [Category Name]
     - Slide 0: [Layout code if available] - Description/purpose
     - Slide 1: [Layout code] - Description/purpose
     - Slide 2: [Layout code] - Description/purpose
     [... EVERY slide must be listed individually with its index ...]
     ```
   * **Using the thumbnail grid**: Reference the visual thumbnails to identify:
     - Layout patterns (title slides, content layouts, section dividers)
     - Image placeholder locations and counts
     - Design consistency across slide groups
     - Visual hierarchy and structure
   * This inventory file is REQUIRED for selecting appropriate templates in the next step

3. **Create presentation outline based on template inventory**:
   * Review available templates from step 2.
   * Choose an intro or title template for the first slide. This should be one of the first templates.
   * Choose safe, text-based layouts for the other slides.
   * **CRITICAL: Match layout structure to actual content**:
     - Single-column layouts: Use for unified narrative or single topic
     - Two-column layouts: Use ONLY when you have exactly 2 distinct items/concepts
     - Three-column layouts: Use ONLY when you have exactly 3 distinct items/concepts
     - Image + text layouts: Use ONLY when you have actual images to insert
     - Quote layouts: Use ONLY for actual quotes from people (with attribution), never for emphasis
     - Never use layouts with more placeholders than you have content
     - If you have 2 items, don't force them into a 3-column layout
     - If you have 4+ items, consider breaking into multiple slides or using a list format
   * Count your actual content pieces BEFORE selecting the layout
   * Verify each placeholder in the chosen layout will be filled with meaningful content
   * Select one option representing the **best** layout for each content section.
   * Save `outline.md` with content AND template mapping that leverages available designs
   * Example template mapping:
      ```
      # Template slides to use (0-based indexing)
      # WARNING: Verify indices are within range! Template with 73 slides has indices 0-72
      # Mapping: slide numbers from outline -> template slide indices
      template_mapping = [
          0,   # Use slide 0 (Title/Cover)
          34,  # Use slide 34 (B1: Title and body)
          34,  # Use slide 34 again (duplicate for second B1)
          50,  # Use slide 50 (E1: Quote)
          54,  # Use slide 54 (F2: Closing + Text)
      ]
      ```

4. **Duplicate, reorder, and delete slides using `rearrange.py`**:
   * Use the `scripts/rearrange.py` script to create a new presentation with slides in the desired order:
     ```bash
     python scripts/rearrange.py template.pptx working.pptx 0,34,34,50,52
     ```
   * The script handles duplicating repeated slides, deleting unused slides, and reordering automatically
   * Slide indices are 0-based (first slide is 0, second is 1, etc.)
   * The same slide index can appear multiple times to duplicate that slide

5. **Extract ALL text using the `inventory.py` script**:
   * **Run inventory extraction**:
     ```bash
     python scripts/inventory.py working.pptx text-inventory.json
     ```
   * **Read text-inventory.json**: Read the entire text-inventory.json file to understand all shapes and their properties. **NEVER set any range limits when reading this file.**

   * The inventory JSON structure:
      ```json
        {
          "slide-0": {
            "shape-0": {
              "placeholder_type": "TITLE",  // or null for non-placeholders
              "left": 1.5,                  // position in inches
              "top": 2.0,
              "width": 7.5,
              "height": 1.2,
              "paragraphs": [
                {
                  "text": "Paragraph text",
                  // Optional properties (only included when non-default):
                  "bullet": true,           // explicit bullet detected
                  "level": 0,               // only included when bullet is true
                  "alignment": "CENTER",    // CENTER, RIGHT (not LEFT)
                  "space_before": 10.0,     // space before paragraph in points
                  "space_after": 6.0,       // space after paragraph in points
                  "line_spacing": 22.4,     // line spacing in points
                  "font_name": "Arial",     // from first run
                  "font_size": 14.0,        // in points
                  "bold": true,
                  "italic": false,
                  "underline": false,
                  "color": "FF0000"         // RGB color
                }
              ]
            }
          }
        }
      ```

   * Key features:
     - **Slides**: Named as "slide-0", "slide-1", etc.
     - **Shapes**: Ordered by visual position (top-to-bottom, left-to-right) as "shape-0", "shape-1", etc.
     - **Placeholder types**: TITLE, CENTER_TITLE, SUBTITLE, BODY, OBJECT, or null
     - **Default font size**: `default_font_size` in points extracted from layout placeholders (when available)
     - **Slide numbers are filtered**: Shapes with SLIDE_NUMBER placeholder type are automatically excluded from inventory
     - **Bullets**: When `bullet: true`, `level` is always included (even if 0)
     - **Spacing**: `space_before`, `space_after`, and `line_spacing` in points (only included when set)
     - **Colors**: `color` for RGB (e.g., "FF0000"), `theme_color` for theme colors (e.g., "DARK_1")
     - **Properties**: Only non-default values are included in the output

6. **Generate replacement text and save the data to a JSON file**
   Based on the text inventory from the previous step:
   - **CRITICAL**: First verify which shapes exist in the inventory - only reference shapes that are actually present
   - **VALIDATION**: The replace.py script will validate that all shapes in your replacement JSON exist in the inventory
     - If you reference a non-existent shape, you'll get an error showing available shapes
     - If you reference a non-existent slide, you'll get an error indicating the slide doesn't exist
     - All validation errors are shown at once before the script exits
   - **IMPORTANT**: The replace.py script uses inventory.py internally to identify ALL text shapes
   - **AUTOMATIC CLEARING**: ALL text shapes from the inventory will be cleared unless you provide "paragraphs" for them
   - Add a "paragraphs" field to shapes that need content (not "replacement_paragraphs")
   - Shapes without "paragraphs" in the replacement JSON will have their text cleared automatically
   - Paragraphs with bullets will be automatically left aligned. Don't set the `alignment` property on when `"bullet": true`
   - Generate appropriate replacement content for placeholder text
   - Use shape size to determine appropriate content length
   - **CRITICAL**: Include paragraph properties from the original inventory - don't just provide text
   - **IMPORTANT**: When bullet: true, do NOT include bullet symbols (•, -, *) in text - they're added automatically
   - **ESSENTIAL FORMATTING RULES**:
     - Headers/titles should typically have `"bold": true`
     - List items should have `"bullet": true, "level": 0` (level is required when bullet is true)
     - Preserve any alignment properties (e.g., `"alignment": "CENTER"` for centered text)
     - Include font properties when different from default (e.g., `"font_size": 14.0`, `"font_name": "Lora"`)
     - Colors: Use `"color": "FF0000"` for RGB or `"theme_color": "DARK_1"` for theme colors
     - The replacement script expects **properly formatted paragraphs**, not just text strings
     - **Overlapping shapes**: Prefer shapes with larger default_font_size or more appropriate placeholder_type
   - Save the updated inventory with replacements to `replacement-text.json`
   - **WARNING**: Different template layouts have different shape counts - always check the actual inventory before creating replacements

   Example paragraphs field showing proper formatting:
   ```json
   "paragraphs": [
     {
       "text": "New presentation title text",
       "alignment": "CENTER",
       "bold": true
     },
     {
       "text": "Section Header",
       "bold": true
     },
     {
       "text": "First bullet point without bullet symbol",
       "bullet": true,
       "level": 0
     },
     {
       "text": "Red colored text",
       "color": "FF0000"
     },
     {
       "text": "Theme colored text",
       "theme_color": "DARK_1"
     },
     {
       "text": "Regular paragraph text without special formatting"
     }
   ]
   ```

   **Shapes not listed in the replacement JSON are automatically cleared**:
   ```json
   {
     "slide-0": {
       "shape-0": {
         "paragraphs": [...] // This shape gets new text
       }
       // shape-1 and shape-2 from inventory will be cleared automatically
     }
   }
   ```

   **Common formatting patterns for presentations**:
   - Title slides: Bold text, sometimes centered
   - Section headers within slides: Bold text
   - Bullet lists: Each item needs `"bullet": true, "level": 0`
   - Body text: Usually no special properties needed
   - Quotes: May have special alignment or font properties

7. **Apply replacements using the `replace.py` script**
   ```bash
   python scripts/replace.py working.pptx replacement-text.json output.pptx
   ```

   The script will:
   - First extract the inventory of ALL text shapes using functions from inventory.py
   - Validate that all shapes in the replacement JSON exist in the inventory
   - Clear text from ALL shapes identified in the inventory
   - Apply new text only to shapes with "paragraphs" defined in the replacement JSON
   - Preserve formatting by applying paragraph properties from the JSON
   - Handle bullets, alignment, font properties, and colors automatically
   - Save the updated presentation

   Example validation errors:
   ```
   ERROR: Invalid shapes in replacement JSON:
     - Shape 'shape-99' not found on 'slide-0'. Available shapes: shape-0, shape-1, shape-4
     - Slide 'slide-999' not found in inventory
   ```

   ```
   ERROR: Replacement text made overflow worse in these shapes:
     - slide-0/shape-2: overflow worsened by 1.25" (was 0.00", now 1.25")
   ```

## Creating Thumbnail Grids

To create visual thumbnail grids of PowerPoint slides for quick analysis and reference:

```bash
python3 scripts/thumbnail.py template.pptx [output_prefix]
```

**Note**: Requires LibreOffice (`soffice`). If unavailable, skip thumbnail generation and verify the presentation manually in PowerPoint.

**Features**:
- Creates: `thumbnails.jpg` (or `thumbnails-1.jpg`, `thumbnails-2.jpg`, etc. for large decks)
- Default: 5 columns, max 30 slides per grid (5×6)
- Custom prefix: `python scripts/thumbnail.py template.pptx my-grid`
  - Note: The output prefix should include the path if you want output in a specific directory (e.g., `workspace/my-grid`)
- Adjust columns: `--cols 4` (range: 3-6, affects slides per grid)
- Grid limits: 3 cols = 12 slides/grid, 4 cols = 20, 5 cols = 30, 6 cols = 42
- Slides are zero-indexed (Slide 0, Slide 1, etc.)

**Use cases**:
- Template analysis: Quickly understand slide layouts and design patterns
- Content review: Visual overview of entire presentation
- Navigation reference: Find specific slides by their visual appearance
- Quality check: Verify all slides are properly formatted

**Examples**:
```bash
# Basic usage
python scripts/thumbnail.py presentation.pptx

# Combine options: custom name, columns
python scripts/thumbnail.py template.pptx analysis --cols 4
```

## Converting Slides to Images

To visually analyze PowerPoint slides, convert them to images using a two-step process:

1. **Convert PPTX to PDF**:
   ```bash
   soffice --headless --convert-to pdf template.pptx
   ```

2. **Convert PDF pages to JPEG images**:
   ```bash
   pdftoppm -jpeg -r 150 template.pdf slide
   ```
   This creates files like `slide-1.jpg`, `slide-2.jpg`, etc.

Options:
- `-r 150`: Sets resolution to 150 DPI (adjust for quality/size balance)
- `-jpeg`: Output JPEG format (use `-png` for PNG if preferred)
- `-f N`: First page to convert (e.g., `-f 2` starts from page 2)
- `-l N`: Last page to convert (e.g., `-l 5` stops at page 5)
- `slide`: Prefix for output files

Example for specific range:
```bash
pdftoppm -jpeg -r 150 -f 2 -l 5 template.pdf slide  # Converts only pages 2-5
```

## Code Style Guidelines
**IMPORTANT**: When generating code for PPTX operations:
- Write concise code
- Avoid verbose variable names and redundant operations
- Avoid unnecessary print statements

## Known Limitations and Workarounds

### python-pptx Placeholder Access Bug (CRITICAL)

**Symptom**: Slides have titles but NO body content - all placeholder content silently fails to populate.

**Root Cause**: The `in` operator does NOT work with `slide.placeholders` collection.

```python
# THIS DOES NOT WORK - always returns False even when placeholder exists!
if 56 in slide.placeholders:  # ❌ Returns False
    body_ph = slide.placeholders[56]

# Direct access DOES work
body_ph = slide.placeholders[56]  # ✅ Returns the placeholder
```

**Affected Pattern**:
```python
# BROKEN - silently skips all content
if 56 in slide.placeholders:
    slide.placeholders[56].text = "Content"
```

**Solution - Use try/except**:
```python
# CORRECT approach
try:
    body_ph = slide.placeholders[56]
    body_ph.text = "Content"
except KeyError:
    print("Placeholder 56 not found")
```

**Complete Example**:
```python
def add_content_slide(prs, title, strapline, body_lines):
    layout = prs.slide_layouts[5]
    slide = prs.slides.add_slide(layout)

    # Title (idx=0)
    try:
        title_ph = slide.placeholders[0]
        set_text_with_formatting(title_ph, title, "KPMG Bold", Pt(44), True, False, DARK_BLUE)
    except KeyError:
        print(f"Warning: Title placeholder not found for '{title}'")

    # Strapline (idx=18) - 18pt, NOT italic
    try:
        strap_ph = slide.placeholders[18]
        set_text_with_formatting(strap_ph, strapline, "Arial", Pt(18), False, False, PACIFIC_BLUE)
    except KeyError:
        pass  # Strapline is optional

    # Body (idx=56) with fallback
    try:
        body_ph = slide.placeholders[56]
        set_multiline_text(body_ph, body_lines, "Arial", Pt(16), DARK_BLUE)
    except KeyError:
        try:
            body_ph = slide.placeholders[17]  # Fallback index
            set_multiline_text(body_ph, body_lines, "Arial", Pt(16), DARK_BLUE)
        except KeyError:
            print(f"Warning: Body placeholder not found for '{title}'")

    return slide
```

This bug was discovered during the Lakehouse Presentation project (Jan 2026) where all 42 slides had titles but no body content because `if X in slide.placeholders:` checks silently skipped all body placeholder population.

### python-pptx Duplicate ZIP Entry Bug (CRITICAL)

**Symptom**: PowerPoint shows "found a problem with content" repair dialog when opening file.

**Root Cause**: When using python-pptx to delete slides and save, it creates duplicate file entries in the ZIP archive (e.g., two `ppt/slides/slide7.xml` entries). This is a known limitation of the library.

**Affected Operations**:
- `prs.slides._sldIdLst` deletion
- `prs.part.drop_rel()`
- Any slide deletion or rearrangement

**Solution - Add-Only with Post-Processing**:

1. **Never delete slides during python-pptx session** - only add new slides
2. **Add new slides at the END** using template layouts
3. **Save to temporary file**
4. **Post-process at ZIP/XML level** to remove unwanted slides:

```python
# Post-processing script to remove original slides
import zipfile
import os
from xml.etree import ElementTree as ET

# Steps:
# 1. Extract PPTX (handling duplicates by keeping last occurrence)
# 2. Modify ppt/presentation.xml to remove slide references
# 3. Modify ppt/_rels/presentation.xml.rels to remove relationships
# 4. Delete original slide XML files from ppt/slides/
# 5. Update [Content_Types].xml
# 6. Renumber remaining slides (slide31.xml → slide1.xml)
# 7. Repack without duplicates
```

See the Lakehouse Presentation project for a complete implementation in `postprocess_pptx.py`.

**Alternative - Template Placeholder Approach**:
If you don't need to remove template slides:
1. Modify content IN PLACE using `slide.placeholders[idx]`
2. Hide unwanted slides or leave as appendix
3. Never delete during python-pptx session

### KPMG Template-Specific Notes

**IMPORTANT**: Each KPMG template has a `config.yaml` file with all settings. Read the config first:
```
~/Library/Mobile Documents/com~apple~CloudDocs/claude-code/templates/kpmg/[TEMPLATE-NAME]/config.yaml
```

The config contains: colors, typography, layout indices, placeholder indices, and notes.

**Reference below is for KPMG-2022** (also in its config.yaml):

**Layout Index Reference** (13 layouts total, indices 0-12):
- Layout 0: Cover page (dark blue background)
- Layout 1: 1_Subsection divider (RECOMMENDED for section breaks - set background programmatically)
- Layout 3: One Column Text (title idx=0, body idx=10)
- Layout 4: Two Columns Text (title idx=0, left idx=10, right idx=11)
- Layout 5: 1_Back Cover light gradient

**KPMG Colors** (NO # prefix in color values):
- KPMG Blue: `00338D` / RGB(0, 51, 141) - use for links, accents
- Dark Blue: `0C233C` / RGB(12, 35, 60) - use for content slide titles
- Pacific Blue: `00B8F5` / RGB(0, 184, 245) - use for straplines
- Light Blue: `ACEAFF` / RGB(172, 234, 255) - background accent (often needs changing to dark blue)

**Typography for Presentations** (screen display, larger than reports):
- Cover title: KPMG Bold, 88pt, White
- Content titles: KPMG Bold, 44pt, Dark Blue (#0C233C)
- Body: Arial, 16pt
- Section dividers: KPMG Bold, 66pt, White on Dark Blue
- Contents title: KPMG Bold, 60pt, White on Dark Blue
- Accent text: Arial, 16pt, Pacific Blue (#00B8F5)

**Note:** No strapline - cleaner, modern design (Anthropic-inspired).

**Font Override Issue - CRITICAL**:
Placeholder shapes inherit ALL font properties from layout/master. You must explicitly set EVERY property you want to control at BOTH paragraph level (`defRPr`) AND run level (`rPr`):
```python
# Set paragraph-level defaults (overrides layout/master)
p.font.size = font_size
p.font.name = font_name
p.font.bold = bold
p.font.italic = False  # CRITICAL: Explicitly set italic=False or it inherits from template
if color:
    p.font.color.rgb = color

# Also set run-level properties
run.font.size = font_size
run.font.name = font_name
run.font.bold = bold
run.font.italic = False  # CRITICAL: Must set at both levels
if color:
    run.font.color.rgb = color
```

**Common mistake**: Straplines inherit italic from template if not explicitly set to `False`. Always include `italic=False` in function calls for non-italic text.

**Setting Slide Background Color** (RECOMMENDED approach for section dividers):
Use Layout 1 (1_Subsection divider) and set the background programmatically:
```python
# Use Layout 1 for section dividers
layout = prs.slide_layouts[1]  # 1_Subsection divider
slide = prs.slides.add_slide(layout)

# Set slide background to dark blue
background = slide.background
fill = background.fill
fill.solid()
fill.fore_color.rgb = RGBColor(12, 35, 60)  # Dark Blue #0C233C

# Set title with white text
title_ph = slide.placeholders[0]
# ... set text with white color
```

**Legacy: Fixing Light Blue Rectangle in Layout 1** (if Layout 2 not suitable):
```python
for shape in slide.shapes:
    if hasattr(shape, 'fill'):
        try:
            if shape.fill.type is not None and shape.fill.fore_color.rgb == RGBColor(172, 234, 255):
                shape.fill.solid()
                shape.fill.fore_color.rgb = DARK_BLUE  # RGB(12, 35, 60)
        except (TypeError, AttributeError):
            pass
```

**Removing DRAFT Watermark**:
```python
def remove_draft_watermark(prs):
    for master in prs.slide_masters:
        for shape in list(master.shapes):
            if hasattr(shape, 'text') and 'DRAFT' in shape.text.upper():
                sp = shape._element
                sp.getparent().remove(sp)
```

## Dependencies

Required dependencies (should already be installed):

**Note**: On macOS, use `python3` not `python` for all commands.

- **markitdown**: `pip install "markitdown[pptx]"` (for text extraction from presentations)
- **pptxgenjs**: `npm install -g pptxgenjs` (for creating presentations via html2pptx)
- **playwright**: `npm install -g playwright` (for HTML rendering in html2pptx)
- **react-icons**: `npm install -g react-icons react react-dom` (for icons)
- **sharp**: `npm install -g sharp` (for SVG rasterization and image processing)
- **LibreOffice**: `sudo apt-get install libreoffice` (for PDF conversion)
- **Poppler**: `sudo apt-get install poppler-utils` (for pdftoppm to convert PDF to images)
- **defusedxml**: `pip install defusedxml` (for secure XML parsing)
---
name: pptx
description: "Presentation creation, editing, and analysis. When Claude needs to work with presentations (.pptx files) for: (1) Creating new presentations, (2) Modifying or editing content, (3) Working with layouts, (4) Adding comments or speaker notes, or any other presentation tasks. Also triggers on: KPMG presentation, KPMG slides, KPMG format, KPMG PowerPoint, KPMG branded"
license: Proprietary. LICENSE.txt has complete terms
---

# PPTX creation, editing, and analysis

A .pptx file is a ZIP archive containing XML files. Different tools and workflows are available depending on the task.

## KPMG Presentations

**ALWAYS use python-pptx with a KPMG template. NEVER use PptxGenJS or html2pptx for branded presentations.**

### Template Location
```
~/Library/Mobile Documents/com~apple~CloudDocs/claude-code/templates/kpmg/KPMG-2022/
```
- `template-clean.pptx` - Empty template (0 slides, 19 layouts, no DRAFT watermark)
- `config.yaml` - **Read this first** for colors, typography, layouts, placeholder indices

### Reference Script
Copy and adapt `skills/pptx/scripts/kpmg_reference.py` rather than writing from scratch.

### Quick Reference

**Layouts**: 0=Cover, 3=Section divider, 10=One column, 11=Two column, 13=Back cover

**Placeholder indices**: title=0, strapline=18, body=56, right column=57

**Colors** (no # prefix): Dark Blue `0C233C`, Pacific Blue `00B8F5`, KPMG Blue `00338D`

**Typography**:
| Element | Font | Size | Color |
|---------|------|------|-------|
| Cover title | KPMG Bold | 88pt | White |
| Content titles | KPMG Bold | 44pt | Dark Blue |
| Strapline | Arial | 18pt | Pacific Blue |
| Body | Arial | 16pt | Default |
| Section dividers | KPMG Bold | 66pt | White |

### Critical: Placeholder Access Bug
```python
# BROKEN - always returns False:
if 56 in slide.placeholders:  # Never use this!

# CORRECT - use try/except:
try:
    body_ph = slide.placeholders[56]
except KeyError:
    pass
```

### Critical: Font Override
Set ALL font properties at BOTH paragraph AND run level, including `italic=False`:
```python
p.font.italic = False  # Must explicitly set or inherits from template
run.font.italic = False
```

### Section Dividers
Use Layout 2 and set background programmatically:
```python
slide.background.fill.solid()
slide.background.fill.fore_color.rgb = RGBColor(12, 35, 60)
```

### Image Constraints
Max height ~3.8" to avoid overlapping KPMG footer.

---

## Reading and Analyzing Content

**Text extraction**:
```bash
python -m markitdown path-to-file.pptx
```

**Raw XML access** (for comments, notes, layouts, animations):
```bash
python ooxml/scripts/unpack.py <office_file> <output_dir>
```

Key paths:
- `ppt/presentation.xml` - Slide references and metadata
- `ppt/slides/slide{N}.xml` - Individual slide contents
- `ppt/notesSlides/notesSlide{N}.xml` - Speaker notes
- `ppt/comments/` - Comments
- `ppt/slideLayouts/` - Layout templates
- `ppt/slideMasters/` - Master slides
- `ppt/theme/theme1.xml` - Colors and fonts

**Extracting typography/colors from existing presentations**:
1. Read `ppt/theme/theme1.xml` for `<a:clrScheme>` (colors) and `<a:fontScheme>` (fonts)
2. Examine `ppt/slides/slide1.xml` for actual `<a:rPr>` font usage
3. Grep for `<a:solidFill>`, `<a:srgbClr>` patterns across XML files

---

## Creating Presentations Without a Template

### Option A: PptxGenJS (Non-branded only)

**WARNING: Do NOT use for KPMG or branded presentations.**

Use for structured content with speaker notes:
```javascript
const pptxgen = require('pptxgenjs');
const pptx = new pptxgen();
pptx.layout = 'LAYOUT_16x9';

const slide = pptx.addSlide();
slide.addText('Title', { x: 0.5, y: 1.5, w: 9, fontSize: 28, bold: true });
slide.addNotes('Speaker notes here');
pptx.writeFile({ fileName: 'output.pptx' });
```

### Option B: html2pptx (Complex visual designs)

**Read [`html2pptx.md`](html2pptx.md) completely before proceeding.**

1. Create HTML slides (720pt x 405pt for 16:9)
2. Use `class="placeholder"` for chart/table areas
3. Rasterize gradients/icons as PNG first using Sharp
4. Run html2pptx.js to convert
5. Validate with thumbnails: `python scripts/thumbnail.py output.pptx`

### Design Principles

Before creating any presentation:
1. Consider subject matter and tone
2. Check for branding requirements
3. Choose colors that match content (see [`color-palettes.md`](color-palettes.md))
4. Use web-safe fonts only: Arial, Helvetica, Georgia, Verdana, Tahoma, Trebuchet MS

**Layout tips**:
- Two-column layouts work best for charts/tables alongside text
- Never vertically stack charts below text
- Full-slide layout for maximum chart/table impact

---

## Editing Existing Presentations

**Read [`ooxml.md`](ooxml.md) completely before proceeding.**

1. Unpack: `python ooxml/scripts/unpack.py <file> <output_dir>`
2. Edit XML files
3. Validate: `python ooxml/scripts/validate.py <dir> --original <file>`
4. Pack: `python ooxml/scripts/pack.py <input_dir> <file>`

---

## Creating Presentations Using a Template

### Workflow

1. **Analyze template**:
   ```bash
   python -m markitdown template.pptx > template-content.md
   python scripts/thumbnail.py template.pptx
   ```

2. **Create template inventory** at `template-inventory.md`:
   - List every slide with index, layout code, and purpose
   - Note: Slides are 0-indexed

3. **Create outline** at `outline.md`:
   - Match layouts to content (don't use 3-column for 2 items)
   - Include template mapping: `template_mapping = [0, 34, 34, 50, 54]`

4. **Rearrange slides**:
   ```bash
   python scripts/rearrange.py template.pptx working.pptx 0,34,34,50,52
   ```

5. **Extract text inventory**:
   ```bash
   python scripts/inventory.py working.pptx text-inventory.json
   ```

6. **Create replacement JSON** at `replacement-text.json`:
   - Only reference shapes that exist in inventory
   - Shapes without "paragraphs" are automatically cleared
   - Include formatting properties (bold, bullet, level, alignment)
   - Don't include bullet symbols in text - added automatically

7. **Apply replacements**:
   ```bash
   python scripts/replace.py working.pptx replacement-text.json output.pptx
   ```

---

## Thumbnail Grids

```bash
python scripts/thumbnail.py template.pptx [output_prefix] [--cols 4]
```
- Default: 5 columns, max 30 slides per grid
- Requires LibreOffice

## Converting Slides to Images

```bash
# 1. Convert PPTX to PDF
soffice --headless --convert-to pdf template.pptx

# 2. Convert PDF pages to JPEG
pdftoppm -jpeg -r 150 template.pdf slide
# Creates: slide-1.jpg, slide-2.jpg, etc.
```

Options: `-r 150` (DPI), `-f N` (first page), `-l N` (last page), `-png` (PNG format)

---

## Known Limitations

### python-pptx Duplicate ZIP Entry Bug
When deleting slides with python-pptx, duplicate ZIP entries cause PowerPoint repair dialogs.

**Solution**: Only add slides during python-pptx session, then post-process at ZIP/XML level to remove unwanted slides.

---

## Dependencies

- **markitdown**: `pip install "markitdown[pptx]"`
- **pptxgenjs**: `npm install -g pptxgenjs`
- **playwright**: `npm install -g playwright`
- **sharp**: `npm install -g sharp`
- **LibreOffice**: For PDF/thumbnail conversion
- **Poppler**: For pdftoppm (PDF to images)
- **defusedxml**: `pip install defusedxml`

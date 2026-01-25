---
name: pptx-template-setup
description: "Set up a new branded PowerPoint template for use with the pptx skill. Use when onboarding a new corporate template (e.g., client branding, new company template) to extract layouts, placeholders, colors, and typography into a reusable config."
---

# PowerPoint Template Setup

Guide for analyzing and onboarding a new branded PowerPoint template for automated presentation generation.

## When to Use This Skill

- User provides a new branded .pptx template
- Need to create presentations in a new corporate style
- Setting up a template for a client or new brand

## Overview

Setting up a new template involves:
1. **Analyze** — Extract layouts, placeholders, colors, typography
2. **Document** — Create config.yaml with all settings
3. **Test** — Generate a test presentation to verify
4. **Store** — Save template and config in templates folder

## Step 1: Create Template Folder

```bash
mkdir -p ~/Library/Mobile\ Documents/com~apple~CloudDocs/claude-code/templates/[brand]/[template-name]/
```

Example: `templates/lakehouse/Lakehouse-2026/`

Copy the source template into this folder as `template.pptx`.

## Step 2: Generate Thumbnail Grid

```bash
python3 ~/Library/Mobile\ Documents/com~apple~CloudDocs/claude-code/skills/pptx/scripts/thumbnail.py template.pptx thumbnails --cols 5
```

Read the thumbnail image to visually identify:
- Cover slide layout
- Section divider layouts
- Content layouts (one-column, two-column)
- Special layouts (quotes, images, back cover)

Note the **slide index** (0-based) for each layout type.

## Step 3: Extract Layout Information

### 3a. Unpack the Template

```bash
mkdir -p /tmp/template_analysis
unzip -q template.pptx -d /tmp/template_analysis
```

### 3b. List All Layouts

```bash
ls /tmp/template_analysis/ppt/slideLayouts/
```

### 3c. Analyze Each Useful Layout

For each layout you identified in the thumbnails, extract placeholder indices:

```bash
# Example: Analyze layout 5
grep -o 'idx="[0-9]*"' /tmp/template_analysis/ppt/slideLayouts/slideLayout5.xml | sort -u
```

Common placeholder types:
- `idx="0"` — Usually title
- `idx="1"` — Usually subtitle or body
- `idx="10-19"` — Often custom placeholders (straplines, footers)
- `idx="56-57"` — Often body/column placeholders in KPMG templates

### 3d. Identify Placeholder Purposes

Read the layout XML to see placeholder names and types:

```bash
grep -o 'name="[^"]*".*idx="[0-9]*"' /tmp/template_analysis/ppt/slideLayouts/slideLayout5.xml
```

Or extract with context:
```bash
grep -B2 -A2 'idx="18"' /tmp/template_analysis/ppt/slideLayouts/slideLayout5.xml
```

## Step 4: Extract Colors

### 4a. Theme Colors

```bash
grep -o 'val="[A-Fa-f0-9]\{6\}"' /tmp/template_analysis/ppt/theme/theme1.xml | sort -u
```

### 4b. Color Scheme Names

```bash
grep -o '<a:dk1\|<a:lt1\|<a:dk2\|<a:lt2\|<a:accent[0-9]' /tmp/template_analysis/ppt/theme/theme1.xml
```

### 4c. Identify Key Colors

Look for:
- **Dark color** — Usually for titles, text (often dk1 or a dark blue)
- **Accent color** — For highlights, straplines (often accent1-4)
- **Background colors** — For section dividers

Document RGB values without # prefix (e.g., `0C233C` not `#0C233C`).

## Step 5: Extract Typography

### 5a. Font Names

```bash
grep -o 'typeface="[^"]*"' /tmp/template_analysis/ppt/theme/theme1.xml | sort -u
grep -o 'typeface="[^"]*"' /tmp/template_analysis/ppt/slideMasters/slideMaster1.xml | sort -u
```

### 5b. Font Sizes in Layouts

```bash
# Size is in hundredths of a point (e.g., 4400 = 44pt)
grep -o 'sz="[0-9]*"' /tmp/template_analysis/ppt/slideLayouts/slideLayout5.xml | sort -u
```

### 5c. Default Formatting

Check for default bold, italic, color settings:
```bash
grep -o 'b="[01]"\|i="[01]"' /tmp/template_analysis/ppt/slideLayouts/slideLayout5.xml
```

## Step 6: Create config.yaml

Create `config.yaml` in the template folder:

```yaml
# [Brand] [Year] Template Configuration
# Used by pptx skill for [brand]-branded presentations

name: [Brand] [Year]
template_file: template.pptx
template_slides: [N]  # Number of slides in original template

# Colors (NO # prefix for python-pptx)
colors:
  primary: "XXXXXX"       # RGB - main brand color
  secondary: "XXXXXX"     # RGB - secondary color
  accent: "XXXXXX"        # RGB - accent/highlight color
  dark: "XXXXXX"          # RGB - dark text/backgrounds
  light: "XXXXXX"         # RGB - light backgrounds

# Typography
typography:
  cover_title:
    font: "[Font Name]"
    size: [N]             # in points
    color: [color_key]
    bold: true

  content_title:
    font: "[Font Name]"
    size: [N]
    color: [color_key]
    bold: true

  strapline:
    font: "[Font Name]"
    size: [N]
    color: [color_key]
    italic: false         # IMPORTANT: explicitly set

  body:
    font: "[Font Name]"
    size: [N]
    color: [color_key]

  section_divider:
    font: "[Font Name]"
    size: [N]
    color: [color_key]
    background: [color_key]

# Layout indices (0-based)
layouts:
  cover: [N]
  section_divider: [N]
  one_column: [N]
  two_column: [N]
  back_cover: [N]
  # Add others as needed: quote, image, three_column, etc.

# Placeholder indices for content layouts
placeholders:
  title: [N]
  strapline: [N]          # or null if not used
  body: [N]
  left_column: [N]
  right_column: [N]
  footer: [N]             # or null if not used

# Notes
notes: |
  - [Any special handling required]
  - [Known issues or workarounds]
  - [Post-processing requirements]
```

## Step 7: Clean the Template (Optional)

If the template has watermarks, draft text, or unwanted elements:

### Remove DRAFT Watermark

```python
from pptx import Presentation

prs = Presentation('template.pptx')
for master in prs.slide_masters:
    for shape in list(master.shapes):
        if hasattr(shape, 'text') and 'DRAFT' in shape.text.upper():
            sp = shape._element
            sp.getparent().remove(sp)
prs.save('template-clean.pptx')
```

Update config.yaml to reference the clean template:
```yaml
template_file: template-clean.pptx
```

### Fix Default Formatting in Layouts

If straplines default to italic or wrong size, edit the layout XML:

```python
# See pptx skill for fix_strapline.py example
# Modifies slideLayout XML to set sz="1800" i="0" on strapline placeholders
```

## Step 8: Create Reference Script

Copy and adapt from:
```
~/Library/Mobile Documents/com~apple~CloudDocs/claude-code/skills/pptx/scripts/kpmg_reference.py
```

Update:
- `TEMPLATE_PATH` — Point to new template
- Colors — Use values from config.yaml
- Layout indices — Use values from config.yaml
- Placeholder indices — Use values from config.yaml
- Typography — Match fonts and sizes from config.yaml

Save as `[template-name]_reference.py` in the template folder.

## Step 9: Test the Template

Generate a test presentation with:
- Cover slide
- Section divider
- One-column content slide
- Two-column content slide
- Back cover

Verify in PowerPoint:
- Fonts render correctly
- Colors match brand
- Placeholders populate properly
- No corruption errors on open

## Step 10: Update CLAUDE.md

Add the new template to the global CLAUDE.md templates table:

```markdown
| [Brand] [Year] | `[path]/template.pptx` | `[path]/config.yaml` |
```

## Checklist

- [ ] Template folder created
- [ ] Thumbnail grid generated and analyzed
- [ ] Layout indices identified
- [ ] Placeholder indices extracted
- [ ] Colors documented (RGB without #)
- [ ] Typography documented (fonts, sizes, styles)
- [ ] config.yaml created
- [ ] Template cleaned (if needed)
- [ ] Reference script created
- [ ] Test presentation generated
- [ ] CLAUDE.md updated

## Troubleshooting

### Placeholders Not Found

Use try/except, never `if X in slide.placeholders:` (see pptx skill).

### Fonts Not Rendering

- Check font is installed on system
- Use fallback fonts (Arial, Helvetica) if custom fonts unavailable

### Wrong Formatting Applied

Set ALL font properties at BOTH paragraph AND run level, including `italic=False`.

### Corrupt File on Open

Never delete slides during python-pptx session. Use post-processing to remove template slides.

## Related

- `pptx` skill — Main presentation skill
- `pptx/scripts/kpmg_reference.py` — Reference implementation
- `templates/kpmg/KPMG-2022/config.yaml` — Example config

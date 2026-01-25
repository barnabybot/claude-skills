---
name: kpmg-pptx
description: "Create KPMG-branded PowerPoint presentations. Use when creating presentations for KPMG work, applying KPMG styling, or when user mentions 'KPMG presentation', 'KPMG slides', or 'KPMG format'."
---

# KPMG PowerPoint Presentation Skill

Create professional PowerPoint presentations following KPMG Brand 2022 guidelines.

**This skill extends the `pptx` skill.** For general PowerPoint operations (reading, editing, workflows), refer to the pptx skill documentation. All scripts referenced below are from the pptx skill.

## Quick Reference

| Resource | Location |
|----------|----------|
| **KPMG Theme** | `~/Library/Group Containers/UBF8T346G9.Office/User Content/Themes/KPMG Theme 2022.thmx` |
| **KPMG Template** | `/Users/barnabyrobson/Desktop/KPMG theme/Theme1.thmx` |
| **pptx Scripts** | `~/Library/Mobile Documents/com~apple~CloudDocs/claude-code/skills/pptx/scripts/` |
| **Fonts** | `~/Library/Fonts/KPMG*.ttf` |

## Creating KPMG Presentations

### RECOMMENDED: Template-Based Workflow

**When you have KPMG template slides available**, use the template-based workflow from the pptx skill. This ensures proper positioning, fonts, and brand compliance.

#### Step 1: Analyze the template
```bash
# Extract text content
python -m markitdown template.pptx > template-content.md

# Create visual thumbnail grid
python scripts/thumbnail.py template.pptx workspace/thumbnails --cols 4
```

Review the thumbnails to identify available slide layouts:
- Title/Cover slides
- Content slides (bullets, two-column)
- Section dividers
- Quote slides
- Tables/data slides

#### Step 2: Create slide mapping
Select template slides that match your content needs:

```python
# Example: Slide indices to use from template (0-indexed)
template_mapping = [
    0,   # Title/Cover slide
    5,   # Content with bullets
    5,   # Duplicate content slide
    12,  # Section divider
    8,   # Two-column layout
    15,  # Quote slide
    20,  # Q&A/Closing
]
```

#### Step 3: Rearrange slides
```bash
python scripts/rearrange.py template.pptx working.pptx 0,5,5,12,8,15,20
```

#### Step 4: Extract text inventory
```bash
python scripts/inventory.py working.pptx text-inventory.json
```

Read the inventory to understand shape positions and placeholder types.

#### Step 5: Create replacement text
Generate `replacement-text.json` with new content:

```json
{
  "slide-0": {
    "shape-0": {
      "paragraphs": [
        { "text": "Presentation Title", "bold": true }
      ]
    },
    "shape-1": {
      "paragraphs": [
        { "text": "Subtitle text here" }
      ]
    }
  },
  "slide-1": {
    "shape-0": {
      "paragraphs": [
        { "text": "Slide Title", "bold": true }
      ]
    },
    "shape-1": {
      "paragraphs": [
        { "text": "First bullet point", "bullet": true, "level": 0 },
        { "text": "Second bullet point", "bullet": true, "level": 0 },
        { "text": "Third bullet point", "bullet": true, "level": 0 }
      ]
    }
  }
}
```

**IMPORTANT**: Shapes not listed will have their text cleared automatically.

#### Step 6: Apply replacements
```bash
python scripts/replace.py working.pptx replacement-text.json output.pptx
```

#### Step 7: Visual validation
```bash
python scripts/thumbnail.py output.pptx validation --cols 4
```

Check thumbnails for:
- Text cutoff at edges or bottom
- Text overlapping with other elements
- Positioning issues
- Content overflow

### ALTERNATIVE: Direct PptxGenJS Approach

Use this approach when:
- No KPMG template is available
- Creating simple presentations programmatically
- Content structure is well-defined

**CRITICAL LAYOUT CONSTRAINTS** (derived from KPMG template):

```javascript
// KPMG Layout Constants (in inches for PptxGenJS)
const L = {
  // Slide dimensions (16:9)
  slideWidth: 13.33,
  slideHeight: 7.5,

  // Horizontal positioning
  left: 1.08,           // Left margin (2.73cm)
  right: 12.25,         // Right edge (31.13cm from left)
  width: 11.17,         // Content width (28.40cm)

  // Vertical positioning - CRITICAL SAFE ZONES
  titleY: 0.48,         // Title position (1.23cm)
  strapY: 1.08,         // Strapline position (2.73cm)
  contentY: 1.47,       // Content start (3.73cm)
  safeBottom: 6.43,     // MAXIMUM Y for content (16.33cm) - NO CONTENT BELOW THIS

  // Element heights
  titleH: 0.55,
  strapH: 0.35,
  contentH: 4.96,       // Max content height with strapline (6.43 - 1.47)
  contentHFull: 5.50,   // Max content height without strapline

  // Two-column layout
  col1W: 5.35,
  col2X: 6.88,
  col2W: 5.35
};

// KPMG Brand Colors (NO # prefix for PptxGenJS!)
const KPMG = {
  blue: '00338D',
  darkBlue: '0C233C',
  pacificBlue: '00B8F5',
  lightBlue: 'ACEAFF',
  white: 'FFFFFF',
  black: '000000',
  grey1: '333333',
  grey2: '666666',
  grey3: '989898',
  grey5: 'E5E5E5',
  red: 'ED2124',
  yellow: 'F1C44D',
  green: '269924'
};
```

**CRITICAL RULES**:
1. **NEVER place content below Y = 6.43"** (the 16.33cm safe zone limit)
2. **NEVER use # prefix** in PptxGenJS colors - causes file corruption
3. **Always set `valign: 'top'`** on text boxes to prevent unexpected positioning
4. **Calculate table row heights** dynamically: `rowHeight = (L.safeBottom - contentY) / rowCount`
5. **Use `sizing: { type: 'contain' }`** for images to prevent overflow

## Font Installation & Troubleshooting

### Critical: Font Naming Mismatch

**Problem**: KPMG fonts from corporate IT install with:
- Family: `KPMG`
- Style: `Bold`

But the KPMG PowerPoint theme requests `KPMG Bold` as a **family name**. This causes PowerPoint to show the correct font name but render a fallback font instead.

**Symptoms**:
- Font dropdown shows "KPMG Bold (Headings)" but text looks wrong
- Headings render as serif font instead of sans-serif

### Fix: Rename Font Family with fonttools

```bash
pip3 install fonttools
```

```python
from fontTools.ttLib import TTFont
import os, shutil

# Backup and modify
src = os.path.expanduser("~/Library/Fonts/KPMG-Bold.ttf")
shutil.copy(src, src + ".backup")

font = TTFont(src)
for record in font['name'].names:
    try:
        text = record.toUnicode()
        if record.nameID in [1, 16] and text == "KPMG":
            encoding = 'utf-16-be' if record.platformID == 3 else 'mac_roman'
            record.string = "KPMG Bold".encode(encoding)
    except:
        pass
font.save(src)
```

Repeat for `KPMG-Bold Italic.ttf`, then restart PowerPoint.

### Verification
```bash
system_profiler SPFontsDataType | grep -A5 "KPMG-Bold.ttf"
# Should show: Family: KPMG Bold
```

## KPMG Brand Color Palette

### Primary Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **KPMG Blue** | `00338D` | 0, 51, 141 | Primary brand, headers |
| **Dark Blue** | `0C233C` | 12, 35, 60 | Cover slides, dark accents |
| **Pacific Blue** | `00B8F5` | 0, 184, 245 | Straplines, links |
| **Light Blue** | `ACEAFF` | 172, 234, 255 | Section dividers |

### Neutrals

| Name | Hex | RGB |
|------|-----|-----|
| Grey 1 | `333333` | 51, 51, 51 |
| Grey 2 | `666666` | 102, 102, 102 |
| Grey 3 | `989898` | 152, 152, 152 |
| Grey 5 | `E5E5E5` | 229, 229, 229 |

### RAG Status Colors

| Name | Hex | Usage |
|------|-----|-------|
| **Red** | `ED2124` | Risk, issues |
| **Yellow** | `F1C44D` | Caution, at risk |
| **Green** | `269924` | On track, complete |

## Typography

| Role | Font | Size | Usage |
|------|------|------|-------|
| **Headings** | KPMG Bold | 24-32pt | Slide titles |
| **Strapline** | Arial Italic | 12-14pt | Subtitles (Pacific Blue) |
| **Body** | Arial | 11-14pt | Bullets, text |
| **Footnotes** | Arial | 8-10pt | Legal, references (Grey 2) |

## Slide Layout Reference

### Master Slide Types

#### 1. Cover/Title Slide
- Background: Dark Blue (`0C233C`)
- Title: Large, white, KPMG Bold
- Subtitle: Pacific Blue
- Tagline: "KPMG. Make the Difference." at bottom

#### 2. Content Slide
- Background: White
- Title: KPMG Bold, Dark Blue, at 0.48" from top
- Strapline: Arial Italic, Pacific Blue, at 1.08" from top
- Content: Starts at 1.47", must end by 6.43"
- Footer zone: Below 6.43" (reserved for logo, legal, page number)

#### 3. Section Divider
- Background: Light Blue (`ACEAFF`)
- Title: Large, bold, black text, centered

## Visual Validation Checklist

After generating any presentation:

- [ ] All content above 6.43" (16.33cm) safe zone
- [ ] Titles align at 0.48" from top
- [ ] Straplines align at 1.08" from top
- [ ] Content starts at 1.47" from top
- [ ] Left margin consistent at 1.08"
- [ ] Tables don't extend below safe zone
- [ ] Images contained within safe zone
- [ ] Fonts rendering correctly (not fallback serif)

## Content Guidelines

### Maximum Content per Slide Type

| Slide Type | Max Items | Font Size |
|------------|-----------|-----------|
| Bullets (with strapline) | 6-8 | 13-14pt |
| Bullets (no strapline) | 8-10 | 13-14pt |
| Table rows | 5-6 (including header) | 11pt |
| Quote text | ~120 words | 18-20pt |
| Two-column bullets | 5-6 per column | 12pt |

### When Content Overflows

1. **Split the slide** - Create multiple slides
2. **Reduce font size** - Minimum 11pt
3. **Summarize** - Consolidate bullet points
4. **Use appendix** - Move detail to appendix slides

## Asset Locations

| Asset | Path |
|-------|------|
| KPMG Theme (PowerPoint) | `~/Library/Group Containers/UBF8T346G9.Office/User Content/Themes/KPMG Theme 2022.thmx` |
| Template Source | `/Users/barnabyrobson/Desktop/KPMG theme/Theme1.thmx` |
| Fonts | `~/Library/Fonts/KPMG*.ttf` |
| Color Reference | `/Users/barnabyrobson/Desktop/KPMG theme/KPMG Colours.jpg` |
| Master Slide Screenshots | `/Users/barnabyrobson/Desktop/KPMG theme/Slide Master*.png` |

## Best Practices

1. **Use template-based workflow** when possible - ensures proper positioning
2. **Always validate visually** with thumbnail grid after generation
3. **Respect the 6.43" safe zone** - footer area is reserved
4. **Use KPMG Bold for titles only** - Arial for all body text
5. **Include straplines** on content slides to summarize key messages
6. **Use Pacific Blue** for highlights and links
7. **Add "DRAFT FOR DISCUSSION PURPOSES ONLY"** watermark for internal docs

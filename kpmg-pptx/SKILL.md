---
name: kpmg-pptx
description: "Create KPMG-branded PowerPoint presentations. Use when creating presentations for KPMG work, applying KPMG styling, or when user mentions 'KPMG presentation', 'KPMG slides', or 'KPMG format'."
---

# KPMG PowerPoint Presentation Skill

Create professional PowerPoint presentations following KPMG Brand 2022 guidelines.

## Prerequisites

This skill extends the `pptx` skill. For general PowerPoint operations (reading, editing, workflows), refer to the pptx skill documentation.

**Required fonts** (must be installed on the system):
- KPMG Bold, KPMG Light, KPMG Thin, KPMG Extralight (with italics)
- KPMGLOGO1 (logo font)
- Arial (body text fallback)

Font location: `~/Library/Fonts/KPMG*.ttf`

**Theme file**: `/Users/barnabyrobson/Desktop/KPMG theme/Theme1.thmx`

## Font Installation & Troubleshooting

### Critical: Font Naming Mismatch

**Problem**: KPMG fonts from corporate IT install with:
- Family: `KPMG`
- Style: `Bold`

But the KPMG PowerPoint theme requests `KPMG Bold` as a **family name**. This causes PowerPoint to show the correct font name in the toolbar but render a fallback font (usually Times New Roman) instead.

**Symptoms**:
- Font dropdown shows "KPMG Bold (Headings)" but text looks wrong
- Headings render as serif font instead of sans-serif
- Presentations look correct on KPMG devices but broken on personal devices

### Fix: Rename Font Family with fonttools

**Step 1: Install fonttools**
```bash
pip3 install fonttools
```

**Step 2: Create backup and modify font**
```python
from fontTools.ttLib import TTFont
import os
import shutil

# Backup original
src = os.path.expanduser("~/Library/Fonts/KPMG-Bold.ttf")
shutil.copy(src, src + ".backup")

# Load and modify
font = TTFont(src)
for record in font['name'].names:
    try:
        text = record.toUnicode()
        # Change family name from "KPMG" to "KPMG Bold"
        if record.nameID in [1, 16] and text == "KPMG":
            encoding = 'utf-16-be' if record.platformID == 3 else 'mac_roman'
            record.string = "KPMG Bold".encode(encoding)
    except:
        pass

font.save(src)
```

**Step 3: Repeat for Bold Italic**
Run the same script for `~/Library/Fonts/KPMG-Bold Italic.ttf`

**Step 4: Clear font cache and restart PowerPoint**
```bash
# Clear macOS font cache
rm -rf ~/Library/Caches/com.apple.FontRegistry* 2>/dev/null
killall fontd 2>/dev/null

# Quit and reopen PowerPoint (Cmd+Q, not just close window)
```

### Verification

After fixing, verify the font registers correctly:
```bash
system_profiler SPFontsDataType | grep -A5 "KPMG-Bold.ttf"
```

Should show:
```
Family: KPMG Bold
Style: Bold
```

**NOT**:
```
Family: KPMG
Style: Bold
```

### Restoring Original Fonts

If needed, restore from backup:
```bash
cp ~/Library/Fonts/KPMG-Bold.ttf.backup ~/Library/Fonts/KPMG-Bold.ttf
cp "~/Library/Fonts/KPMG-Bold Italic.ttf.backup" "~/Library/Fonts/KPMG-Bold Italic.ttf"
```

## KPMG Brand Color Palette

### Primary Brand Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **KPMG Blue** | `#00338D` | 0, 51, 141 | Primary brand color, headers, emphasis |
| **Dark Blue** | `#0C233C` | 12, 35, 60 | Cover slides background, dark accents |
| **Cobalt Blue** | `#1E49E2` | 30, 73, 226 | Accent, links |
| **Pacific Blue** | `#00B8F5` | 0, 184, 245 | Highlights, hyperlinks |

### Extended Blue Palette

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **Blue** | `#76D2FF` | 118, 210, 255 | Light accents |
| **Light Blue** | `#ACEAFF` | 172, 234, 255 | Backgrounds, fills |
| **Blue Accent 1** | `#D2DBF9` | 210, 219, 249 | Subtle backgrounds |

### Chart Colors (Primary)

| Name | Hex | RGB |
|------|-----|-----|
| **Blue Gray** | `#34556D` | 52, 85, 109 |
| **Aqua** | `#77A8BE` | 119, 168, 190 |
| **Light Turquoise** | `#96CEE4` | 150, 206, 228 |
| **Grey 5** | `#E5E5E5` | 229, 229, 229 |

### Traffic Light / RAG Status Colors

| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| **Red** | `#ED2124` | 237, 33, 36 | Risk, issues, behind |
| **Yellow** | `#F1C44D` | 241, 196, 77 | Caution, at risk |
| **Green** | `#269924` | 38, 153, 36 | On track, complete |

### Secondary Palette

| Category | Dark | Medium | Light |
|----------|------|--------|-------|
| **Purple** | `#510DBC` | `#7213EA` | `#B497FF` |
| **Green** | `#008E7E` | `#00C0AE` | `#7AFFBD` |
| **Pink** | `#AB0D82` | `#FD349C` | `#FFA3DA` |

### Neutral Grays

| Name | Hex | RGB |
|------|-----|-----|
| Grey 1 | `#333333` | 51, 51, 51 |
| Grey 2 | `#666666` | 102, 102, 102 |
| Grey 3 | `#989898` | 152, 152, 152 |
| Grey 4 | `#B2B2B2` | 178, 178, 178 |
| Grey 5 | `#E5E5E5` | 229, 229, 229 |
| White | `#FFFFFF` | 255, 255, 255 |
| Black | `#000000` | 0, 0, 0 |

## Typography

### Font Scheme (KPMG Brand 2022)

| Role | Font | Usage |
|------|------|-------|
| **Major (Headings)** | KPMG Bold | Slide titles, section headers |
| **Minor (Body)** | Arial | Body text, bullets, tables |

### Font Weights Available

- **KPMG Bold** - Primary headings
- **KPMG Light** - Secondary text, subtitles
- **KPMG Thin** - Decorative, large display text
- **KPMG Extralight** - Delicate accents
- All weights available in Regular and Italic

### Text Hierarchy (Recommended Sizes)

| Element | Font | Size | Style |
|---------|------|------|-------|
| Slide Title | KPMG Bold | 28-36pt | Bold |
| Strapline/Subtitle | Arial | 14-16pt | Regular, KPMG Blue |
| Body Text | Arial | 11-14pt | Regular |
| Bullets | Arial | 11-14pt | Regular |
| Footnotes | Arial | 8-10pt | Regular, Grey 2 |

## Slide Layouts

### Slide Dimensions
- **Width**: 33.87cm (13.33 inches)
- **Height**: 19.05cm (7.5 inches)
- **Aspect Ratio**: 16:9 Widescreen

### Margins and Safe Zones
- **Left margin**: 2.73cm
- **Right margin**: 2.20cm (31.13cm from left)
- **Top margin**: 1.23cm
- **Bottom safe zone**: 16.33cm from top (NO CONTENT BELOW THIS LINE)
- **Content width**: ~28.40cm
- **Content height**: ~15.10cm

### Master Slide Types

#### 1. Cover/Title Slide
- **Background**: Dark Blue (`#0C233C`)
- **KPMG Logo**: Top-left, white
- **Title**: Large, white, KPMG Bold, left-aligned
- **Subtitle area**: Below title, stacked text boxes
- **Image placeholder**: Right side (~17.43cm from left)
- **Tagline**: "KPMG. Make the Difference." bottom-left

#### 2. Content Slide (Main)
- **Background**: White
- **Title**: Top, KPMG Bold, Dark Blue text
- **Strapline**: Below title, Pacific Blue, italic
- **Content area**: Two-column layout available
- **Footer**: KPMG logo bottom-left, legal text, page number
- **Color palette reference**: Left sidebar (for design guidance)
- **"DRAFT FOR DISCUSSION PURPOSES ONLY"**: Top-right (when applicable)

#### 3. Divider/Section Slide
- **Background**: Light Blue (`#ACEAFF`)
- **Title**: Large, bold, black text
- **Navigation icons**: Top-right (home, arrows)
- **Content box**: Centered, dashed border

## Creating Presentations with KPMG Styling

### Option A: Direct PptxGenJS (Recommended)

Use when creating structured presentations programmatically:

```javascript
const pptxgen = require('pptxgenjs');
const pptx = new pptxgen();

// KPMG Brand Setup
pptx.layout = 'LAYOUT_16x9';
pptx.author = 'KPMG';
pptx.company = 'KPMG';

// Define brand colors
const KPMG = {
  blue: '00338D',
  darkBlue: '0C233C',
  pacificBlue: '00B8F5',
  lightBlue: 'ACEAFF',
  white: 'FFFFFF',
  grey1: '333333',
  grey5: 'E5E5E5',
  red: 'ED2124',
  yellow: 'F1C44D',
  green: '269924'
};

// Cover Slide
function addCoverSlide(pptx, title, subtitle) {
  const slide = pptx.addSlide();
  slide.background = { color: KPMG.darkBlue };

  // Title
  slide.addText(title, {
    x: 1.0, y: 1.5, w: 6, h: 1.5,
    fontSize: 36, bold: true, color: KPMG.white,
    fontFace: 'KPMG Bold'
  });

  // Subtitle
  slide.addText(subtitle, {
    x: 1.0, y: 3.2, w: 6, h: 0.8,
    fontSize: 16, color: KPMG.white,
    fontFace: 'Arial'
  });

  // Tagline
  slide.addText('KPMG. Make the Difference.', {
    x: 1.0, y: 6.5, w: 4, h: 0.4,
    fontSize: 12, color: KPMG.white,
    fontFace: 'Arial'
  });
}

// Content Slide
function addContentSlide(pptx, title, strapline, bullets) {
  const slide = pptx.addSlide();
  slide.background = { color: KPMG.white };

  // Title
  slide.addText(title, {
    x: 1.0, y: 0.5, w: 11, h: 0.8,
    fontSize: 28, bold: true, color: KPMG.darkBlue,
    fontFace: 'KPMG Bold'
  });

  // Strapline
  if (strapline) {
    slide.addText(strapline, {
      x: 1.0, y: 1.3, w: 11, h: 0.5,
      fontSize: 14, italic: true, color: KPMG.pacificBlue,
      fontFace: 'Arial'
    });
  }

  // Bullets
  slide.addText(bullets.map(b => ({ text: b, options: { bullet: true } })), {
    x: 1.0, y: 2.0, w: 11, h: 4.5,
    fontSize: 14, color: KPMG.grey1,
    fontFace: 'Arial',
    paraSpaceAfter: 8
  });
}

// Section Divider
function addSectionSlide(pptx, sectionTitle) {
  const slide = pptx.addSlide();
  slide.background = { color: KPMG.lightBlue };

  slide.addText(sectionTitle, {
    x: 1.5, y: 2.5, w: 10, h: 2,
    fontSize: 44, bold: true, color: '000000',
    fontFace: 'KPMG Bold',
    align: 'left'
  });
}
```

### Option B: Using the Theme File

When creating presentations in PowerPoint directly, apply the theme:

1. Open PowerPoint
2. Go to **Design > Themes > Browse for Themes**
3. Select `/Users/barnabyrobson/Desktop/KPMG theme/Theme1.thmx`

### Option C: html2pptx with KPMG Styling

When using the html2pptx workflow from the pptx skill, apply these CSS styles:

```css
/* KPMG Brand Styles */
:root {
  --kpmg-blue: #00338D;
  --kpmg-dark-blue: #0C233C;
  --kpmg-pacific-blue: #00B8F5;
  --kpmg-light-blue: #ACEAFF;
}

body {
  font-family: Arial, sans-serif;
  color: #333333;
}

h1, h2, h3 {
  font-family: 'KPMG Bold', Arial, sans-serif;
  color: var(--kpmg-dark-blue);
}

.slide-title {
  font-size: 28pt;
  font-weight: bold;
  color: var(--kpmg-dark-blue);
}

.strapline {
  font-size: 14pt;
  font-style: italic;
  color: var(--kpmg-pacific-blue);
}

.cover-slide {
  background-color: var(--kpmg-dark-blue);
  color: white;
}

.divider-slide {
  background-color: var(--kpmg-light-blue);
}
```

## Asset Locations

| Asset | Path |
|-------|------|
| Theme file | `/Users/barnabyrobson/Desktop/KPMG theme/Theme1.thmx` |
| Fonts | `~/Library/Fonts/KPMG*.ttf` |
| Color reference | `/Users/barnabyrobson/Desktop/KPMG theme/KPMG Colours.jpg` |
| Cover layout | `/Users/barnabyrobson/Desktop/KPMG theme/Slide Master_Cover.png` |
| Content layout | `/Users/barnabyrobson/Desktop/KPMG theme/Slide Master main.png` |
| Divider layout | `/Users/barnabyrobson/Desktop/KPMG theme/Slide Master_Divider.png` |

## Common Slide Patterns

### Executive Summary
- Cover slide with client name/project
- Agenda slide (numbered bullets)
- Key findings (2-column layout)
- Recommendations
- Next steps

### Status Report
- Cover with date
- Traffic light RAG summary
- Workstream status (use RAG colors)
- Risks and issues
- Key milestones

### Proposal
- Cover slide
- About KPMG
- Understanding your needs
- Our approach
- Team/credentials
- Commercial terms

## Best Practices

1. **Never place content below 16.33cm** from the top (footer zone)
2. **Use KPMG Blue** for primary emphasis, Pacific Blue for links/highlights
3. **Maintain contrast**: Dark text on light backgrounds, white text on dark backgrounds
4. **Include straplines** on content slides to summarize key messages
5. **Use the color palette consistently** - avoid colors outside the brand palette
6. **Legal footer**: Include appropriate disclaimers on client-facing materials
7. **Draft watermark**: Add "DRAFT FOR DISCUSSION PURPOSES ONLY" for internal documents

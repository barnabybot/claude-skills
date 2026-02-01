---
name: nano-banana
description: Generate images using Nano Banana (Google Gemini Image Generation). Use when creating infographics, diagrams, presentation graphics, or any visual content.
triggers:
  - nano banana
  - generate image
  - create graphic
  - create infographic
  - gemini image
---

# Nano Banana - Gemini Image Generation

Nano Banana is the nickname for Google's Gemini image generation model. It excels at:
- Rendering text accurately in images
- Following complex spatial/layout instructions
- Creating professional infographics and diagrams

## Model

Current model: `gemini-2.0-flash-exp-image-generation`

## Prompting Style

Use clear, descriptive English sentences with explicit layout instructions. **Always use GitHub/Apple style** for clean, professional output.

### Prompt Template

```
You are generating a professional presentation graphic.

IMPORTANT: Do NOT include any meta-text or instructions in the image itself. Only render the specific content described below.

Style: GitHub/Apple design - ultra-clean, minimal, white background, flat vector icons, no gradients or shadows. 16:9 aspect ratio, high resolution.

CONTENT TO RENDER:

[Describe layout and elements here]
```

### GitHub/Apple Style Rules

| Element | Specification |
|---------|---------------|
| Background | Pure white (#FFFFFF) |
| Primary accent | Muted blue (#0969DA) |
| Secondary | Gray (#656D76) |
| Icons | Simple outlined, thin 2px strokes, not filled |
| Typography | Clean sans-serif, sparse text |
| Effects | NO gradients, NO shadows, NO 3D, NO texture |
| Spacing | Generous padding and whitespace |
| Aspect ratio | 16:9 (1920x1080 proportions) |

### Key Principles

1. **Prefix with meta-instructions**: Tell the model NOT to render instructions as text
2. **Explicit spatial layout**: "Split screen", "Three-panel horizontal", "Centered row"
3. **Specify exact colors**: Use hex codes (#0969DA, #F97316)
4. **Describe each element**: Icons, text, positioning
5. **State what NOT to include**: "DO NOT put text at the top"

### Example Prompt

```
You are generating a professional presentation graphic.

IMPORTANT: Do NOT include any meta-text or duplicate elements. Only render EXACTLY what is described below.

Style: GitHub/Apple design - ultra-clean, minimal, white background, flat vector icons, no gradients or shadows. 16:9 aspect ratio, high resolution.

CONTENT TO RENDER:

Two rounded rectangles side by side with space between.

LEFT BOX (light blue tint #EBF5FF):
- Header: "Before"
- Folder icon with nested subfolders
- Muted gray tones

RIGHT BOX (light gray tint #F6F8FA):
- Header: "After"
- Flat files with tag icons
- Blue accent (#0969DA)

CENTER: Arrow pointing left to right

BOTTOM: Text "Files over folders"
```

## Python Script Usage

Location: `~/Desktop/generate_presentation_graphics.py`

### Setup

1. Get API key from https://aistudio.google.com/app/apikey
2. Run script - it will prompt to save the key

### Commands

```bash
# Generate all preset images
python3 ~/Desktop/generate_presentation_graphics.py

# Custom prompt
python3 ~/Desktop/generate_presentation_graphics.py \
  --prompt "Your detailed prompt here" \
  --output my-image-name

# Specify output directory
python3 ~/Desktop/generate_presentation_graphics.py \
  --output-dir /path/to/folder

# List available presets
python3 ~/Desktop/generate_presentation_graphics.py --list
```

### API Key Storage

Key is stored in **macOS Keychain** (service: `nano-banana`, account: `google-api-key`)

```bash
# Save key to Keychain
python3 ~/Desktop/generate_presentation_graphics.py --save-key YOUR_KEY

# Or manually via security command
security add-generic-password -s nano-banana -a google-api-key -w "YOUR_KEY"

# Retrieve key
security find-generic-password -s nano-banana -a google-api-key -w
```

For cross-device sharing, also store in KeePassXC vault at:
`/Users/barnabyrobson/Library/Mobile Documents/com~apple~CloudDocs/KeyPassXC/Clawdbot-vault.kdbx`

## Python SDK Direct Usage

```python
from google import genai
from google.genai import types

client = genai.Client(api_key="YOUR_KEY")

response = client.models.generate_content(
    model="gemini-2.0-flash-exp-image-generation",
    contents="Your prompt here",
    config=types.GenerateContentConfig(
        response_modalities=["image", "text"],
    ),
)

# Extract image
for part in response.candidates[0].content.parts:
    if part.inline_data is not None:
        with open("output.png", "wb") as f:
            f.write(part.inline_data.data)
```

## Style Guidelines (GitHub/Apple - Preferred)

**Always use GitHub/Apple style** for clean, professional presentation graphics.

| Element | Specification |
|---------|---------------|
| Background | Pure white (#FFFFFF) |
| Primary accent | GitHub blue (#0969DA) |
| Secondary | Gray (#656D76) |
| Warm accents | Orange (#F97316), Yellow (#FBBF24) |
| Icons | Outlined, thin 2px strokes, NOT filled |
| Containers | Light tinted boxes (#EBF5FF blue, #F6F8FA gray) |
| Typography | Clean sans-serif, sparse text |
| Effects | NO gradients, NO shadows, NO 3D, NO texture |
| Spacing | Generous padding and whitespace |
| Aspect ratio | 16:9 for presentations |

**Critical:** Always prefix prompts with instructions telling the model NOT to render meta-text as visible content.

## Troubleshooting

**"Model not found"**: Check model name is exactly `gemini-2.0-flash-exp-image-generation`

**No image in response**: Model may have returned text instead. Check the text output for why it couldn't generate.

**API key errors**: Ensure key is from Google AI Studio (not Vertex AI)

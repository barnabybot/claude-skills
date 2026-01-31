---
name: midjourney
description: Generate AI portraits using Midjourney Alpha web interface. Use when user wants to create portraits, generate images via Midjourney, or batch-generate images for Obsidian People notes. Automates browser-based Midjourney workflow.
---

# Midjourney Portrait Generator

Automates Midjourney Alpha (https://alpha.midjourney.com) to generate portraits and save them to Obsidian vault.

## Requirements

- Python 3.11 with Playwright installed
- Logged-in Midjourney session (run `--login` first)
- Obsidian vault with People notes in `References/People/`

## Usage

```bash
# First time: Login to Midjourney (opens browser)
/opt/homebrew/bin/python3.11 ~/.claude/skills/midjourney/mjgen.py --login

# List people needing portraits
/opt/homebrew/bin/python3.11 ~/.claude/skills/midjourney/mjgen.py --list

# Test with one person
/opt/homebrew/bin/python3.11 ~/.claude/skills/midjourney/mjgen.py --test "Person Name"

# Generate all missing portraits
/opt/homebrew/bin/python3.11 ~/.claude/skills/midjourney/mjgen.py --all
```

## How It Works

1. Opens Midjourney Alpha with saved browser session
2. For each person without a `feature:` image:
   - Types prompt: `{Name} painted by Quentin Blake --ar 1:1 --s 150`
   - Submits with Enter key
   - Waits 60s for generation (MJ creates 4 images per prompt)
   - Clicks first image to open large view
   - Screenshots largest visible image
   - Saves to `Attachments/{Name}.png`
   - Updates person's markdown file with `feature: Attachments/{Name}.png`
3. Waits 10s between people (rate limiting)

## Configuration

Edit `mjgen.py` to customize:
- `PEOPLE_TO_GENERATE` list - people to process
- `get_prompt()` - change art style/parameters
- `ATTACHMENTS_DIR` / `PEOPLE_DIR` - vault paths

## Troubleshooting

**Browser won't start**: Delete `~/.midjourney-automation/SingletonLock`

**Session expired**: Run `--login` again

**Images not saving**: Check Attachments folder permissions

**Markdown files not updating**: Obsidian caches files in memory. See "Updating Obsidian Files" below.

## Updating Obsidian Files

The script updates markdown files with `feature: Attachments/{name}.png`. However, **Obsidian will revert these changes if it's running**.

### Required Workflow

1. **Quit Obsidian before running `--all`**
   ```bash
   osascript -e 'quit app "Obsidian"'
   rm -f "/path/to/vault/.obsidian/workspace.json"
   ```

2. **Run the generation**
   ```bash
   python3.11 ~/.claude/skills/midjourney/mjgen.py --all
   ```

3. **Reopen Obsidian** after generation completes

### If Files Get Reverted

If you ran with Obsidian open and changes were reverted:

```bash
# Quit Obsidian and clear cache
osascript -e 'quit app "Obsidian"'
rm -f "/path/to/vault/.obsidian/workspace.json"

# Re-add feature properties
python3 << 'EOF'
from pathlib import Path
attachments = Path("/path/to/vault/Attachments")
people_dir = Path("/path/to/vault/References/People")

for md in people_dir.glob("*.md"):
    name = md.stem
    if (attachments / f"{name}.png").exists():
        content = md.read_text()
        if f"feature: Attachments/{name}.png" not in content:
            content = content.replace(
                '  - "[[People]]"\n',
                f'  - "[[People]]"\nfeature: Attachments/{name}.png\n'
            )
            md.write_text(content)
EOF

# Reopen Obsidian
open -a Obsidian
```

## Key Implementation Details

- Uses Playwright for browser automation
- Fixed 60s wait (image count unreliable due to lazy loading)
- Screenshots element instead of downloading URL (CDN requires auth)
- Dismisses suggestion dropdown before submitting (Escape key)
- MJ generates 4 images per prompt; script takes the first one
- People Base uses `image: feature` property for card thumbnails

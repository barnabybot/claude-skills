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

## Key Implementation Details

- Uses Playwright for browser automation
- Fixed 60s wait (image count unreliable due to lazy loading)
- Screenshots element instead of downloading URL (CDN requires auth)
- Dismisses suggestion dropdown before submitting (Escape key)

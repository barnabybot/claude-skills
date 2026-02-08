---
name: clip
description: "Process Obsidian web clippings: categorize, add topics, normalize frontmatter, and add backlinks. Use when the user says /clip, 'process clippings', 'categorize articles', 'process tweets', 'normalize clippings', or wants to process items in Clippings/ subfolders (Articles, Tweets, Books, Podcasts). Handles Readwise imports, Obsidian Web Clipper content, and any note with [[Inbox]] category that needs processing."
---

# Clip

Process Obsidian web clippings in the Core vault. Categorize content, normalize frontmatter, add topics, and insert backlinks following the Kepano method.

## Vault

`/Users/barnabyrobson/Library/Mobile Documents/iCloud~md~obsidian/Documents/Core`

## Arguments

- `/clip` - Process all `[[Inbox]]` items across Clippings/ subfolders
- `/clip <file-path>` - Process a single file
- `/clip <folder>` - Process a folder (e.g., `/clip Clippings/Articles`)
- `/clip all` - Process everything in all Clippings/ subfolders

## Workflow

### 1. Find Files to Process

If no argument given, find all files with `[[Inbox]]` in categories:
```bash
grep -rl '\[\[Inbox\]\]' "VAULT/Clippings/" --include="*.md"
```

If a folder is given, process all `.md` files in that folder.

### 2. Determine Clipping Type

Detect type from file location or frontmatter:

| Location | Type | Category |
|----------|------|----------|
| `Clippings/Articles/` | Article | `[[Clippings]]` |
| `Clippings/Tweets/` | Tweet | `[[Clippings]]` |
| `Clippings/Books/` | Book | `[[References]]`, `[[Books]]` |
| `Clippings/Podcasts/` | Podcast | `[[Podcast episodes]]` |
| `Clippings/Voice Memos/` | Voice Memo | `[[Clippings]]` |
| `Clippings/Youtube/` | YouTube | `[[Clippings]]` |

### 3. Update Frontmatter

For each file:

**a) Remove `[[Inbox]]` from categories**

**b) Set correct categories** (as wikilinks in list format):
- Articles: `[[Clippings]]`
- Tweets: `[[Clippings]]` (type: `[[Tweets]]`)
- Books: `[[References]]`, `[[Books]]` (use normalize-books.py patterns)
- Podcasts: `[[Podcast episodes]]` (use normalize-podcasts.py patterns)

**c) Assign topics** (up to 5, as wikilinks):
Read content and assign from vault taxonomy. Common topics:
- Tech: `[[AI]]`, `[[Programming]]`, `[[Crypto]]`, `[[Web3]]`
- Finance: `[[Investing]]`, `[[Macro]]`, `[[Stocks]]`, `[[Venture Capital]]`
- Ideas: `[[Mental Models]]`, `[[Philosophy]]`, `[[Psychology]]`, `[[Productivity]]`
- Life: `[[Health]]`, `[[Fitness]]`, `[[Travel]]`, `[[Design]]`
- Meta: `[[Obsidian]]`, `[[Claude Code]]`, `[[Twitter]]`

**d) Ensure standard properties exist:**
- `categories`: list of wikilinks
- `topics`: list of wikilinks
- `author`: wikilink if identifiable
- `type`: wikilink (`[[Articles]]`, `[[Tweets]]`, `[[Books]]`, `[[Podcasts]]`)
- `created`: YYYY-MM-DD

**e) For Books specifically** - run the normalize-books pattern:
- Google Books API lookup for genre/description
- Set genre (Biography, Non-Fiction, Fiction, Philosophy)
- Extract people profiled for biographies
- Add `to-read` tag if no rating

**f) For Podcasts specifically** - run the normalize-podcasts pattern:
- Extract show name, guest names, episode number
- Set show as wikilink

### 4. Add Backlinks (Kepano Method)

After frontmatter is set, add wikilinks throughout the body:

- **First mention only** of each entity
- Link people: `[[Person Name]]`
- Link concepts: `[[Mental Models]]`, `[[Compounding]]`, etc.
- Link places/companies: `[[HSBC]]`, `[[Hong Kong]]`
- Unresolved links are fine - they serve as breadcrumbs

**Skip linking inside:**
- YAML frontmatter
- Code blocks
- URLs
- Already-linked terms
- Headings (leave clean)

**Use display text when needed:** `[[Full Name|short name]]`

### 5. Batch Processing

For large batches (>5 files), dispatch parallel Opus agents:
- Group files by type (Articles, Tweets, Books, Podcasts)
- Each agent processes 3-5 files
- Use `subagent_type=Explore` for reading, regular Task for writing

### 6. Report Results

After processing, output a summary:
```
Processed 12 clippings:
  Articles: 5 (topics: AI, Investing, Programming...)
  Tweets: 4 (topics: Crypto, AI, Startups...)
  Books: 2 (genres: Non-Fiction, Biography)
  Podcasts: 1 (show: All-In Podcast)

Changes:
  - Removed [[Inbox]] from 12 files
  - Added topics to 12 files
  - Added backlinks to 8 files (47 links total)
  - Normalized book frontmatter: 2 files
  - Normalized podcast frontmatter: 1 file
```

## YAML Format Rules

- Property names: lowercase, plural for lists
- Wikilinks in YAML: quoted (`"[[Topic]]"`)
- Lists use dash format:
```yaml
categories:
  - "[[Clippings]]"
topics:
  - "[[AI]]"
  - "[[Investing]]"
author: "[[Person Name]]"
type: "[[Articles]]"
created: 2026-01-15
```

## Existing Scripts

The vault has automation scripts at `.claude/auto-categorize/` that run hourly via LaunchAgent. This skill provides interactive, higher-quality processing with backlinks that the automated scripts don't add.

Key scripts for reference (patterns, not to execute directly):
- `categorize.py` - Topic detection patterns for tweets/clippings
- `normalize-books.py` - Book frontmatter normalization with Google Books API
- `normalize-podcasts.py` - Podcast frontmatter normalization
- `add_internal_links.py` - Entity linking using vault database

## Quality Checks

Before marking complete:
- [ ] No `[[Inbox]]` categories remain
- [ ] All files have at least 1 topic
- [ ] YAML is valid (no syntax errors)
- [ ] Wikilinks are quoted in YAML
- [ ] Backlinks added to body (first mentions only)
- [ ] No links inside code blocks or URLs

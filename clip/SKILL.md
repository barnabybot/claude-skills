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
- `/clip fix-formatting` - Run only step 3c (formatting cleanup) on all articles in `Clippings/Articles/`. Skips inbox processing, frontmatter, and backlinks. Use for retroactive cleanup of already-processed articles.

## Workflow

### 1. Find Files to Process

If no argument given, find all files with `[[Inbox]]` in categories:
```bash
grep -rl '\[\[Inbox\]\]' "VAULT/Clippings/" --include="*.md"
```

If a folder is given, process all `.md` files in that folder.

### 1b. Check for Misfiled Content

Before processing, detect files in the wrong location:

- **Files in `Clippings/` root**: Should be in a subfolder. Determine type from content/URL and move using Obsidian CLI `move` with `path=` syntax.
- **Personal content in Clippings/**: If content has no external source (user's own writing, session logs), recategorize to `[[Journals]]` or `[[Essays]]` and flag for move to vault root.
- **X articles in Tweets/**: See step 2b below — long-form X articles should be in Articles/, not Tweets/.

### 1c. Sanitize Frontmatter Keys

Web clippers sometimes create malformed YAML keys. Before processing content, scan for and fix:
- **Trailing whitespace in keys**: e.g., `"published "` → `published` (common web clipper artifact)
- **Inconsistent type values**: `[[Tweet]]` (singular) → `[[Tweets]]` (plural, per vault standard)

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

### 2b. X Article Detection (IMPORTANT)

X (formerly Twitter) has a native articles feature. Long-form X posts are articles, not tweets. **Always check content structure**, not just URL origin.

**Classify as Article** (move to `Clippings/Articles/`, type `[[Articles]]`):
- Structured long-form prose with headings (##), multiple sections/parts
- Reads like a blog post or essay (continuous narrative)
- Typically 200+ lines of content
- Often has code examples, step-by-step guides, or structured arguments
- May be cross-posted to a blog

**Classify as Tweet** (stays in `Clippings/Tweets/`, type `[[Tweets]]`):
- Short posts, even if the text is long (e.g., a single prompt template share)
- Numbered thread format (`1/N`, `2/N`, etc. with `(View Tweet)` links)
- Podcast clip excerpts or quote shares
- Image-only posts with brief caption

**Heuristics** (check in order):
1. Does it have `## Part N:` or `## Step N:` section headings? → Article
2. Is it numbered tweet format (`1/206`, `(View Tweet)`)? → Tweet thread
3. Is body content > 200 lines of continuous prose? → Likely article
4. Is it < 60 lines? → Likely tweet
5. When ambiguous, read the content — if it reads like a blog post, it's an article

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

### 3b. Obsidian CLI (Preferred When Obsidian Running)

When Obsidian 1.12+ is running, **prefer CLI commands over direct file editing** for property changes:

```bash
OBS="/Applications/Obsidian.app/Contents/MacOS/obsidian"

# Remove [[Inbox]] from categories
$OBS vault=Core property:remove name=categories path="Clippings/Tweets/Note Name.md"

# Set correct categories
$OBS vault=Core property:set name=categories value="[[Clippings]]" type=list path="Clippings/Tweets/Note Name.md"

# Add topics
$OBS vault=Core property:set name=topics value="[[AI]]" type=list path="Clippings/Tweets/Note Name.md"

# Set author
$OBS vault=Core property:set name=author value="[[Person Name]]" path="Clippings/Tweets/Note Name.md"

# Set type
$OBS vault=Core property:set name=type value="[[Articles]]" path="Clippings/Tweets/Note Name.md"

# Move file (updates all backlinks automatically)
$OBS vault=Core move path="Clippings/Tweets/Note Name.md" to="Clippings/Articles/Note Name.md"
```

**Why CLI**: No need to read the file first (saves tokens). Properties are set atomically. Use direct file editing only for body content changes (backlinks) or when Obsidian isn't running.

**IMPORTANT**: Use `path=` (not `file=`) for files in subfolders. `file=` only works for vault-root files.

**Note**: `property:remove` removes the entire property. To replace categories, remove first then set the new value.

**Escaping `$` in filenames**: Bash interprets `$` as a variable (e.g., `$800` becomes empty). For files with `$` in the name, use python `subprocess.run()` or ensure the entire path is in single quotes. The Read/Edit tools handle `$` in paths correctly — this only affects Bash/CLI commands.

**CLI double-quoting**: `property:set` sometimes wraps values as `'"[[Articles]]"'` (extra quote layer). Always verify with a read after setting properties via CLI. If double-quoted, re-run without the outer quotes or use direct file Edit.

**CLI list properties are BROKEN for multiple values**: `property:set` with `type=list` and comma-separated values creates a SINGLE STRING, not a list. For example, `value='[[Crypto]],[[Philosophy]],[[Web3]]'` produces `topics: "[[Crypto]],[[Philosophy]],[[Web3]]"` (one string) instead of three separate list items. **For multi-value list properties (topics, categories), always use direct file Edit with YAML dash format instead of CLI.** CLI is safe only for single-value lists (e.g., `categories=[[Clippings]]`) or scalar properties (author, type).

### 3c. Clean Web Clipper Body Formatting

Web clippers (especially from X/Twitter articles and Substack) produce broken markdown. Fix these **before** adding backlinks:

#### Empty Headings
Clipper creates `## ` with heading text on the next line:
```
##

What you actually need before you start
```
→ Merge into one heading, collapse surrounding blank lines:
```
## What you actually need before you start
```
Also detect doubled empty headings (section break artifact):
```
##

The actual setup

##
```
→ Single heading: `## The actual setup`

#### Multi-line Image Links
Clipper wraps images in clickable links but splits the markdown:
```
[

![Image](https://pbs.twimg.com/media/xxx.jpg)




](https://x.com/.../media/...)
```
→ Collapse to a clean image embed. Strip the outer link wrapper:
```
![Image](https://pbs.twimg.com/media/xxx.jpg)
```

#### Split Inline Links
Clipper puts links on their own line, breaking mid-sentence:
```
lets your agent search the web. Sign up at

[brave.com/search/api](https://brave.com/search/api)

. Takes two minutes.
```
→ Join inline with surrounding text:
```
lets your agent search the web. Sign up at [brave.com/search/api](https://brave.com/search/api). Takes two minutes.
```
Same pattern with `[@handle](url)` links:
```
search for

[@BotFather](https://x.com/@BotFather)

, send a message
```
→ `search for [@BotFather](https://x.com/@BotFather), send a message`

#### Fake Filename Links
Clippers turn `.md` and `.sh` filenames into links to TLD domains:
```
[CLAUDE.md](https://claude.md/)
[SOUL.md](https://soul.md/)
[skills.sh](https://skills.sh/)
```
→ Convert to inline code (these are filenames, not web links):
```
`CLAUDE.md`
`SOUL.md`
`skills.sh`
```
**Detection**: Link text ends in `.md` or `.sh`, URL is `https://<same-name>/` (TLD domain, not a real page).

#### Split Italics / Bold
Clipper isolates emphasized words on their own line:
```
the work becomes

*increasingly*

important
```
→ `the work becomes *increasingly* important`

#### Split Footnote References
Clipper breaks `[N]` footnote markers across lines:
```
[

1

]
```
→ `[1]`

#### Twitter UI Chrome
X article clippings sometimes include page furniture at the top (e.g., "View keyboard shortcuts", profile badges, follower counts). Remove these — they're not article content.

#### Redundant Code Block Language Labels
Clipper renders code tab labels as bare words before fenced blocks:
```
bash
​```bash
npm install -g openclaw
​```
```
→ Remove the bare `bash` / `json` / `python` line before the fenced block (the language is already specified in the fence).

#### Excessive Blank Lines
X article clippings often have 3+ consecutive blank lines and `  ` (two-space) lines used as spacers. Normalize to max 1 blank line between paragraphs. Remove lines that are just whitespace.

#### When to Apply
These fixes apply primarily to **Articles** clipped from X/Twitter and Substack. Tweets and Books rarely have these issues. Run formatting cleanup on any article with:
- `x.com` or `twitter.com` in the `url` frontmatter field
- `substackcdn.com` image URLs in the body
- Any `## ` (empty heading) detected in the file

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
- Group files by **complexity**, not just type
- **Heavy files** (50+ fixes, e.g., Mission Control with 50 empty headings): solo agent
- **Medium files** (10-30 fixes): pair 2 per agent
- **Light files** (1-5 fixes): group 3-4 per agent
- Use `subagent_type=general-purpose` with `mode=dontAsk` for writing
- For `/clip fix-formatting`, scan for patterns first (grep for `^## $`, `^\[$`, fake `.md` links) to estimate fix counts before grouping

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
- [ ] YAML is valid (no syntax errors, no trailing whitespace in keys)
- [ ] Wikilinks are quoted in YAML
- [ ] Type values use plural form (`[[Tweets]]` not `[[Tweet]]`, `[[Articles]]` not `[[Article]]`)
- [ ] X articles are in `Clippings/Articles/` with type `[[Articles]]`, not in Tweets/
- [ ] No personal content miscategorized as `[[Clippings]]`
- [ ] Backlinks added to body (first mentions only)
- [ ] No links inside code blocks or URLs
- [ ] No empty headings (`## ` with no text)
- [ ] No broken multi-line image links (`[` and `](url)` on separate lines)
- [ ] No split inline links (link on its own line mid-sentence)
- [ ] No fake `.md`/`.sh` filename links (e.g., `[CLAUDE.md](https://claude.md/)` → `` `CLAUDE.md` ``)
- [ ] No excessive blank lines (max 1 between paragraphs)

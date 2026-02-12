---
name: organize
description: Organize and maintain the Core Obsidian vault. Audit filing locations, fix YAML frontmatter, assign categories/topics, and add backlinks. Use when user says "organize", "audit vault", "fix frontmatter", "process inbox", "check vault health", or provides a file/folder path to organize. Accepts arguments - a file path, folder path, "inbox" (process [[Inbox]] items), or "audit" (full vault health check).
---

# Organize

Vault organization and maintenance for the Core Obsidian vault.

**Vault**: `/Users/barnabyrobson/Library/Mobile Documents/iCloud~md~obsidian/Documents/Core`

**Always read the vault's `CLAUDE.md` first** for current filing rules and property standards.

## Arguments

| Argument | Action |
|----------|--------|
| `<file-path>` | Organize a single file (fix frontmatter, location, backlinks) |
| `<folder-path>` | Organize all files in a folder |
| `inbox` | Process all notes with `[[Inbox]]` category |
| `audit` | Full vault health check with stats report |
| *(none)* | Default to `inbox` |

## Filing Rules (Kepano Method)

### Location Decision Tree

1. **Did someone else write it?** → `Clippings/` subfolder:
   - Articles/essays → `Clippings/Articles/`
   - Tweets/X posts → `Clippings/Tweets/`
   - Podcast episodes → `Clippings/Podcasts/`
   - Book highlights → `Clippings/Books/`
   - Voice memos → `Clippings/Voice Memos/`
   - YouTube → `Clippings/Youtube/`
2. **Is it about an external thing?** → `References/`
   - People → `References/People/`
   - Companies, products, places → `References/`
3. **Is it personal writing/thinking?** → **Root**

### Category Assignment

| Content Type | Categories |
|-------------|-----------|
| Personal essay/writing | `[[Essays]]`, `[[Writing]]` |
| Idea/thought fragment | `[[Thoughts]]` |
| Journal entry | `[[Journal]]` |
| Article by others | `[[Clippings]]` |
| Book highlights | `[[Books]]` |
| Podcast episode | `[[Podcast episodes]]` |
| Tweet/X post | `[[Clippings]]` |
| Person reference | `[[People]]` |
| Company reference | `[[Companies]]` |
| Quote | `[[Quotes]]` |
| Recipe | `[[Recipes]]` |
| Meeting notes | `[[Meetings]]` |

## YAML Frontmatter Standards

### Required Fields

Every note must have:
- `created`: YYYY-MM-DD format
- `categories`: list of wikilinks

### Property Rules

- **Names**: lowercase, plural for lists (e.g., `categories`, `topics`, `tags`)
- **Values**: Title Case for wikilink entries (e.g., `"[[Mental Models]]"`)
- **Wikilinks**: categories, topics, author, source, type, genre all use `"[[Value]]"` format
- **Standard properties**: categories (list), topics (list), author (single/list), source (single), type (single), genre (single/list), rating (number 1-7), created (date), published (date), status (text)

### Common Fixes

| Problem | Fix |
|---------|-----|
| `Categories:` (uppercase) | → `categories:` |
| `topic:` (singular list) | → `topics:` |
| `categories: [[Essays]]` (not list) | → `categories:\n  - "[[Essays]]"` |
| Missing `created` | Add from file creation date or content |
| `[[Inbox]]` still present | Remove after proper category assigned |
| Properties with bare text instead of wikilinks | Wrap in `"[[...]]"` |

## Workflow: Single File / Folder

### Step 1: Read and Analyze

For each file:
1. Read frontmatter and content
2. Determine content type (who wrote it, what is it about)
3. Check current location against decision tree
4. Check frontmatter completeness and correctness
5. Identify missing backlinks in body text

### Step 2: Present Changes

```
## filename.md
- **Location**: root → Clippings/Articles/ (move needed)
- **Frontmatter fixes**:
  - Add: categories: ["[[Clippings]]"]
  - Add: topics: ["[[AI]]", "[[Investing]]"]
  - Fix: created: 2026-01-15
  - Remove: [[Inbox]]
- **Backlinks**: 3 first-mention links to add
```

### Step 3: Execute with Confirmation

Ask for approval before applying. Group changes:
- **Auto-approve**: Remove `[[Inbox]]` from already-categorized files in correct location
- **Confirm**: File moves, category changes, topic additions

## Workflow: Inbox Mode

1. Find all files containing `[[Inbox]]` in categories (exclude Templates/, .trash)
2. Group by action type:
   - **Ready**: Correct location + categories, just remove `[[Inbox]]`
   - **Need category fix**: Wrong or missing categories
   - **Need move**: File in wrong location
   - **Need topics**: No topics assigned
3. Present grouped summary
4. Execute approved changes

## Workflow: Audit Mode

Scan the entire vault and report:

```
## Vault Health Report

### Filing Issues
- X files in wrong location (list top 10)
- X files missing categories
- X files with [[Inbox]] still pending

### Frontmatter Issues
- X files missing `created` date
- X files with non-standard property names
- X files with bare text instead of wikilinks in properties

### Orphan Notes
- X notes with no incoming links and no categories

### Stats
- Total notes: X
- By location: Root (X), Clippings (X), References (X), Daily (X)
- By category: Essays (X), Clippings (X), Books (X), ...
- Inbox queue: X items
```

Do NOT auto-fix in audit mode. Present the report and ask which issues to address.

## Backlink Rules

When adding backlinks to note body text:
- **First occurrence only** per file
- **Skip YAML frontmatter** (between `---` markers)
- **Don't double-link** terms already in `[[wikilinks]]`
- **Whole word matching** only
- People with first names alone: `[[Full Name|First Name]]`

## Execution: Obsidian CLI (Preferred)

When Obsidian is running, **always prefer CLI commands** over direct file manipulation:

### File Moves (CRITICAL)
**Never use `mv`** — it breaks backlinks. Use the CLI `move` command which updates all wikilinks automatically:
```bash
obsidian vault=Core move file="Note Name" to="Clippings/Articles/Note Name"
```

### Property Changes
Use `property:set` and `property:remove` to edit frontmatter **without reading the file** (saves tokens):
```bash
# Remove [[Inbox]] category
obsidian vault=Core property:remove name=categories file="Note Name"
obsidian vault=Core property:set name=categories value="[[Clippings]]" type=list file="Note Name"

# Add topics
obsidian vault=Core property:set name=topics value="[[AI]]" type=list file="Note Name"
```

### Audit Mode Shortcuts
Use CLI for instant vault-wide analysis instead of grep-based scanning:
```bash
obsidian vault=Core orphans total          # Notes with no incoming links
obsidian vault=Core deadends total         # Notes with no outgoing links
obsidian vault=Core unresolved total       # Broken wikilinks
obsidian vault=Core properties all sort=count counts  # Property usage audit
```

### Fallback
If Obsidian is not running, use the Read/Edit/Write tools directly. For file moves without Obsidian, use `mv` **but flag that backlinks need manual repair**.

## Safety

- Never delete files (move or archive instead)
- Never modify body content beyond adding wikilinks
- Always show changes before executing
- For file moves, use CLI `move` (auto-updates all backlinks)
- Log all changes made for undo reference

## Batch Processing

For folders with >10 files, dispatch parallel Sonnet agents grouped by subfolder or content type. Each agent gets:
- List of files to process
- The filing rules above
- Instructions to present changes for confirmation

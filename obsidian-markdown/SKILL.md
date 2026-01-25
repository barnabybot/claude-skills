---
name: obsidian-markdown
description: Create and edit Obsidian Flavored Markdown with wikilinks, embeds, callouts, properties, and other Obsidian-specific syntax. Use when working with .md files in Obsidian, or when the user mentions wikilinks, callouts, frontmatter, tags, embeds, or Obsidian notes.
---

# Obsidian Flavored Markdown

Obsidian extends CommonMark and GFM with wikilinks, callouts, embeds, and properties. This skill covers **Obsidian-specific syntax only** - standard markdown (headings, lists, tables, code blocks, LaTeX, Mermaid) works as expected.

## Wikilinks

```markdown
[[Note Name]]                    Basic link
[[Note Name|Display Text]]       Custom display text
[[Note Name#Heading]]            Link to heading
[[Note Name#^block-id]]          Link to block
[[#Heading in same note]]        Same-note heading link
```

**Block IDs**: Add `^block-id` at end of paragraph. For lists/quotes, add on separate line after.

## Embeds

```markdown
![[Note Name]]                   Embed note
![[Note Name#Heading]]           Embed section
![[image.png]]                   Embed image
![[image.png|300]]               Image with width
![[document.pdf#page=3]]         PDF page
![[audio.mp3]]                   Audio file
```

## Callouts

```markdown
> [!note]
> Basic callout content.

> [!warning] Custom Title
> Callout with title.

> [!tip]- Collapsed by default
> Foldable callout.

> [!info]+ Expanded by default
> Starts open, can collapse.
```

**Types**: `note`, `abstract`/`summary`/`tldr`, `info`, `todo`, `tip`/`hint`/`important`, `success`/`check`/`done`, `question`/`help`/`faq`, `warning`/`caution`, `failure`/`fail`, `danger`/`error`, `bug`, `example`, `quote`/`cite`

## Comments

```markdown
This is visible %%but this is hidden%% text.

%%
Multi-line hidden comment block.
%%
```

## Properties (Frontmatter)

```yaml
---
title: Note Title
date: 2024-01-15
tags:
  - project
  - active
aliases:
  - Alternative Name
cssclasses:
  - custom-class
status: in-progress
rating: 5
---
```

**Property types**: Text, Number, Checkbox (`true`/`false`), Date (`YYYY-MM-DD`), DateTime (`YYYY-MM-DDTHH:MM:SS`), List, Links (`"[[Note]]"`)

**Template dates**: Use `{{date}}` (core Templates) or `<% tp.date.now("YYYY-MM-DD") %>` (Templater), never hardcoded dates.

## Tags

```markdown
#tag #nested/tag #tag-with-dashes

# In frontmatter:
tags:
  - tag1
  - nested/tag2
```

Tags can contain letters, numbers (not first), underscores, hyphens, forward slashes.

---

## Vault Organization (Kepano Method)

### Folder Structure

| Location | Content | Author |
|----------|---------|--------|
| **Root** | Daily notes, personal notes | You |
| **References** | Notes ABOUT external things | You |
| **Clippings** | Content written by others | Others |
| **Attachments** | Images, PDFs, media | N/A |
| **Daily** | Daily notes (`YYYY-MM-DD.md`) | You |

**The test**: Who wrote most of the words? You → Root/References. Someone else → Clippings.

### Properties Conventions

- **Names**: lowercase plural (`categories`, `topics`, `authors`)
- **Values**: Title Case with wikilinks (`"[[Career]]"`, `"[[Writing]]"`)
- **Category**: Has a template or Base → use `categories` property
- **Topic**: Thematic grouping without template → use `topics` property

### Rating Scale (1-7)

| Rating | Meaning |
|--------|---------|
| 7 | Perfect, life-changing |
| 6 | Excellent |
| 5 | Good |
| 4 | Passable |
| 3 | Bad |
| 2 | Atrocious |
| 1 | Harmful |

---

## Meeting Notes Format

```yaml
---
categories:
  - "[[Meetings]]"
date: 2024-01-15
time: "10:00"
attendees:
  - "[[Person One]]"
  - "External Person"
topics:
  - "[[Topic One]]"
---
```

**Sections**: About Meeting, Meeting Outline, Overview, Action Items (table), Decisions

**Attendees**: Wikilinks for vault entries, plain text for external people.

---

## Presentation Format

```markdown
# SLIDE 1: Title

Content here.

### Speaker Notes — Slide 1

Notes for presenter.

---

# SLIDE 2: Next Slide
```

Use `# SLIDE N: Title` for parsing, `### Speaker Notes — Slide N` for notes, `---` between slides.

---

## Batch Operations

### Wikilink Rules
- First occurrence only per file (Kepano method)
- Skip YAML frontmatter
- Don't double-link existing wikilinks
- Whole word matching only
- Use display syntax for first names: `[[Full Name|First]]`

### Vault Maintenance
- **Find incoming links** before moving/deleting files
- **Prefer archiving** over deletion
- **Update cross-references** after renaming

---

## Vault-Specific Configuration

**Always check for vault-level CLAUDE.md** which may define:
- Custom taxonomy and allowed values
- Valid link targets from vault bases
- Naming conventions
- Project-specific terms

Vault CLAUDE.md takes precedence over general conventions.

---

## References

- [Obsidian syntax](https://help.obsidian.md/syntax)
- [Internal links](https://help.obsidian.md/links)
- [Embeds](https://help.obsidian.md/embeds)
- [Callouts](https://help.obsidian.md/callouts)
- [Properties](https://help.obsidian.md/properties)

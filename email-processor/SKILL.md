---
name: email-processor
description: Process raw emails into structured Obsidian vault documents with YAML frontmatter, wikilinks, and date-prefixed filenames. Use when the user wants to add an email to their vault, process email content, or batch rename emails with dates.
---

# Email Processor Skill

Process raw emails into well-structured Obsidian vault documents with proper metadata, backlinks, and organization.

## When to Use

- User says "process this email", "add email to vault"
- Raw email content needs to be converted to Obsidian format
- Emails need renaming with date prefixes
- Batch processing of email folder

## Workflow

### 1. Extract Metadata

Parse email headers to extract:

| Field | Source |
|-------|--------|
| `date` | "Sent:" line (convert to YYYY-MM-DD) |
| `from` | "From:" line |
| `to` | "To:" line (may be multiple) |
| `cc` | "Cc:" line (may be multiple) |
| `subject` | "Subject:" line |

### 2. Generate YAML Frontmatter

```yaml
---
categories:
  - "[[Emails]]"
type: "[[Email]]"
date: YYYY-MM-DD
subject: "Email subject line"
from: "[[Person Name]]"
to:
  - "[[Person One]]"
  - "[[Person Two]]"
cc:
  - "[[Person Three]]"
topics:
  - "[[Topic One]]"
  - "[[Topic Two]]"
workstream: "[[Workstream Name]]"
synergy_buckets:  # if applicable
  - "[[Bucket Reference]]"
priority: High|Medium|Low
action_required: true|false
created: YYYY-MM-DD
---
```

**Rules:**
- People with vault entries → wikilinks
- External people (no vault entry) → plain text
- Topics derived from email content
- `action_required: true` if email contains action items

### 3. Add Wikilinks Throughout Content

**First occurrence only** (Kepano method):
- People names → `[[Full Name|First Name]]` for short references
- Projects/concepts → `[[Project Name]]`
- Business units → `[[Unit Name]]`
- Dates → `[[YYYY-MM-DD]]` for daily note linking

**Skip:**
- Content inside YAML frontmatter (already linked)
- Content inside code blocks
- Already-linked terms

### 4. Structure Content

Transform raw email into structured markdown:

```markdown
# Email Subject as Title

## Summary

1-3 sentence executive summary of the email's key point.

## Key Points

### Subsection for Major Topic

- Bullet points extracting key information
- Include specific quotes using > blockquote format
- Tables for structured data

## Action Items

| Action | Owner | Due |
|--------|-------|-----|
| Action description | [[Person]] | Date/ASAP |

## Implications

What this means for ongoing work (if significant email).

## Related

- [[Related Document 1]]
- [[Related Meeting]]
```

### 5. File Naming Convention

**Format:** `YYYY-MM-DD Email Subject or Description.md`

**Rules:**
- Date from email's "Sent:" field
- Subject cleaned of special characters
- Keep concise but descriptive
- Capitalize appropriately

**Examples:**
- `2026-01-17 Omar Malik - Go-forward support to Assurance.md`
- `2026-01-16 Balance Sheet Email.md`
- `2026-01-15 Card Schemes Email.md`

### 6. File Placement

Move processed email to the vault's Emails folder:
- Default: `[Vault]/Emails/`
- Check vault CLAUDE.md for custom location

## Batch Operations

### Rename Existing Emails with Dates

When emails exist without date prefixes:

1. Read each email file
2. Extract date from YAML frontmatter (`date:` field)
3. Rename file with date prefix
4. Preserve the rest of the filename

```bash
# Pattern: "Old Name.md" → "YYYY-MM-DD Old Name.md"
mv "Balance sheet email.md" "2026-01-16 Balance Sheet Email.md"
```

### Process Multiple Emails

For batch processing:
1. Dispatch parallel Sonnet agents grouped by date or topic
2. Each agent processes 3-5 emails
3. Maintain consistent formatting across all files

## Quality Checks

After processing:
- [ ] YAML frontmatter valid (no syntax errors)
- [ ] All people with vault entries are wikilinked
- [ ] Date prefix matches YAML date field
- [ ] File in correct folder
- [ ] Summary accurately reflects email content
- [ ] Action items captured if present

## Example: Raw Email → Processed

**Input (raw):**
```
From: Omar MALIK <omar.malik@hsbc.com.hk>
Sent: Saturday, January 17, 2026 12:08 PM
To: Kris Pearson <kris.pearson@hsbc.com.hk>
Subject: Go-forward support

Hi Kris,

Thanks for the support. FMG was a watershed moment...
```

**Output (processed):**
```yaml
---
categories:
  - "[[Emails]]"
type: "[[Email]]"
date: 2026-01-17
subject: "Go-forward support"
from: "[[Omar Malik]]"
to:
  - "[[Kris Pearson]]"
topics:
  - "[[FMG]]"
priority: High
action_required: true
---

# Go-forward Support

## Summary

[[Omar Malik]] sent update following [[FMG]] meeting...
```

**Filename:** `2026-01-17 Omar Malik - Go-forward support.md`

## Vault-Specific Configuration

Always check the vault's CLAUDE.md for:
- Custom email folder location
- Specific YAML properties required
- Topic/category taxonomy
- People directory for wikilink validation

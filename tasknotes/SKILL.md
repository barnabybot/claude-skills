---
name: tasknotes
description: Query and manage tasks in Obsidian vault. Use when user asks about tasks, what's overdue, what to work on, due today, task status, or wants to see their todo items. Works with both TaskNotes plugin tasks (frontmatter-based) and markdown checkbox tasks (`- [ ]`).
---

# TaskNotes

Query tasks from Obsidian vault - both TaskNotes plugin tasks and markdown checkboxes.

## Quick Reference

Run the query script:
```bash
python3 scripts/query_tasks.py "<vault_path>" --filter <type> --format <format>
```

**Filters**:
- `actionable` (default): Open/in-progress tasks scheduled for today or earlier
- `overdue`: Tasks past their due date
- `today`: Tasks due or scheduled today
- `high-priority`: High priority tasks only
- `all`: All tasks including completed

**Formats**: `summary` (default), `detailed` (includes file paths), `json`

## Common Queries

| User asks | Command |
|-----------|---------|
| "What's overdue?" | `--filter overdue` |
| "What can I work on?" | `--filter actionable` |
| "What's due today?" | `--filter today` |
| "What's high priority?" | `--filter high-priority` |
| "Show all my tasks" | `--filter all --format detailed` |

## Task Sources

**TaskNotes Plugin** (`TaskNotes/Tasks/*.md`):
- Frontmatter: `status`, `priority`, `due`, `scheduled`, `projects`, `contexts`
- Status: `open`, `in-progress`, `done`
- Priority: `high`, `normal`, `low`

**Markdown Checkboxes** (vault-wide):
- `- [ ]` open, `- [x]` done
- Inline due dates: `due: 2026-01-31` or `by 2026-01-31`
- Priority markers: `!!`, `🔴` (high), `⚠️`, `🟡` (normal)

## Output Example

```
🔴⬜ Finish quarterly report ⚠️ OVERDUE (due 2026-01-28)
⬜ Review pull requests 📅 TODAY
🔄 Write documentation (due 2026-02-01)
⬜ Update dependencies
```

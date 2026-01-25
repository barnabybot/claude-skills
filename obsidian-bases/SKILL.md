---
name: obsidian-bases
description: Create and edit Obsidian Bases (.base files) with views, filters, formulas, and summaries. Use when working with .base files, creating database-like views of notes, or when the user mentions Bases, table views, card views, filters, or formulas in Obsidian.
---

# Obsidian Bases

Bases are YAML files (`.base`) that define dynamic views of notes. They support filters, formulas, multiple view types, and summaries.

## Schema Overview

```yaml
filters:                    # Global filters for all views
  and: []                   # All conditions must match
  or: []                    # Any condition matches
  not: []                   # Exclude matches

formulas:                   # Computed properties
  name: 'expression'

properties:                 # Display name configuration
  property_name:
    displayName: "Name"

summaries:                  # Custom summary formulas
  name: 'values.mean().round(3)'

views:
  - type: table | cards | list | map
    name: "View Name"
    limit: 10               # Optional result limit
    filters: {}             # View-specific filters
    order:                  # Properties to display
      - file.name
      - property_name
    groupBy:
      property: name
      direction: ASC | DESC
    summaries:
      property: Average
```

## Filters

```yaml
# Single filter
filters: 'status == "done"'

# AND/OR/NOT
filters:
  and:
    - 'status == "done"'
    - 'priority > 3'

filters:
  or:
    - file.hasTag("book")
    - file.hasTag("article")

filters:
  not:
    - file.hasTag("archived")

# Nested
filters:
  or:
    - file.hasTag("tag")
    - and:
        - file.hasTag("book")
        - file.inFolder("Reading")
```

**Operators**: `==`, `!=`, `>`, `<`, `>=`, `<=`, `&&`, `||`, `!`

## Properties

### Three Types
1. **Note properties**: From frontmatter - `author` or `note.author`
2. **File properties**: Metadata - `file.name`, `file.mtime`
3. **Formula properties**: Computed - `formula.my_formula`

### File Properties

| Property | Description |
|----------|-------------|
| `file.name` | Filename |
| `file.basename` | Name without extension |
| `file.path` | Full path |
| `file.folder` | Parent folder |
| `file.ext` | Extension |
| `file.size` | Size in bytes |
| `file.ctime` | Created time |
| `file.mtime` | Modified time |
| `file.tags` | All tags |
| `file.links` | Internal links |
| `file.backlinks` | Files linking here |

### The `this` Keyword

- Main content: refers to the base file
- When embedded: refers to the embedding file
- `this.file.name` returns basename without `.md`

## Formulas

```yaml
formulas:
  total: "price * quantity"
  status_icon: 'if(done, "✅", "⏳")'
  days_old: '((now() - file.ctime) / 86400000).round(0)'
  created: 'file.ctime.format("YYYY-MM-DD")'
  stars: '"⭐".repeat(rating)'
```

### Key Functions

**Global**: `date()`, `now()`, `today()`, `if(cond, true, false)`, `min()`, `max()`, `link()`, `list()`, `file()`, `image()`, `icon()`

**Date**: `.format("YYYY-MM-DD")`, `.relative()`, `.date()`, `.year`, `.month`, `.day`

**String**: `.contains()`, `.startsWith()`, `.endsWith()`, `.isEmpty()`, `.lower()`, `.split()`, `.length`

**List**: `.contains()`, `.filter(expr)`, `.map(expr)`, `.join()`, `.sort()`, `.unique()`, `.length`

**File**: `.hasTag()`, `.hasLink()`, `.hasProperty()`, `.inFolder()`, `.asLink()`

### Date Arithmetic

```yaml
"date + \"1M\""           # Add 1 month
"now() - file.ctime"      # Milliseconds since creation
"today() + \"7d\""        # A week from today
```

Duration units: `y`, `M`, `d`, `w`, `h`, `m`, `s`

## View Types

### Table
```yaml
views:
  - type: table
    name: "My Table"
    order: [file.name, status, due_date]
    summaries:
      price: Sum
```

### Cards
```yaml
views:
  - type: cards
    name: "Gallery"
    image: cover              # Property with image path/URL
    cardSize: 150             # Width in pixels
    imageFit: contain         # contain | cover | fill
    imageAspectRatio: 1.4     # Height/width (1.4 for books)
    order: [file.name, author]
```

### List
```yaml
views:
  - type: list
    order: [file.name, status]
```

### Map
Requires lat/lng properties and Maps plugin.

## Default Summaries

**Number**: `Average`, `Min`, `Max`, `Sum`, `Range`, `Median`, `Stddev`
**Date**: `Earliest`, `Latest`, `Range`
**Boolean**: `Checked`, `Unchecked`
**Any**: `Empty`, `Filled`, `Unique`

## Example: Reading List

```yaml
filters:
  or:
    - file.hasTag("book")
    - file.hasTag("article")

formulas:
  stars: '"⭐".repeat(rating)'
  status_icon: 'if(status == "reading", "📖", if(status == "done", "✅", "📚"))'

views:
  - type: cards
    name: "Library"
    image: cover
    cardSize: 150
    imageFit: contain
    imageAspectRatio: 1.4
    order: [file.name, author, formula.stars]

  - type: table
    name: "All Books"
    order: [file.name, author, genre, rating, status]
```

## Embedding

```markdown
![[MyBase.base]]
![[MyBase.base#View Name]]
```

## Common Pitfalls

### Use `link()` for Link Properties
```yaml
# ✅ CORRECT
filters:
  and:
    - type.contains(link("Books"))

# ❌ WRONG - strings don't match link-typed properties
filters:
  and:
    - type.containsAny("[[Books]]")
```

### Bare Property Names in Cards
```yaml
# ✅ CORRECT
image: cover

# ❌ WRONG
image: note.cover
```

### Bare Property Names in Order Arrays
```yaml
# ✅ CORRECT
order: [file.name, author, genre]

# ❌ WRONG
order: [file.name, note.author, note.genre]
```

### Global vs View Filters
Global filters exclude from ALL views. Use view-level filters for different audiences:

```yaml
# View-level filters allow different subsets per view
views:
  - name: "Alice's Books"
    filters:
      or:
        - readers.isEmpty()
        - readers.containsAny("alice")

  - name: "Bob's Books"
    filters:
      and:
        - readers.containsAny("bob")
```

## References

- [Bases Syntax](https://help.obsidian.md/bases/syntax)
- [Functions](https://help.obsidian.md/bases/functions)

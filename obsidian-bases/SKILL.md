---
name: obsidian-bases
description: Create and edit Obsidian Bases (.base files) with views, filters, formulas, and summaries. Use when working with .base files, creating database-like views of notes, or when the user mentions Bases, table views, card views, filters, or formulas in Obsidian.
---

# Obsidian Bases Skill

This skill enables Claude Code to create and edit valid Obsidian Bases (`.base` files) including views, filters, formulas, and all related configurations.

## Overview

Obsidian Bases are YAML-based files that define dynamic views of notes in an Obsidian vault. A Base file can contain multiple views, global filters, formulas, property configurations, and custom summaries.

## File Format

Base files use the `.base` extension and contain valid YAML. They can also be embedded in Markdown code blocks.

## Complete Schema

```yaml
# Global filters apply to ALL views in the base
filters:
  # Can be a single filter string
  # OR a recursive filter object with and/or/not
  and: []
  or: []
  not: []

# Define formula properties that can be used across all views
formulas:
  formula_name: 'expression'

# Configure display names and settings for properties
properties:
  property_name:
    displayName: "Display Name"
  formula.formula_name:
    displayName: "Formula Display Name"
  file.ext:
    displayName: "Extension"

# Define custom summary formulas
summaries:
  custom_summary_name: 'values.mean().round(3)'

# Define one or more views
views:
  - type: table | cards | list | map
    name: "View Name"
    limit: 10                    # Optional: limit results
    groupBy:                     # Optional: group results
      property: property_name
      direction: ASC | DESC
    filters:                     # View-specific filters
      and: []
    order:                       # Properties to display in order
      - file.name
      - property_name
      - formula.formula_name
    summaries:                   # Map properties to summary formulas
      property_name: Average
```

## Filter Syntax

Filters narrow down results. They can be applied globally or per-view.

### Filter Structure

```yaml
# Single filter
filters: 'status == "done"'

# AND - all conditions must be true
filters:
  and:
    - 'status == "done"'
    - 'priority > 3'

# OR - any condition can be true
filters:
  or:
    - 'file.hasTag("book")'
    - 'file.hasTag("article")'

# NOT - exclude matching items
filters:
  not:
    - 'file.hasTag("archived")'

# Nested filters
filters:
  or:
    - file.hasTag("tag")
    - and:
        - file.hasTag("book")
        - file.hasLink("Textbook")
    - not:
        - file.hasTag("book")
        - file.inFolder("Required Reading")
```

### Filter Operators

| Operator | Description |
|----------|-------------|
| `==` | equals |
| `!=` | not equal |
| `>` | greater than |
| `<` | less than |
| `>=` | greater than or equal |
| `<=` | less than or equal |
| `&&` | logical and |
| `\|\|` | logical or |
| <code>!</code> | logical not |

## Properties

### Three Types of Properties

1. **Note properties** - From frontmatter: `note.author` or just `author`
2. **File properties** - File metadata: `file.name`, `file.mtime`, etc.
3. **Formula properties** - Computed values: `formula.my_formula`

### File Properties Reference

| Property | Type | Description |
|----------|------|-------------|
| `file.name` | String | File name |
| `file.basename` | String | File name without extension |
| `file.path` | String | Full path to file |
| `file.folder` | String | Parent folder path |
| `file.ext` | String | File extension |
| `file.size` | Number | File size in bytes |
| `file.ctime` | Date | Created time |
| `file.mtime` | Date | Modified time |
| `file.tags` | List | All tags in file |
| `file.links` | List | Internal links in file |
| `file.backlinks` | List | Files linking to this file |
| `file.embeds` | List | Embeds in the note |
| `file.properties` | Object | All frontmatter properties |

### The `this` Keyword

- In main content area: refers to the base file itself
- When embedded: refers to the embedding file
- In sidebar: refers to the active file in main content

**Important:** When embedded, `this.file.name` returns the basename without the `.md` extension. For a file `Daily/2026-01-16.md`, `this.file.name` returns `2026-01-16`.

## Formula Syntax

Formulas compute values from properties. Defined in the `formulas` section.

```yaml
formulas:
  # Simple arithmetic
  total: "price * quantity"
  
  # Conditional logic
  status_icon: 'if(done, "✅", "⏳")'
  
  # String formatting
  formatted_price: 'if(price, price.toFixed(2) + " dollars")'
  
  # Date formatting
  created: 'file.ctime.format("YYYY-MM-DD")'
  
  # Complex expressions
  days_old: '((now() - file.ctime) / 86400000).round(0)'
```

## Functions Reference

### Global Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `date()` | `date(string): date` | Parse string to date. Format: `YYYY-MM-DD HH:mm:ss` |
| `duration()` | `duration(string): duration` | Parse duration string |
| `now()` | `now(): date` | Current date and time |
| `today()` | `today(): date` | Current date (time = 00:00:00) |
| `if()` | `if(condition, trueResult, falseResult?)` | Conditional |
| `min()` | `min(n1, n2, ...): number` | Smallest number |
| `max()` | `max(n1, n2, ...): number` | Largest number |
| `number()` | `number(any): number` | Convert to number |
| `link()` | `link(path, display?): Link` | Create a link |
| `list()` | `list(element): List` | Wrap in list if not already |
| `file()` | `file(path): file` | Get file object |
| `image()` | `image(path): image` | Create image for rendering |
| `icon()` | `icon(name): icon` | Lucide icon by name |
| `html()` | `html(string): html` | Render as HTML |
| `escapeHTML()` | `escapeHTML(string): string` | Escape HTML characters |

### Any Type Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `isTruthy()` | `any.isTruthy(): boolean` | Coerce to boolean |
| `isType()` | `any.isType(type): boolean` | Check type |
| `toString()` | `any.toString(): string` | Convert to string |

### Date Functions & Fields

**Fields:** `date.year`, `date.month`, `date.day`, `date.hour`, `date.minute`, `date.second`, `date.millisecond`

| Function | Signature | Description |
|----------|-----------|-------------|
| `date()` | `date.date(): date` | Remove time portion |
| `format()` | `date.format(string): string` | Format with Moment.js pattern |
| `time()` | `date.time(): string` | Get time as string |
| `relative()` | `date.relative(): string` | Human-readable relative time |
| `isEmpty()` | `date.isEmpty(): boolean` | Always false for dates |

### Date Arithmetic

```yaml
# Duration units: y/year/years, M/month/months, d/day/days, 
#                 w/week/weeks, h/hour/hours, m/minute/minutes, s/second/seconds

# Add/subtract durations
"date + \"1M\""           # Add 1 month
"date - \"2h\""           # Subtract 2 hours
"now() + \"1 day\""       # Tomorrow
"today() + \"7d\""        # A week from today

# Subtract dates for millisecond difference
"now() - file.ctime"

# Complex duration arithmetic
"now() + (duration('1d') * 2)"
```

### String Functions

**Field:** `string.length`

| Function | Signature | Description |
|----------|-----------|-------------|
| `contains()` | `string.contains(value): boolean` | Check substring |
| `containsAll()` | `string.containsAll(...values): boolean` | All substrings present |
| `containsAny()` | `string.containsAny(...values): boolean` | Any substring present |
| `startsWith()` | `string.startsWith(query): boolean` | Starts with query |
| `endsWith()` | `string.endsWith(query): boolean` | Ends with query |
| `isEmpty()` | `string.isEmpty(): boolean` | Empty or not present |
| `lower()` | `string.lower(): string` | To lowercase |
| `title()` | `string.title(): string` | To Title Case |
| `trim()` | `string.trim(): string` | Remove whitespace |
| `replace()` | `string.replace(pattern, replacement): string` | Replace pattern |
| `repeat()` | `string.repeat(count): string` | Repeat string |
| `reverse()` | `string.reverse(): string` | Reverse string |
| `slice()` | `string.slice(start, end?): string` | Substring |
| `split()` | `string.split(separator, n?): list` | Split to list |

### Number Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `abs()` | `number.abs(): number` | Absolute value |
| `ceil()` | `number.ceil(): number` | Round up |
| `floor()` | `number.floor(): number` | Round down |
| `round()` | `number.round(digits?): number` | Round to digits |
| `toFixed()` | `number.toFixed(precision): string` | Fixed-point notation |
| `isEmpty()` | `number.isEmpty(): boolean` | Not present |

### List Functions

**Field:** `list.length`

| Function | Signature | Description |
|----------|-----------|-------------|
| `contains()` | `list.contains(value): boolean` | Element exists |
| `containsAll()` | `list.containsAll(...values): boolean` | All elements exist |
| `containsAny()` | `list.containsAny(...values): boolean` | Any element exists |
| `filter()` | `list.filter(expression): list` | Filter by condition (uses `value`, `index`) |
| `map()` | `list.map(expression): list` | Transform elements (uses `value`, `index`) |
| `reduce()` | `list.reduce(expression, initial): any` | Reduce to single value (uses `value`, `index`, `acc`) |
| `flat()` | `list.flat(): list` | Flatten nested lists |
| `join()` | `list.join(separator): string` | Join to string |
| `reverse()` | `list.reverse(): list` | Reverse order |
| `slice()` | `list.slice(start, end?): list` | Sublist |
| `sort()` | `list.sort(): list` | Sort ascending |
| `unique()` | `list.unique(): list` | Remove duplicates |
| `isEmpty()` | `list.isEmpty(): boolean` | No elements |

### File Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `asLink()` | `file.asLink(display?): Link` | Convert to link |
| `hasLink()` | `file.hasLink(otherFile): boolean` | Has link to file |
| `hasTag()` | `file.hasTag(...tags): boolean` | Has any of the tags |
| `hasProperty()` | `file.hasProperty(name): boolean` | Has property |
| `inFolder()` | `file.inFolder(folder): boolean` | In folder or subfolder |

### Link Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `asFile()` | `link.asFile(): file` | Get file object |
| `linksTo()` | `link.linksTo(file): boolean` | Links to file |

### Object Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `isEmpty()` | `object.isEmpty(): boolean` | No properties |
| `keys()` | `object.keys(): list` | List of keys |
| `values()` | `object.values(): list` | List of values |

### Regular Expression Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `matches()` | `regexp.matches(string): boolean` | Test if matches |

## View Types

### Table View

```yaml
views:
  - type: table
    name: "My Table"
    order:
      - file.name
      - status
      - due_date
    summaries:
      price: Sum
      count: Average
```

### Cards View

Cards view displays notes as visual cards, ideal for content with images like books, recipes, or media.

```yaml
views:
  - type: cards
    name: "Gallery"
    image: cover              # Property containing image URL or path
    cardSize: 150             # Card width in pixels (default: 200)
    imageFit: contain         # How image fits: contain | cover | fill
    imageAspectRatio: 1.4     # Height/width ratio (1.4 = portrait/book, 0.75 = landscape)
    order:
      - file.name
      - author
      - formula.stars
```

**Card View Options:**

| Option | Type | Description |
|--------|------|-------------|
| `image` | string | Property name containing image URL or vault path |
| `cardSize` | number | Card width in pixels (default: 200) |
| `imageFit` | string | `contain` (show full image), `cover` (fill card, crop), `fill` (stretch) |
| `imageAspectRatio` | number | Height = width × ratio. Use 1.4 for books, 0.75 for landscape, 1 for square |

**Image Property Sources:**
- URL: `cover: "https://example.com/image.jpg"`
- Vault path: `cover: "Attachments/book-covers/mybook.jpg"`
- Wikilink: `cover: "[[Attachments/cover.png]]"`

**Best Practices for Cards:**
- Place card views first when content has images (makes them the default view)
- Use `imageFit: contain` for book covers to show full artwork
- Use `imageFit: cover` for photos/thumbnails where cropping is acceptable
- Aspect ratio 1.4 works well for book covers, 0.5625 (16:9) for video thumbnails

### List View

```yaml
views:
  - type: list
    name: "Simple List"
    order:
      - file.name
      - status
```

### Map View

Requires the **Maps community plugin** to be installed and enabled.

```yaml
views:
  - type: map
    name: "Locations"
    coordinates: coordinates       # Property containing [lat, lng] array
    markerColor: formula.color     # Optional: property/formula for marker color
    markerIcon: coffee             # Optional: Lucide icon name
    defaultZoom: 10                # Optional: initial zoom level
    order:
      - file.name
      - rating
```

**Map View Options:**

| Option | Type | Description |
|--------|------|-------------|
| `coordinates` | string | Property name containing coordinates (array `[lat, lng]` or string `"lat, lng"`) |
| `markerColor` | string | Property or formula returning color name (green, gold, red, gray, etc.) |
| `markerIcon` | string | Lucide icon name for markers |
| `defaultZoom` | number | Initial zoom level (higher = more zoomed in) |

**Coordinates Format:**
- Array: `coordinates: [-8.263, 115.354]`
- String: `coordinates: "-8.263, 115.354"`

**Example with dynamic marker colors:**
```yaml
formulas:
  markerColor: 'if(rating >= 4, "green", if(rating >= 2, "gold", "red"))'

views:
  - type: map
    name: "Rated Locations"
    coordinates: coordinates
    markerColor: formula.markerColor
    markerIcon: star
```

## Default Summary Formulas

| Name | Input Type | Description |
|------|------------|-------------|
| `Average` | Number | Mathematical mean |
| `Min` | Number | Smallest number |
| `Max` | Number | Largest number |
| `Sum` | Number | Sum of all numbers |
| `Range` | Number | Max - Min |
| `Median` | Number | Mathematical median |
| `Stddev` | Number | Standard deviation |
| `Earliest` | Date | Earliest date |
| `Latest` | Date | Latest date |
| `Range` | Date | Latest - Earliest |
| `Checked` | Boolean | Count of true values |
| `Unchecked` | Boolean | Count of false values |
| `Empty` | Any | Count of empty values |
| `Filled` | Any | Count of non-empty values |
| `Unique` | Any | Count of unique values |

## Complete Examples

### Task Tracker Base

```yaml
filters:
  and:
    - file.hasTag("task")
    - 'file.ext == "md"'

formulas:
  days_until_due: 'if(due, ((date(due) - today()) / 86400000).round(0), "")'
  is_overdue: 'if(due, date(due) < today() && status != "done", false)'
  priority_label: 'if(priority == 1, "🔴 High", if(priority == 2, "🟡 Medium", "🟢 Low"))'

properties:
  status:
    displayName: Status
  formula.days_until_due:
    displayName: "Days Until Due"
  formula.priority_label:
    displayName: Priority

views:
  - type: table
    name: "Active Tasks"
    filters:
      and:
        - 'status != "done"'
    order:
      - file.name
      - status
      - formula.priority_label
      - due
      - formula.days_until_due
    groupBy:
      property: status
      direction: ASC
    summaries:
      formula.days_until_due: Average

  - type: table
    name: "Completed"
    filters:
      and:
        - 'status == "done"'
    order:
      - file.name
      - completed_date
```

### Reading List Base (Books)

```yaml
filters:
  or:
    - file.hasTag("book")
    - file.hasTag("article")

formulas:
  stars: '"⭐".repeat(rating)'
  reading_time: 'if(pages, (pages * 2).toString() + " min", "")'
  status_icon: 'if(status == "reading", "📖", if(status == "done", "✅", "📚"))'

properties:
  author:
    displayName: Author
  formula.stars:
    displayName: Rating
  formula.reading_time:
    displayName: "Est. Time"

views:
  # Card view FIRST for visual library browsing
  - type: cards
    name: "Library"
    image: cover                # Property with cover image URL
    cardSize: 150
    imageFit: contain           # Show full book cover
    imageAspectRatio: 1.4       # Portrait ratio for books
    order:
      - file.name
      - author
      - formula.stars
    filters:
      not:
        - 'status == "dropped"'

  - type: table
    name: "All Books"
    order:
      - file.name
      - author
      - genre
      - rating
      - status

  - type: cards
    name: "Anti-Library"
    image: cover
    cardSize: 150
    imageFit: contain
    imageAspectRatio: 1.4
    filters:
      and:
        - 'rating.isEmpty()'
    order:
      - file.name
      - author

  - type: cards
    name: "Favorites"
    image: cover
    cardSize: 150
    imageFit: contain
    imageAspectRatio: 1.4
    filters:
      and:
        - 'rating >= 5'
    order:
      - file.name
      - author
      - formula.stars
```

### Project Notes Base

```yaml
filters:
  and:
    - file.inFolder("Projects")
    - 'file.ext == "md"'

formulas:
  last_updated: 'file.mtime.relative()'
  link_count: 'file.links.length'
  
summaries:
  avgLinks: 'values.filter(value.isType("number")).mean().round(1)'

properties:
  formula.last_updated:
    displayName: "Updated"
  formula.link_count:
    displayName: "Links"

views:
  - type: table
    name: "All Projects"
    order:
      - file.name
      - status
      - formula.last_updated
      - formula.link_count
    summaries:
      formula.link_count: avgLinks
    groupBy:
      property: status
      direction: ASC

  - type: list
    name: "Quick List"
    order:
      - file.name
      - status
```

### Daily Notes Index

```yaml
filters:
  and:
    - file.inFolder("Daily Notes")
    - '/^\d{4}-\d{2}-\d{2}$/.matches(file.basename)'

formulas:
  word_estimate: '(file.size / 5).round(0)'
  day_of_week: 'date(file.basename).format("dddd")'

properties:
  formula.day_of_week:
    displayName: "Day"
  formula.word_estimate:
    displayName: "~Words"

views:
  - type: table
    name: "Recent Notes"
    limit: 30
    order:
      - file.name
      - formula.day_of_week
      - formula.word_estimate
      - file.mtime
```

### Daily.base (Embedded in Daily Notes)

For daily notes (Kepano method), create a base that shows notes linked to or created on a specific day. This base is embedded in each daily note via `![[Daily.base]]`.

```yaml
# Works when embedded in Daily/YYYY-MM-DD.md files
# this.file.name resolves to the date (e.g., "2026-01-16")
filters:
  or:
    - file.name.contains(this.file.name)           # Notes with date in filename
    - created.toString().contains(this.file.name)  # Notes created on this date
    - start.toString().contains(this.file.name)    # Events starting this date
    - end.toString().contains(this.file.name)      # Events ending this date
    - file.links.contains(this.file)               # Notes linking to this daily note

properties:
  file.name:
    displayName: Entry
  note.categories:
    displayName: Categories
  note.created:
    displayName: Created

views:
  - type: table
    name: Daily notes
    order:
      - file.name
      - created
      - categories
```

**Key points:**
- `this.file.name` returns the date portion (e.g., `2026-01-16`) when embedded
- `created.toString()` converts the frontmatter date to a string for matching
- Works with notes that have `created: YYYY-MM-DD` in frontmatter OR date-prefixed filenames
- The daily note template should just have `![[Daily.base]]` in the body

## Embedding Bases

Embed in Markdown files:

```markdown
![[MyBase.base]]

<!-- Specific view -->
![[MyBase.base#View Name]]
```

## YAML Quoting Rules

- Use single quotes for formulas containing double quotes: `'if(done, "Yes", "No")'`
- Use double quotes for simple strings: `"My View Name"`
- Escape nested quotes properly in complex expressions

## Common Patterns

### Filter by Tag
```yaml
filters:
  and:
    - file.hasTag("project")
```

### Filter by Folder
```yaml
filters:
  and:
    - file.inFolder("Notes")
```

### Filter by Date Range
```yaml
filters:
  and:
    - 'file.mtime > now() - "7d"'
```

### Filter by Property Value
```yaml
filters:
  and:
    - 'status == "active"'
    - 'priority >= 3'
```

### Combine Multiple Conditions
```yaml
filters:
  or:
    - and:
        - file.hasTag("important")
        - 'status != "done"'
    - and:
        - 'priority == 1'
        - 'due != ""'
```

## Common Pitfalls

### ❌ Cards View: `cover:` vs `image:`

The key for specifying the image property in cards view is `image:`, **NOT** `cover:`.

```yaml
# ✅ CORRECT - use image: key
views:
  - type: cards
    name: "Gallery"
    image: feature
    cardSize: 150

# ❌ WRONG - cover: is not a valid key
views:
  - type: cards
    name: "Gallery"
    cover: feature
```

### ❌ Map View: `location:` vs `coordinates:`

The key for specifying the coordinates property in map view is `coordinates:`, **NOT** `location:`.

```yaml
# ✅ CORRECT - use coordinates: key
views:
  - type: map
    name: "Map"
    coordinates: coordinates

# ❌ WRONG - location: is not a valid key (map will show nothing)
views:
  - type: map
    name: "Map"
    location: coordinates
```

### ❌ String vs Link Function

**NEVER** use string `"[[Note]]"` for link property checks. **ALWAYS** use the `link()` function.

```yaml
# ✅ CORRECT - use link() function
filters:
  and:
    - type.contains(link("Books"))
    - genre.containsAny(link("Fiction"))

# ❌ WRONG - string won't match link-typed properties
filters:
  and:
    - type.containsAny("[[Books]]")
    - genre.containsAny("[[Fiction]]")
```

### ❌ Image Property in Cards

Use the **bare property name** for `image:`, not `note.property`:

```yaml
# ✅ CORRECT
views:
  - type: cards
    image: feature
    image: cover

# ❌ WRONG
views:
  - type: cards
    image: note.feature
    image: note.cover
```

### ❌ Global vs View Filters

**Global filters exclude items from ALL views.** View-level filters can only narrow results further, never expand them.

For multi-audience bases (e.g., different readers, different statuses), use **view-level filters** instead of global exclusions:

```yaml
# ✅ CORRECT - view-level filtering for different audiences
filters:
  and:
    - type.contains(link("Books"))

views:
  - name: "My Books"
    filters:
      or:
        - readers.isEmpty()
        - readers.containsAny("alice")

  - name: "Bob's Books"
    filters:
      and:
        - readers.containsAny("bob")

# ❌ WRONG - global filter excludes bob's books from entire base
filters:
  and:
    - type.contains(link("Books"))
    - readers.containsAny("alice")  # Bob's books can't appear anywhere
```

### ❌ Property Names in Order Arrays

In `order:` arrays, use **bare property names** (not `note.` prefixed):

```yaml
# ✅ CORRECT
order:
  - file.name
  - author
  - genre
  - formula.stars

# ❌ WRONG
order:
  - file.name
  - note.author
  - note.genre
```

### ❌ Property Definition vs Actual Note Property

Ensure `properties:` definitions match what your notes actually use. If notes have `image:` but you define `note.feature:`, the base won't find your images.

```yaml
# If your notes have: image: "[[photo.jpg]]"

# ✅ CORRECT - matches note property name
properties:
  note.image:
    type: image
    displayName: Photo

# ❌ WRONG - defines different property than notes use
properties:
  note.feature:
    type: image
    displayName: Photo
```

### ❌ Case Sensitivity

Property names are case-sensitive. `Image` ≠ `image`.

```yaml
# If your notes have: image: "[[photo.jpg]]"

# ✅ CORRECT
image: image

# ❌ WRONG - capital I won't match
image: Image
```

## References

- [Bases Syntax](https://help.obsidian.md/bases/syntax)
- [Functions](https://help.obsidian.md/bases/functions)
- [Views](https://help.obsidian.md/bases/views)
- [Formulas](https://help.obsidian.md/formulas)


---
name: obsidian-base-builder
description: "Build optimal Obsidian Base (.base) configurations by analyzing note content and frontmatter. Use when creating a new Base for a folder of notes, optimizing existing Base views, or needing to determine which properties to display. Analyzes frontmatter schemas across notes to suggest views, filters, formulas, and property configurations."
---

# Obsidian Base Builder

Build optimal Obsidian Base configurations by analyzing note content and frontmatter.

## Workflow

### 1. Analyze Target Notes

First, examine the notes that the Base will query:

```
1. Read 3-5 representative notes from the target folder
2. Extract all frontmatter properties and their types
3. Identify common properties across notes
4. Note which properties have meaningful variance (good for filtering/grouping)
```

### 2. Determine Property Display

**Critical**: The `order` array in views controls which columns appear. Properties MUST be:
1. Present in note frontmatter (not just in body)
2. Listed in the `order` array to display
3. Optionally configured in `properties` section for display names

```yaml
# Properties to display are controlled by the order array
views:
  - type: table
    name: "View Name"
    order:          # Only these properties will show as columns
      - file.name   # Always include for note identification
      - property1   # Must exist in note frontmatter
      - property2   # Must exist in note frontmatter
```

### 3. Build Base Structure

```yaml
# Global filters - applied to all views
filters:
  and:
    - file.inFolder("Target/Folder")
    - 'file.ext == "md"'

# Configure display names for cleaner headers
properties:
  property_name:
    displayName: "Nice Name"

# Define computed values
formulas:
  computed_value: 'expression'

# Create views
views:
  - type: table
    name: "Primary View"
    order:
      - file.name
      - key_property
      - another_property
```

## Property Type Guidelines

| Frontmatter Type | Best Display | Good for Grouping | Good for Filtering |
|------------------|--------------|-------------------|-------------------|
| Text (short) | Direct | Yes | Yes (exact match) |
| Text (long) | Truncate/skip | No | No |
| Number | Direct | No | Yes (ranges) |
| Date | Formatted | Yes (by month/year) | Yes (ranges) |
| List | Join or count | By first item | containsAny |
| Boolean | Icon/text | Yes | Yes |
| Wikilink | Direct | Yes | Yes |

## View Type Selection

| Content Type | Recommended View | Why |
|--------------|------------------|-----|
| Reference data | Table | Scannable, sortable |
| Visual items | Cards | Shows thumbnails |
| Simple lists | List | Minimal, fast |
| Location data | Map | Geographic context |

## Optimal Configurations by Category

### Skills/Tools Catalog
```yaml
order:
  - name
  - description
  - rating
  - invoke       # Command to run
summaries:
  rating: Average
```

### Books/Reading List
```yaml
order:
  - file.name
  - author
  - genre
  - rating
  - status
groupBy:
  property: status
```

### People Directory
```yaml
order:
  - file.name
  - company
  - role
  - topics
```

### Meeting Notes
```yaml
order:
  - file.name
  - date
  - attendees
  - topics
filters:
  and:
    - 'file.mtime > now() - "30d"'  # Recent meetings
```

## Common Patterns

### Filter by Category Property
```yaml
filters:
  and:
    - 'categories.containsAny("[[Category Name]]")'
```

### Multiple Themed Views
```yaml
views:
  - type: table
    name: "All Items"
    order: [file.name, topic, rating]

  - type: table
    name: "By Topic"
    order: [file.name, topic, rating]
    groupBy:
      property: topics
      direction: ASC

  - type: table
    name: "High Rated"
    filters:
      and:
        - 'rating >= 5'
    order: [file.name, topic, rating]
```

### Summary Calculations
```yaml
summaries:
  rating: Average
  price: Sum
  count: Filled    # Count non-empty
```

## Checklist Before Delivery

1. **Properties exist**: All `order` items exist in note frontmatter
2. **Display names set**: Key properties have `displayName` configured
3. **Filters work**: Test filter expressions match expected notes
4. **Views are useful**: Each view serves a distinct purpose
5. **Summaries are relevant**: Only add summaries for numeric/countable fields

## Example: Building a Base for a New Folder

Given a folder `References/Projects/` with notes like:

```yaml
---
name: Project Alpha
status: active
priority: high
owner: "[[John Smith]]"
due: 2024-03-15
topics:
  - "[[Development]]"
  - "[[AI]]"
---
```

Optimal Base:

```yaml
filters:
  and:
    - file.inFolder("References/Projects")
    - 'file.ext == "md"'

properties:
  name:
    displayName: "Project"
  owner:
    displayName: "Owner"
  due:
    displayName: "Due Date"

formulas:
  days_remaining: 'if(due, ((date(due) - today()) / 86400000).round(0), "")'
  is_overdue: 'if(due, date(due) < today() && status != "completed", false)'

views:
  - type: table
    name: "All Projects"
    order:
      - name
      - status
      - priority
      - owner
      - due
      - formula.days_remaining
    groupBy:
      property: status
      direction: ASC

  - type: table
    name: "My Projects"
    filters:
      and:
        - 'owner.contains("[[Current User]]")'
    order:
      - name
      - priority
      - due
      - formula.days_remaining

  - type: table
    name: "Overdue"
    filters:
      and:
        - 'formula.is_overdue == true'
    order:
      - name
      - owner
      - due

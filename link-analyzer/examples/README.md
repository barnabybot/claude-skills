# Link Analyzer Examples

This directory contains example files to demonstrate the link-analyzer skill.

## Contents

### sample-site/
A minimal static site demonstrating various link issues:

| Page | Issue Demonstrated |
|------|-------------------|
| `/` | Hub page with many outbound links |
| `/about/` | Link sink (receives links, doesn't pass them) |
| `/blog/getting-started/` | Well-linked content |
| `/blog/advanced-tips/` | Under-linked (only 1 inbound) |
| `/blog/hidden-gem/` | **Orphan page** (0 inbound links) |
| `/resources/` | Over-linked page (many outbound) |

### sample-outputs/
Example output files showing what the analyzer produces.

## Running the Analysis

```bash
# From the link-analyzer skill directory
cd link-analyzer

# Run full analysis on sample site
python scripts/link_graph.py \
  --dist ./examples/sample-site \
  --output ./examples/sample-outputs/analysis.json \
  --report ./examples/sample-outputs/report.md

# Check internal links only
python scripts/internal_links.py \
  --dist ./examples/sample-site \
  --output ./examples/sample-outputs/internal_links.json
```

## Expected Results

Running on the sample site should find:
- **1 orphan page**: `/blog/hidden-gem/` (no pages link to it)
- **1 under-linked page**: `/blog/advanced-tips/` (only 1 inbound link)
- **1 link sink**: `/about/` (receives 3 links, has 0 outbound)
- **1 over-linked page**: `/resources/` (6 outbound links, threshold is 5 for demo)

## Customizing Thresholds

The sample uses lower thresholds to demonstrate issues with a small site:

```bash
python scripts/link_graph.py \
  --dist ./examples/sample-site \
  --underlinked 2 \
  --overlinked 5 \
  --output analysis.json
```

## Real-World Usage

For a real site build (e.g., Astro, Hugo, Next.js):

```bash
# Point to your build output
python scripts/link_graph.py \
  --dist ./dist \
  --config ./config.json \
  --output ./reports/link_graph.json \
  --report ./reports/link_analysis.md
```

# SEO WordPress Manager Examples

This directory contains sample files demonstrating the SEO WordPress Manager workflow.

## Files

| File | Description |
|------|-------------|
| `analysis_output.json` | Sample output from `analyze_seo.py` showing SEO issues |
| `changes.json` | Sample input for `yoast_batch_updater.py` with optimized SEO data |
| `graphql_queries.md` | Useful GraphQL queries for WordPress SEO management |
| `quick_audit.sh` | Shell script for quick SEO health check |

## Quick Start

### 1. Analyze Current SEO State

```bash
cd /path/to/claude-skills/seo-wordpress-manager

# Analyze all posts
python scripts/analyze_seo.py --all --output examples/my_analysis.json

# Analyze specific category
python scripts/analyze_seo.py --category tutorials --output examples/tutorials_analysis.json
```

### 2. Generate Changes File

After reviewing `analysis_output.json`, create a `changes.json` with your optimized SEO data. See `changes.json` for the expected format.

### 3. Preview Changes

```bash
python scripts/preview_changes.py --input examples/changes.json
```

### 4. Apply Changes

```bash
# Dry run (default)
python scripts/yoast_batch_updater.py --input examples/changes.json

# Apply for real
python scripts/yoast_batch_updater.py --input examples/changes.json --apply
```

## Environment Setup

Set these environment variables or use `config.json`:

```bash
export WP_GRAPHQL_URL="https://your-site.com/graphql"
export WP_USERNAME="your-username"
export WP_APP_PASSWORD="xxxx xxxx xxxx xxxx xxxx xxxx"
```

## Common Workflows

### Audit All Posts
```bash
./examples/quick_audit.sh https://your-site.com/graphql username "app password"
```

### Fix Missing Meta Descriptions
1. Run analysis: `python scripts/analyze_seo.py --all --output analysis.json`
2. Filter for missing descriptions: `jq '.posts | map(select(.meta_desc == "" or .meta_desc == null))' analysis.json`
3. Generate descriptions (Claude helps here)
4. Apply changes via batch updater

### Bulk Title Optimization
1. Export current titles from analysis
2. Optimize for 50-60 character length + keyword placement
3. Create changes.json with new titles
4. Preview and apply

## Tips

- **Always preview first** — the dry-run mode shows exactly what will change
- **Batch size** — default is 10 posts per batch with 1s delay; adjust in config.json
- **Resume capability** — if interrupted, use `--resume` flag to continue
- **Backup current values** — the tool logs original values before changing

# Astro CTA Injector Examples

This directory contains practical examples demonstrating how to use the Astro CTA Injector skill.

## Contents

```
examples/
├── README.md                      # This file
├── sample-blog/                   # Mock Astro blog for testing
│   └── src/content/blog/
│       ├── productivity-tips.md   # High-scoring post for newsletter CTA
│       ├── weekly-update.md       # Low-scoring post (too short)
│       └── task-management.md     # High-scoring post for product CTA
├── config/
│   ├── newsletter-config.json     # Config for newsletter CTA campaign
│   └── product-config.json        # Config for product promotion campaign
├── output/
│   ├── scored_posts.json          # Example scoring output
│   ├── preview_report.md          # Preview of proposed changes
│   └── injection_report.md        # Post-injection summary
└── templates/
    ├── custom-newsletter.html     # Custom styled newsletter CTA
    └── course-promotion.html      # Course/education CTA template
```

## Quick Start

### 1. Score Posts for CTA Relevance

```bash
# From the skill directory
python scripts/score_posts.py \
  --content-path ./examples/sample-blog/src/content/blog \
  --config ./examples/config/newsletter-config.json \
  --output ./examples/output/scored_posts.json
```

### 2. Preview Changes (Dry Run)

```bash
python scripts/preview_injection.py \
  --input ./examples/output/scored_posts.json \
  --output ./examples/output/preview_report.md
```

### 3. Apply Injections

```bash
python scripts/inject_ctas.py \
  --input ./examples/output/scored_posts.json \
  --dry-run false
```

## Example Workflow: Newsletter Signup Campaign

**Goal:** Add newsletter signup CTAs to all productivity-related blog posts.

### Step 1: Configure the Campaign

```json
{
  "content_path": "./src/content/blog",
  "cta_type": "newsletter",
  "template": "./templates/newsletter.html",
  "placement": "after-paragraph-50%",
  "keywords": ["productivity", "tip", "guide", "workflow"],
  "min_score": 5.0,
  "dry_run": true
}
```

### Step 2: Run Scoring

The scoring algorithm evaluates each post based on:
- Keyword density (0-5 points)
- Content length (0-4 points)  
- Title keyword match (0-1 point)

Posts scoring below `min_score` are excluded.

### Step 3: Review & Approve

The preview shows exactly what will be injected and where:

```markdown
## productivity-tips.md
- Score: 8.2/10
- Placement: After paragraph 4 of 8
- CTA: Newsletter signup
- Preview: [see diff]
```

### Step 4: Execute

Once approved, run without `--dry-run` to apply changes.

## Example Workflow: Product Promotion

**Goal:** Add product promotion CTAs to task management articles.

See `config/product-config.json` for configuration and `output/` for expected results.

## Customizing Templates

Create custom templates in the `templates/` directory:

```html
<aside class="cta cta-custom" data-cta-type="custom">
  <h3>{{title}}</h3>
  <p>{{description}}</p>
  <a href="{{product_url}}" class="cta-button">
    {{button_text}}
  </a>
</aside>
```

Available variables:
- `{{title}}` - CTA headline
- `{{description}}` - Body text
- `{{button_text}}` - Button label
- `{{form_url}}` - Form action URL
- `{{product_url}}` - Product page link
- `{{image_url}}` - Image source

## Testing Without Live Site

Use the `sample-blog/` directory as a sandbox:

```bash
# Copy to temp location
cp -r examples/sample-blog /tmp/test-blog

# Run injection on test copy
python scripts/inject_ctas.py \
  --content-path /tmp/test-blog/src/content/blog \
  --config ./examples/config/newsletter-config.json

# Review changes
cat /tmp/test-blog/src/content/blog/productivity-tips.md
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No posts scored above threshold | Lower `min_score` or expand keywords |
| CTA appears in wrong location | Adjust `placement` strategy |
| Template variables not replaced | Check template variable syntax `{{var}}` |
| Duplicate CTAs after re-run | Injector detects `data-cta-type` attribute |

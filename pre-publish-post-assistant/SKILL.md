---
name: pre-publish-post-assistant
description: Pre-publish assistant for new blog posts. Use when the user wants to classify a new post with categories and tags, generate SEO metadata (title, description, focus keyphrase), or get intelligent suggestions with rationale. Works with draft content (file path, URL, or text) and suggests from existing taxonomy to maintain balanced distribution. Also covers the full publish-to-WordPress workflow including image validation, markdown-to-HTML conversion, and post-publish verification.
---

# Pre-publish Post Assistant Skill

## Purpose

This skill covers the full lifecycle of publishing a blog post:

1. **Categories** - From existing site categories, with distribution awareness
2. **Tags** - From existing tags, avoiding tag pollution
3. **SEO Metadata** - Title, meta description, and focus keyphrase
4. **Image Validation** - Check all images before upload to prevent mobile crashes
5. **Publishing** - Markdown-to-HTML conversion, WP REST API update, media handling
6. **Post-Publish Validation** - Verify rendered HTML for responsive images, lazy loading

All suggestions include rationale explaining the reasoning.

## When to Use This Skill

- User says "classify this post" or "suggest categories/tags"
- User asks to "prepare this post for publishing"
- User says "publish to my website" or "push this to WordPress"
- User wants "SEO suggestions" for a draft
- User provides a draft post and asks for taxonomy suggestions
- User mentions "new blog post" and needs categorization help

## Key Principles

### Category Selection
- **Limit to 1-2 categories** per post (primary + optional secondary)
- Prefer categories with moderate post counts (avoid over/under-populated)
- Match content theme, not just keywords
- Consider category hierarchy if applicable

### Tag Selection
- **Limit to 3-5 tags** per post
- Only use existing tags (no new tag creation unless explicitly requested)
- Avoid tag pollution (tags with only 1-2 posts are low value)
- Prefer tags that group related content meaningfully
- Consider tag search potential

### SEO Metadata
- **Title**: 50-60 characters, include primary keyword, compelling
- **Meta Description**: 150-160 characters, summarize value proposition, include CTA
- **Focus Keyphrase**: 2-4 words, searchable, relevant to content

## Input Formats

The skill accepts draft content in multiple formats:

```
# File path
"Classify this post: /path/to/draft.md"

# URL (for already-published posts needing optimization)
"Suggest tags for https://example.com/my-post/"

# Inline text
"Here's my draft: [content]... What categories fit?"
```

## Data Sources

### Categories and Tags
Can be retrieved from:
1. **WordPress GraphQL** - Live data from WP
2. **Static dist folder** - Parse from built site (`/category/`, `/tag/` pages)
3. **Cached taxonomy file** - Pre-generated `taxonomy.json`

### Distribution Data
For balanced suggestions, the skill needs post counts per category/tag:
- Categories: Aim for even distribution, flag if category would become oversized
- Tags: Prefer tags with 5+ posts, warn about orphan tags

## Output Format

```markdown
## Suggested Categories

| Category | Post Count | Confidence | Rationale |
|----------|------------|------------|-----------|
| personal-development | 245 | High | Core theme matches self-improvement focus |
| productivity-effectiveness | 89 | Medium | Secondary theme around habits and routines |

**Recommendation**: Use "personal-development" as primary category.

---

## Suggested Tags

| Tag | Post Count | Confidence | Rationale |
|-----|------------|------------|-----------|
| habits | 45 | High | Central topic of the post |
| productivity | 67 | High | Directly discussed |
| morning-routine | 12 | Medium | Specific example in content |

**Recommendation**: Use all 3 tags. Avoid creating new tags.

---

## SEO Metadata

**Title** (58 chars):
> How to Build Morning Habits That Actually Stick | Your Blog

**Meta Description** (156 chars):
> Discover the science-backed approach to building morning habits that last. Learn the 3-step framework used by high performers. Start your transformation today.

**Focus Keyphrase**:
> morning habits

**Rationale**:
- "morning habits" has good search volume and matches user intent
- Title includes keyphrase naturally at the beginning
- Description creates urgency and promises specific value
```

## Workflow

### 1. Analyze Content
- Extract main themes and topics
- Identify key concepts and terminology
- Determine content type (how-to, opinion, review, etc.)

### 2. Load Taxonomy
- Fetch existing categories with post counts via REST API: `GET /wp-json/wp/v2/categories?per_page=100`
- Fetch existing tags with post counts: `GET /wp-json/wp/v2/tags?per_page=100&orderby=count&order=desc`
- Identify distribution patterns

### 3. Match & Score
- Score each category/tag by relevance
- Consider distribution balance
- Flag potential issues (orphan tags, oversized categories)

### 4. Generate SEO
- Craft title with primary keyword
- Write compelling meta description
- Suggest focus keyphrase

### 5. Validate Images (CRITICAL)

**Why:** WordPress silently fails to process oversized images — no error, just missing thumbnails. This results in raw multi-MB images served without `lazy` loading, `srcset`, or `width`/`height`, which crashes mobile browsers.

Before publishing, check every image referenced in the markdown:

| Check | Threshold | Action if exceeded |
|-------|-----------|-------------------|
| Pixel dimensions | >1600px wide | Resize with `sips --resampleWidth 1600` — prevents WP generating medium_large variants taller than ~3000px for portrait images |
| File size | >2MB | Resize and/or compress (JPEG quality 75-85) |
| Total pixels | >100 million | Resize — this WILL crash phones and may crash WP image processor |
| Aspect ratio | >1:3 (portrait) | Flag and warn — extreme ratios produce very tall WP variants (e.g., 768x2808) that stress mobile decoders. Consider splitting into multiple images. |
| Format | Raw PNG for photos | Convert to JPEG before upload (PNG fine for diagrams <500KB) |

**After uploading to WP media library**, verify the response:
- `media_details.width` and `media_details.height` must be present (not null)
- `media_details.sizes` must contain generated thumbnails (medium, large, etc.)
- If sizes are empty, WP failed to process the image — **do not use it**. Resize smaller and re-upload.

**Resize command (macOS):**
```bash
sips --resampleWidth 1600 input.png --out /tmp/resized.jpg --setProperty format jpeg --setProperty formatOptions 80
```

**After uploading, verify AVIF MIME type on CDN (CRITICAL):**

WordPress/LiteSpeed auto-converts uploads to `.avif`. Hostinger's server must have `AddType image/avif .avif` in `.htaccess` or avif files are served as `text/plain`, which **crashes mobile browsers** (iOS Safari + Chrome both affected).

```bash
# Check MIME type via CDN
curl -sI "https://barnabyrobson.org/wp-content/uploads/2026/02/image.avif" | grep content-type
# Expected: content-type: image/avif
# Bad: content-type: text/plain → CDN cached wrong type
```

If wrong MIME type:
1. Verify `.htaccess` has `AddType image/avif .avif` (add via Code Snippets if missing — see Known Limitations)
2. CDN (`hcdn`) caches stale MIME types for up to 1 year with no PURGE API
3. **Only fix for stale CDN cache:** re-upload images with new filenames to create new URLs that bypass the CDN cache

### 6. Check for Existing Post

Before creating a new WP post, always search first:
```
GET /wp-json/wp/v2/posts?search=<title keywords>&per_page=5
```
If an existing post matches:
- Update it (`POST /wp-json/wp/v2/posts/{id}`) rather than creating a duplicate
- Preserve the existing featured media, categories, and tags unless they need changing
- Check existing Yoast SEO metadata before overwriting

### 7. Publish to WordPress

**Markdown to WordPress HTML conversion:**
- Strip YAML frontmatter and H1 title (WP has its own title field)
- Convert headings to `<!-- wp:heading -->` blocks
- Convert paragraphs to `<!-- wp:paragraph -->` blocks
- Convert lists to `<!-- wp:list -->` blocks with `<!-- wp:list-item -->` children
- Convert inline markdown (bold, italic, links, code) to HTML
- Convert `---` to `<!-- wp:separator -->` blocks
- For images: use `<!-- wp:image {"id":MEDIA_ID,"sizeSlug":"large"} -->` blocks

**REST API update:**
```bash
curl -X POST -u "$USER:$APP_PASSWORD" \
  -H "Content-Type: application/json" \
  -d '{"content":"...","status":"publish"}' \
  "https://barnabyrobson.org/wp-json/wp/v2/posts/{id}"
```

**Homepage visibility:** Posts must include category ID 13 (Essays) to appear on the homepage Query Loop.

### 8. Post-Publish Validation

After updating the post, fetch the rendered content and verify:

```
GET /wp-json/wp/v2/posts/{id}
```

Check every `<img>` tag in `content.rendered`:

| Attribute | Required | Why |
|-----------|----------|-----|
| `loading="lazy"` | Yes | Prevents loading off-screen images on page load |
| `width` + `height` | Yes | Prevents layout shift; WP only adds lazy when these exist |
| `srcset` | Yes | Responsive delivery — mobile gets small image, desktop gets large |
| File format | Should be `.avif` or `.webp` | LiteSpeed/WP auto-converts; raw PNG/JPG >500KB is a red flag |
| AVIF MIME type | `content-type: image/avif` | If served as `text/plain`, mobile browsers crash — see Step 5 AVIF section |

If any image fails these checks, the WP media entry is broken — re-upload a resized version.

**Cache:** Post updates auto-purge LiteSpeed page cache (the page returns `x-litespeed-cache: miss` after update). No manual purge needed. Verify with `curl -sI <url> | grep x-litespeed`. **Note:** This only purges the HTML page cache, not the CDN cache for individual image files (see Known Limitations).

### 9. Present with Rationale
- Show recommendations in table format
- Explain reasoning for each suggestion
- Highlight any concerns or alternatives

## Configuration

```json
{
  "taxonomy_source": "graphql|dist|file",
  "dist_path": "./dist",
  "taxonomy_file": "./taxonomy.json",
  "graphql_endpoint": "https://wp.example.com/graphql",
  "limits": {
    "max_categories": 2,
    "max_tags": 5,
    "min_tag_posts": 3
  },
  "seo": {
    "title_max_length": 60,
    "description_max_length": 160,
    "site_name": "Your Blog"
  }
}
```

## Example Usage

### Basic Classification
```
User: "Classify this post for me: /content/drafts/morning-routine-guide.md"

Claude: [Reads file, analyzes content, fetches taxonomy]
        [Presents category/tag suggestions with rationale]
        [Generates SEO metadata]
```

### Quick Tag Check
```
User: "What tags should I use for a post about Bitcoin ETFs and institutional adoption?"

Claude: [Analyzes topic, checks existing tags]
        "Based on your existing tags, I recommend:
        - bitcoin (89 posts) - primary topic
        - cryptocurrency (45 posts) - broader category
        - investing (23 posts) - relevant angle

        Avoid creating new tags like 'etf' or 'institutional' unless you plan
        to write more content on these specific topics."
```

### SEO Focus
```
User: "Generate SEO metadata for my post about productivity apps for remote workers"

Claude: [Analyzes topic and search intent]

        Title: "Best Productivity Apps for Remote Workers in 2025 | Your Blog"

        Description: "Discover the top productivity apps that remote workers
        swear by. From task management to focus tools, find the perfect
        stack for your home office."

        Focus Keyphrase: "productivity apps remote workers"
```

## Best Practices Enforced

1. **No tag pollution** - Won't suggest creating new tags unless justified
2. **Balanced distribution** - Warns if category is becoming oversized
3. **SEO compliance** - Enforces character limits and keyword placement
4. **Existing taxonomy** - Always checks against actual site data
5. **Transparent reasoning** - Every suggestion includes rationale
6. **Image validation before publish** - Never upload images >5000px or >2MB without resizing first
7. **Post-publish image verification** - Every `<img>` must have lazy loading, dimensions, and srcset
8. **AVIF MIME type verification** - After upload, verify CDN serves `.avif` as `image/avif` not `text/plain`
9. **Aspect ratio awareness** - Flag images with aspect ratio >1:3 that produce oversized WP variants

## Known Limitations

### Yoast SEO Meta Updates
Yoast meta fields (`_yoast_wpseo_metadesc`, `_yoast_wpseo_focuskw`) are **not exposed** via the WP REST API `meta` field or the WPGraphQL `UpdatePostInput` type. Updating Yoast SEO requires either:
- A custom GraphQL mutation registered in `functions.php` (see seo-wordpress-manager skill)
- Manual update via wp-admin

The `og_description` in `yoast_head_json` is read-only in the REST API response. If the existing Yoast metadata is acceptable, leave it rather than attempting to update.

### Hostinger CDN Cache (hcdn)

Hostinger's CDN (`hcdn`) caches static assets (images, CSS, JS) with `max-age=31557600` (1 year). There is **no PURGE API** and no REST endpoint for cache invalidation.

**Impact:** If an image is first served with a wrong MIME type (e.g., `text/plain` for `.avif`), the CDN caches that wrong type for up to a year. Subsequent requests to the same URL get the stale cached response even after the origin server is fixed.

**Workarounds:**
- **New filenames:** Re-upload the image with a different filename → new URL → CDN cache miss → correct MIME type from origin
- **Manual purge:** User must log into Hostinger panel (hpanel.hostinger.com) to purge CDN cache
- **Prevention:** Ensure `.htaccess` has `AddType image/avif .avif` BEFORE uploading any images

### .htaccess Modification via Code Snippets

Server config changes (like adding MIME types) can be made remotely using the Code Snippets REST API:

```php
// Snippet scope: global, hook: init
function fix_avif_mime_type_htaccess() {
    $htaccess = ABSPATH . '.htaccess';
    if (!file_exists($htaccess) || !is_writable($htaccess)) return;
    $content = file_get_contents($htaccess);
    if (strpos($content, 'AVIF MIME Type') !== false) return;
    if (!function_exists('insert_with_markers')) {
        require_once ABSPATH . 'wp-admin/includes/misc.php';
    }
    insert_with_markers($htaccess, 'AVIF MIME Type', array(
        'AddType image/avif .avif',
        'AddType image/avif-sequence .avifs',
    ));
}
add_action('init', 'fix_avif_mime_type_htaccess');
```

**Important:** `insert_with_markers()` lives in `wp-admin/includes/misc.php` — you must `require_once` it when using from `init` hook (it's only auto-loaded on admin pages). Deactivate the snippet after the `.htaccess` change is confirmed (it's persistent).

# Skills Inventory & Capability Matrix

Quick reference for all skills in this repository. Use this to find the right skill for your task.

---

## Quick Lookup Table

| Skill | Category | What It Does | Key Triggers |
|-------|----------|--------------|--------------|
| [9-lov](#9-lov) | Strategy | KPMG 9 Levers of Value framework | "9LoV", "value levers", M&A analysis |
| [astro-cta-injector](#astro-cta-injector) | Web Dev | Inject CTAs into Astro site content | "add CTAs", "newsletter signup" |
| [clip](#clip) | Obsidian | Process web clippings: categorize, add topics, backlinks | "/clip", "process clippings", Clippings/ |
| [docx](#docx) | Documents | Create/edit Word documents with tracked changes | .docx files, redlining |
| [email-processor](#email-processor) | Productivity | Convert emails to Obsidian vault format | "process email", "add to vault" |
| [falcon-maintenance](#falcon-maintenance) | M&A | Update Falcon synergy files from meetings | "update synergies", "scan meetings" |
| [gsc-assistant](#gsc-assistant) | SEO | Track Google Search Console indexing | "indexing status", "GSC" |
| [json-canvas](#json-canvas) | Obsidian | Create/edit JSON Canvas files | .canvas files, mind maps |
| [link-analyzer](#link-analyzer) | SEO | Analyze internal/external links, find broken links | "broken links", "orphan pages" |
| [mcp-builder](#mcp-builder) | Development | Build MCP servers for LLM tool integration | "MCP server", API integrations |
| [obsidian-bases](#obsidian-bases) | Obsidian | Create database-like views in Obsidian | .base files, filters, formulas |
| [obsidian-markdown](#obsidian-markdown) | Obsidian | Obsidian-flavored markdown with wikilinks | callouts, embeds, frontmatter |
| [pdf](#pdf) | Documents | Read, extract, merge, split, fill PDFs | PDF files, form filling |
| [pptx](#pptx) | Documents | Create/edit presentations (KPMG branded) | .pptx files, KPMG slides |
| [pptx-template-setup](#pptx-template-setup) | Documents | Onboard new branded PowerPoint templates | "new template", corporate branding |
| [pre-publish-post-assistant](#pre-publish-post-assistant) | Content | Suggest categories, tags, SEO for blog posts | "classify post", "SEO suggestions" |
| [reflect](#reflect) | Meta | Analyze sessions to improve skills | "/reflect", skill improvements |
| [seo-wordpress-manager](#seo-wordpress-manager) | SEO | Batch update Yoast SEO metadata | "update SEO", Yoast, meta descriptions |
| [skill-creator](#skill-creator) | Meta | Guide for creating new skills | "create skill", skill development |
| [synergy-reviewer](#synergy-reviewer) | M&A | Evaluate synergies against assurance frameworks | "review synergy", auditor prep |
| [vault-cascade-update](#vault-cascade-update) | Obsidian | Propagate updates across vault documents | "update vault", cascade changes |
| [wp-performance-review](#wp-performance-review) | WordPress | Code review for WP performance issues | "slow WordPress", "performance review" |
| [xlsx](#xlsx) | Documents | Create/edit spreadsheets with formulas | .xlsx files, financial models |

---

## By Category

### 📊 Strategy & M&A

| Skill | Purpose | Dependencies |
|-------|---------|--------------|
| **9-lov** | KPMG 9 Levers of Value business analysis | None |
| **falcon-maintenance** | Project Falcon synergy file management | Obsidian vault |
| **synergy-reviewer** | Evaluate synergies against ICAEW/PwC frameworks | None |

### 📝 Document Processing

| Skill | Purpose | Dependencies |
|-------|---------|--------------|
| **docx** | Word document creation, editing, tracked changes | python-docx |
| **pdf** | PDF reading, extraction, merging, form filling | pypdf, pdfplumber |
| **pptx** | PowerPoint creation/editing (KPMG branded) | python-pptx, template files |
| **pptx-template-setup** | Onboard new corporate PPT templates | python-pptx |
| **xlsx** | Spreadsheet creation with formulas | openpyxl |

### 🗄️ Obsidian & PKM

| Skill | Purpose | Dependencies |
|-------|---------|--------------|
| **clip** | Process web clippings: categorize, topics, backlinks | Obsidian vault path |
| **email-processor** | Convert emails to vault documents | Obsidian vault path |
| **json-canvas** | Create/edit .canvas files | None |
| **obsidian-bases** | Create .base files with views/filters | None |
| **obsidian-markdown** | Obsidian-flavored markdown syntax | None |
| **vault-cascade-update** | Propagate changes across vault | Obsidian vault path |

### 🌐 Web & SEO

| Skill | Purpose | Dependencies |
|-------|---------|--------------|
| **astro-cta-injector** | Inject CTAs into Astro content | Python, BeautifulSoup4 |
| **gsc-assistant** | Track GSC indexing status | Sitemap, GSC export data |
| **link-analyzer** | Analyze site link structure | Site file access |
| **pre-publish-post-assistant** | Suggest taxonomy/SEO for posts | Site categories/tags list |
| **seo-wordpress-manager** | Batch update Yoast metadata | WPGraphQL, Yoast plugin |
| **wp-performance-review** | WordPress performance code review | PHP code access |

### 🛠️ Development & Meta

| Skill | Purpose | Dependencies |
|-------|---------|--------------|
| **mcp-builder** | Build MCP servers for LLM tools | Python/Node.js |
| **reflect** | Analyze sessions to improve skills | Active conversation |
| **skill-creator** | Guide for creating new skills | None |

---

## Skill Details

### 9-lov

**KPMG 9 Levers of Value framework for comprehensive business analysis.**

- **Use when:** Business analysis, M&A evaluation, due diligence, value creation planning
- **Key insight:** Operating Model levers (7-9) are systematically overlooked
- **Output:** Structured analysis across Financial, Business, and Operating Models
- **Dependencies:** None

---

### astro-cta-injector

**Inject Call-to-Action blocks into Astro site content.**

- **Use when:** Adding CTAs, newsletter signups, product promotions to blog posts
- **Features:** Multiple placement strategies, content scoring, batch processing
- **Dependencies:** Python 3.10+, BeautifulSoup4

---

### clip

**Process Obsidian web clippings: categorize, add topics, normalize frontmatter, and add backlinks.**

- **Use when:** Processing items in Clippings/ subfolders (Articles, Tweets, Books, Podcasts), Readwise imports, Web Clipper content, or notes with `[[Inbox]]` category
- **Trigger:** `/clip`, "process clippings", "categorize articles", "normalize clippings"
- **Features:** Frontmatter normalization, topic assignment, Kepano-method backlinks, batch processing, web clipper formatting cleanup
- **Dependencies:** Obsidian Core vault

---

### docx

**Comprehensive Word document manipulation.**

- **Use when:** Creating new documents, editing with tracked changes, adding comments
- **Key workflow:** Redlining (recommended for editing external docs)
- **Dependencies:** python-docx

---

### email-processor

**Convert raw emails into structured Obsidian vault documents.**

- **Use when:** Processing emails into vault, batch renaming with dates
- **Output:** YAML frontmatter, wikilinks, date-prefixed filenames
- **Dependencies:** Obsidian vault path

---

### falcon-maintenance

**Project Falcon synergy file maintenance.**

- **Use when:** Scanning meetings for synergy info, updating R01-R10/C01-C22 files
- **Vault:** Specific to Falcon project structure
- **Dependencies:** Falcon vault access

---

### gsc-assistant

**Google Search Console indexing status tracker.**

- **Use when:** Tracking indexing, comparing sitemap vs indexed, managing submissions
- **Output:** indexed.md and to-index.md tracking files
- **Dependencies:** Sitemap, GSC export data

---

### json-canvas

**Create and edit JSON Canvas files (.canvas).**

- **Use when:** Creating visual canvases, mind maps, flowcharts in Obsidian
- **Spec:** JSON Canvas 1.0
- **Dependencies:** None

---

### link-analyzer

**Comprehensive link analysis for static sites.**

- **Use when:** Finding broken links, orphan pages, under-linked content
- **Features:** HTTP validation, false-positive filtering, SEO recommendations
- **Dependencies:** Site file access

---

### mcp-builder

**Guide for creating MCP (Model Context Protocol) servers.**

- **Use when:** Building integrations between LLMs and external services
- **Languages:** Python (FastMCP), Node/TypeScript (MCP SDK)
- **Dependencies:** Python or Node.js

---

### obsidian-bases

**Create Obsidian Bases (.base files) with views, filters, and formulas.**

- **Use when:** Building database-like views of notes
- **Format:** YAML-based
- **Dependencies:** None

---

### obsidian-markdown

**Obsidian Flavored Markdown with all extensions.**

- **Use when:** Creating notes with wikilinks, callouts, embeds, properties
- **Covers:** CommonMark, GFM, LaTeX, Obsidian-specific syntax
- **Dependencies:** None

---

### pdf

**Comprehensive PDF processing toolkit.**

- **Use when:** Reading, extracting text/tables, merging, splitting, filling forms
- **Libraries:** pypdf, pdfplumber
- **Special:** See forms.md for PDF form filling
- **Dependencies:** pypdf, pdfplumber

---

### pptx

**PowerPoint creation and editing (KPMG branded).**

- **Use when:** Creating presentations, especially KPMG-branded
- **Critical:** Always use python-pptx with templates, never PptxGenJS
- **Templates:** `~/Library/Mobile Documents/com~apple~CloudDocs/claude-code/templates/kpmg/`
- **Dependencies:** python-pptx

---

### pptx-template-setup

**Onboard new branded PowerPoint templates.**

- **Use when:** Setting up a new corporate/client template for automation
- **Output:** config.yaml with layouts, placeholders, colors, typography
- **Dependencies:** python-pptx

---

### pre-publish-post-assistant

**Pre-publish assistant for blog posts.**

- **Use when:** Classifying posts, suggesting categories/tags, generating SEO metadata
- **Output:** Suggestions with rationale
- **Dependencies:** Existing site taxonomy

---

### reflect

**Analyze sessions and propose skill improvements.**

- **Use when:** After using a skill, to capture learnings
- **Trigger:** `/reflect` or `/reflect [skill-name]`
- **Dependencies:** Active conversation context

---

### seo-wordpress-manager

**Batch update Yoast SEO metadata in WordPress.**

- **Use when:** Updating SEO titles, descriptions, focus keyphrases
- **Method:** GraphQL mutations via WPGraphQL
- **Dependencies:** WPGraphQL plugin, Yoast SEO, Application Password

---

### skill-creator

**Guide for creating effective skills.**

- **Use when:** Building new skills or updating existing ones
- **Key principle:** Concise is key—context window is a shared resource
- **Dependencies:** None

---

### synergy-reviewer

**Evaluate synergies against assurance frameworks.**

- **Use when:** Reviewing synergy cases, preparing for auditor review
- **Standard:** ICAEW Tech 04/20 "very little risk" test
- **Dependencies:** None

---

### vault-cascade-update

**Propagate updates across Obsidian vault documents.**

- **Use when:** After processing significant new info that affects multiple files
- **Flow:** Source → CLAUDE.md → Primary → Analysis → Action documents
- **Dependencies:** Obsidian vault path

---

### wp-performance-review

**WordPress performance code review.**

- **Use when:** Reviewing WP code for performance issues, auditing before launch
- **Detects:** Unbounded queries, cache bypass, OOM risks, anti-patterns
- **Dependencies:** PHP code access

---

### xlsx

**Comprehensive spreadsheet creation and editing.**

- **Use when:** Creating spreadsheets with formulas, analyzing data, financial models
- **Standards:** Zero formula errors, industry-standard color coding
- **Dependencies:** openpyxl

---

## Skill Combinations

Common multi-skill workflows:

| Workflow | Skills Used |
|----------|-------------|
| M&A analysis | 9-lov → synergy-reviewer → falcon-maintenance |
| New blog post | pre-publish-post-assistant → seo-wordpress-manager |
| Vault update | email-processor → vault-cascade-update |
| Clippings processing | clip → vault-cascade-update |
| Template onboarding | pptx-template-setup → pptx |
| Skill development | skill-creator → reflect |
| Site audit | link-analyzer → gsc-assistant → wp-performance-review |

---

*Last updated: 2026-02-02*

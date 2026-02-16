# CLAUDE.md

This repository is a collection of modular skills for Claude Code and OpenClaw agents. Each skill is a self-contained package (folder with a `SKILL.md` file) that provides specialized instructions, scripts, references, and assets for a specific domain.

## Repository Structure

```
claude-skills/
├── CLAUDE.md              # This file
├── README.md              # Project overview and skill list
├── SKILLS.md              # Detailed inventory with categories, triggers, dependencies
├── .gitignore
├── template-clean.pptx    # Shared KPMG PowerPoint template
└── <skill-name>/          # One folder per skill (31 total)
    ├── SKILL.md           # Main instructions (required)
    ├── references/        # Domain docs loaded into context as needed (optional)
    ├── scripts/           # Executable Python/Bash helpers (optional)
    ├── assets/            # Templates, fonts, images for output (optional)
    └── examples/          # Usage examples (optional)
```

## How Skills Work

Skills use a **progressive disclosure** loading model:

1. **Metadata** (name + description in YAML frontmatter) — always in context; determines when a skill triggers
2. **SKILL.md body** — loaded when the skill triggers; target <8k chars (~2k tokens)
3. **Bundled resources** (scripts, references, assets) — loaded on demand or executed without loading

The `description` field in frontmatter is the only field used to match tasks to skills. It must include what the skill does, when to use it, and trigger keywords.

## Skill Categories

| Category | Skills |
|----------|--------|
| **Documents** | `docx`, `pdf`, `pptx`, `pptx-template-setup`, `xlsx` |
| **Obsidian/PKM** | `obsidian-markdown`, `obsidian-bases`, `obsidian-base-builder`, `json-canvas`, `email-processor`, `vault-cascade-update` |
| **Web & SEO** | `link-analyzer`, `gsc-assistant`, `seo-wordpress-manager`, `pre-publish-post-assistant`, `wp-performance-review`, `astro-cta-injector` |
| **Strategy & M&A** | `9-lov`, `synergy-reviewer`, `falcon-maintenance`, `integration-separation` |
| **Development & Meta** | `skill-creator`, `reflect`, `mcp-builder`, `organize` |
| **Other** | `clip`, `tasknotes`, `podcast-transcript`, `midjourney`, `nano-banana`, `seat-monitor` |

See `SKILLS.md` for the full inventory with triggers, dependencies, and multi-skill workflows.

## Key Conventions

### Skill Design Rules

- **Context efficiency is the highest priority.** The context window is shared. Skip anything Claude already knows (standard markdown, stdlib, common patterns). Only document domain-specific knowledge, pitfalls, and non-obvious workflows.
- **SKILL.md must stay under 500 lines / 8k characters.** Extract detailed references, schemas, and large tables into separate files under `references/`.
- **Do not create extraneous documentation files** (no README.md, CHANGELOG.md, INSTALLATION_GUIDE.md, etc. inside skill folders). The skill should only contain what an AI agent needs to do the job.
- **Use imperative form** in all instructions ("Create", "Edit", "Run", not "You should create").
- **Prefer concise examples over verbose explanations.**
- **Information should appear once.** Do not duplicate content between SKILL.md and reference files.

### Frontmatter Format

Every SKILL.md requires exactly this YAML frontmatter:

```yaml
---
name: skill-name
description: "What the skill does. When to use it. Trigger keywords."
license: Complete terms in LICENSE.txt
---
```

No other frontmatter fields. The `description` must be comprehensive since it is the sole trigger mechanism.

### File and Folder Naming

- Skill folders: lowercase with hyphens (`obsidian-markdown`, `email-processor`)
- Python files: lowercase with underscores (`rotate_pdf.py`, `init_skill.py`)
- Reference files: lowercase with hyphens (`color-palettes.md`, `docx-js.md`)

### Creating New Skills

Use the `skill-creator` skill as a guide. The standard process:

1. Understand the skill with concrete examples
2. Plan reusable resources (scripts, references, assets)
3. Initialize with `scripts/init_skill.py <skill-name> --path <output-directory>`
4. Implement resources and write SKILL.md
5. Package with `scripts/package_skill.py <path/to/skill-folder>`
6. Iterate based on real usage

### Improving Existing Skills

Use the `reflect` skill (`/reflect` or `/reflect [skill-name]`) after using a skill to capture learnings and propose improvements.

## Common Dependencies

Skills have no shared dependency file. Dependencies are skill-specific and documented in each SKILL.md:

| Domain | Common Libraries |
|--------|-----------------|
| Word documents | `python-docx` |
| PowerPoint | `python-pptx` |
| Excel | `openpyxl`, `pandas` |
| PDF | `pypdf`, `pdfplumber`, `reportlab` |
| OOXML editing | `defusedxml`, custom `ooxml/scripts/` |
| Web scraping | `BeautifulSoup4`, `playwright` |
| Conversion | `pandoc`, `LibreOffice` |

## Build and Test

There is no centralized build system or test suite. This is a content repository — skills are text-based instructions loaded into Claude's context at runtime.

- **Testing is skill-specific**: some skills include tests (e.g., `pdf/scripts/check_bounding_boxes_test.py` uses pytest)
- **Validation**: Run `scripts/package_skill.py <skill-folder>` to validate a skill's structure and frontmatter before distribution
- **PPTX verification**: Generate thumbnails with `python scripts/thumbnail.py output.pptx`
- **XLSX verification**: Confirm zero formula errors (#REF!, #DIV/0!, etc.)
- **OOXML workflow**: Unpack → edit XML → validate → repack using scripts in `ooxml/scripts/`

## Git Workflow

- Default branch: `main`
- Commit messages follow conventional format: `<skill-name>: <description of change>`
- GPG signing enabled via SSH key
- PRs used for integration (automated example generation via `barnabybot`)

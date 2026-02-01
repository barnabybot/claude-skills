# Claude Skills

A collection of skills for Claude Code / OpenClaw agents. Each skill provides specialized instructions for specific tasks.

## What Are Skills?

Skills are structured guides (SKILL.md files) that teach Claude how to handle specific domains—from document processing to SEO management to Obsidian automation. Agents load the relevant SKILL.md when a task matches its description.

## Available Skills

| Skill | Description |
|-------|-------------|
| **9-lov** | KPMG framework for business value analysis across Financial, Business, and Operating Models |
| **astro-cta-injector** | Inject Call-to-Action blocks into Astro site content |
| **docx** | Create, edit, and analyze .docx files (Word documents) |
| **email-processor** | Process raw emails into structured Obsidian vault documents |
| **falcon-maintenance** | Maintain Project Falcon synergy files from meeting minutes |
| **gsc-assistant** | Manage Google Search Console indexing status via tracking files |
| **json-canvas** | Create and edit JSON Canvas files (.canvas) for Obsidian |
| **link-analyzer** | Comprehensive link analysis for static websites |
| **mcp-builder** | Create MCP (Model Context Protocol) servers for LLM tooling |
| **obsidian-bases** | Create and edit Obsidian Bases (.base files) with views/filters |
| **obsidian-markdown** | Obsidian Flavored Markdown with wikilinks, callouts, embeds |
| **pdf** | PDF processing, form filling, and manipulation |
| **pptx** | Create, edit, and analyze PowerPoint presentations |
| **pptx-template-setup** | Onboard branded PowerPoint templates for automation |
| **pre-publish-post-assistant** | Prepare blog posts for publication with intelligent suggestions |
| **reflect** | Analyze conversations and propose skill improvements |
| **seo-wordpress-manager** | Manage Yoast SEO metadata via WPGraphQL API |
| **skill-creator** | Guide for creating effective new skills |
| **synergy-reviewer** | Evaluate synergies against ICAEW/PwC assurance frameworks |
| **vault-cascade-update** | Propagate updates across Obsidian vault documents |
| **wp-performance-review** | WordPress performance code review with severity levels |
| **xlsx** | Create, edit, and analyze Excel spreadsheets |

## Usage

### With OpenClaw

Add skills to your agent's skill path in `openclaw.yaml`:

```yaml
skills:
  paths:
    - /path/to/claude-skills
```

### With Claude Code

Point to skills via project configuration or include them in your workspace.

### Manual

Each skill folder contains a `SKILL.md` file with complete instructions. Read the relevant SKILL.md before tackling a task in that domain.

## Structure

```
skill-name/
├── SKILL.md          # Main instructions (required)
├── reference.md      # Additional reference material (optional)
├── examples/         # Example files (optional)
└── scripts/          # Helper scripts (optional)
```

## Contributing

1. Create a new folder with your skill name
2. Add a `SKILL.md` following the patterns in existing skills
3. Include examples and references where helpful
4. Submit a PR

## License

MIT

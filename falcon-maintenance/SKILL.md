---
name: falcon-maintenance
description: Project Falcon synergy file maintenance workflows. Use when scanning meetings for synergy information, updating R01-R10 (revenue) or C01-C22 (cost) synergy files, cross-referencing meeting content, or identifying gaps between meeting minutes and synergy documentation. Triggers on "update synergies", "scan meetings", "cross-reference", "Falcon", "revenue synergies", "cost synergies".
---

# Falcon Maintenance

Workflows for maintaining Project Falcon synergy files by extracting information from meeting minutes and updating synergy bucket documentation.

## Context

- **Vault**: `/Users/barnabyrobson/Library/Mobile Documents/iCloud~md~obsidian/Documents/Falcon`
- **Revenue Synergies**: R01-R10 in `Revenue Synergies/`
- **Cost Synergies**: C01-C22 in `Cost Synergies/`
- **Meetings**: `Meetings/` (41+ files, format: `YYYY-MM-DD Meeting Title.md`)

Always read the vault's `CLAUDE.md` first for full context on bucket definitions and key stakeholders.

## Workflow: Meeting-to-Synergy Update

### Step 1: Scope the Task

Determine which synergy type (revenue/cost) and date range to scan.

### Step 2: Parallel Meeting Scan

Dispatch **parallel Task agents** with `subagent_type=Explore` to scan meetings by date range:

```
Agent 1: Jan 5-9 meetings
Agent 2: Jan 12-14 meetings
Agent 3: Jan 15-17 meetings
```

**Prompt template for agents:**
```
Scan all meeting files from [DATE RANGE] in [VAULT]/Meetings/ for [COST/REVENUE] synergy information.

The [22 cost / 10 revenue] synergy workstreams are:
[LIST BUCKETS]

Look for:
1. Specific figures (savings, revenue, FTE reductions)
2. CTA (Cost to Achieve) discussions
3. Operating model changes
4. Attrition/severance constraints
5. Technology consolidation
6. Key quotes from stakeholders

Return findings organized by synergy bucket.
```

### Step 3: Gap Analysis

Compare agent findings against existing "Meeting Cross-References" sections in synergy files. Identify:
- Missing meeting references
- New quantified data
- Updated constraints or risks

### Step 4: Update Files

Add new meeting content using standard format:

```markdown
### YYYY-MM-DD Meeting Title

Per [[YYYY-MM-DD Meeting Title]]:

**Key Finding Category:**
- Bullet point with [[wikilinks]] for people/concepts
- Specific figures in **bold**

> "Direct quote" - **[[Speaker Name]]**
```

**Placement**: Insert chronologically within "Meeting Cross-References" section.

## Meeting Content Patterns

### Cost Synergies (C01-C22)

Look for:
- FTE reductions and headcount targets
- Severance vs attrition discussions
- CTA breakdown (severance, tech, non-tech)
- ServCo/shared services model changes
- PwC haircut expectations (~30%)

### Revenue Synergies (R01-R10)

Look for:
- Run-rate revenue figures
- Transaction attribution arguments
- Catch-up vs co-build distinction
- FRP baseline references
- Customer pool and penetration rates

## Key Stakeholders (Quick Reference)

| Name | Role | Relevant For |
|------|------|--------------|
| Omar Malik | CFO HK | CTA caps, severance constraints |
| Rob Wall | Strategy Lead | Revenue synergy definitions |
| Kaushik Sridhar | Cost Lead | Cost synergy validation |
| Steve Liberman | MSS Lead | C06 CIB MSS specifics |

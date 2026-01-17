---
name: vault-cascade-update
description: Propagate new information across interconnected Obsidian vault documents. Use after processing a significant new document (email, meeting notes) that has vault-wide impact, requiring updates to CLAUDE.md, risk logs, synergy files, priority actions, and analysis documents.
---

# Vault Cascade Update Skill

When new information enters the vault (e.g., a critical email or meeting notes), systematically propagate relevant updates across all affected documents.

## When to Use

- After processing a significant email with project-wide implications
- After adding meeting notes that change priorities, risks, or status
- When user says "update the vault" or "propagate this across documents"
- When new constraints, deadlines, or decisions affect multiple files

## Cascade Hierarchy

Updates flow through the vault in this order:

```
1. Source Document (email/meeting)
        ↓
2. CLAUDE.md (vault context file)
        ↓
3. Primary Documents (synergy buckets, workstream files)
        ↓
4. Analysis Documents (risk log, 9 levers, paper analysis)
        ↓
5. Action Documents (priority actions, hypothesis tracker)
```

## Update Patterns by Document Type

### 1. CLAUDE.md Updates

The vault's CLAUDE.md is the central context file. Update when source contains:

| Content Type | CLAUDE.md Section |
|--------------|-------------------|
| New deadlines/dates | Key Dates table |
| Status changes | Current Status section |
| New constraints | Add callout/warning |
| Strategy shifts | Key Issues section |
| New risks | Reference to Risk Log |

**Format for constraints:**
```markdown
> [!warning] Constraint Name (Date)
> - Bullet point details
> - Source reference: Per [[Source Document]]
```

### 2. Synergy/Bucket File Updates

When source affects specific synergies or workstreams:

**Add a dated feedback section:**
```markdown
---

## [Source Type] Feedback (DD Mon YYYY)

Per [[Source Document]]:

**Challenge/Finding:**
| Issue | Required Response |
|-------|-------------------|
| Specific issue | What needs to happen |

**Constraints:**
> [!warning] Constraint Name
> - Details

**Action Required:**
- Specific action items
```

**Placement:** Before "## Related Documents" section

### 3. Risk Log Updates

When source surfaces new risks:

**Add to Risk Summary table:**
```markdown
| **RX** | **Risk Name** | **Likelihood** | **Impact** | **NEW (Date)** |
```

**Add full risk section:**
```markdown
---

## RX: Risk Name (NEW - Date)

**Risk:** One-sentence description.

| Aspect | Detail |
|--------|--------|
| **Key Metric** | Value |

**From [[Source Document]]:**
> "Direct quote if available"

**Mitigations:**
- [ ] Action item 1
- [ ] Action item 2
```

**Update interconnections diagram** if risk relates to existing risks.

### 4. Analysis Documents (9 Levers, Paper Analysis)

When source changes strategic context:

- Update relevant lever assessments
- Add source feedback to appropriate sections
- Update status indicators (🟢🟡🔴) if warranted
- Add to priority recommendations if new actions needed

### 5. Priority Actions Updates

When source contains action items or deadlines:

- Add to executive summary if significant
- Insert dated action lists with COB deadlines
- Update "Immediate Next Steps" section
- Add source to "Emails/Meetings Processed" table

## Parallel Agent Strategy

For large cascades (>5 files affected), use parallel Sonnet agents:

```
Agent 1: CLAUDE.md + Risk Log
Agent 2: Revenue synergy files (R01-R10)
Agent 3: Cost synergy files (C01-C22)
Agent 4: Analysis documents (9 Levers, Paper Analysis, Priority Actions)
```

**Agent prompt template:**
```
Update [document type] files with [source type] from [source document].

Files to update:
- [list of file paths]

Key information to propagate:
- [bullet points of key content]

Add a "[Source Type] (Date)" section with:
- Reference to source document
- Relevant content extracted
- Action items if applicable

Format: [specific format guidance]
```

## Wikilink Consistency

When adding content across files:

- Use consistent wikilinks for people: `[[Full Name]]` or `[[Full Name|Short Name]]`
- Use consistent wikilinks for source: `[[YYYY-MM-DD Source Title]]`
- Cross-reference related documents in "Related" sections

## Cascade Checklist

After processing a significant source document:

- [ ] **CLAUDE.md** - Key dates, status, constraints updated
- [ ] **Primary documents** - Relevant synergy/bucket files have feedback section
- [ ] **Risk Log** - New risks added with mitigations
- [ ] **9 Levers Analysis** - Relevant levers updated
- [ ] **Paper Analysis** - Page-by-page updates if applicable
- [ ] **Priority Actions** - New actions and deadlines added
- [ ] **Cross-references** - Source document linked from all updated files

## Example: Email Cascade

**Source:** Critical email with FMG feedback

**Cascade:**

1. **CLAUDE.md:**
   - Add 6 new key dates
   - Add FMG constraint callout
   - Add FMG feedback to Key Issues

2. **R01, R02, R04 (revenue synergies):**
   - Add "FMG Feedback (Date)" section to each
   - Specific challenges and required responses

3. **C01-C22 (cost synergies):**
   - Add "FMG Constraints (Date)" section to all
   - Severance cap, attrition model details

4. **Risk Log:**
   - Add R9: Severance CTA Cap
   - Add R10: Double-Counting Risk
   - Add R11: "Not Aggressive Enough" Risk

5. **9 Levers Analysis:**
   - Update Lever 1 (Financial) with constraints
   - Update Lever 8 (People) with severance cap
   - Change status from 🟡 to 🔴 where warranted

6. **Priority Actions:**
   - Add FMG feedback section
   - Update immediate next steps with deadlines
   - Add to emails processed table

## Quality Checks

After cascade:
- [ ] All updated files reference the source document
- [ ] No conflicting information between files
- [ ] Wikilinks consistent across all updates
- [ ] Dates formatted consistently (YYYY-MM-DD in filenames, readable in content)
- [ ] Action items have owners and deadlines where possible

---
name: reflect
description: Analyze the current session and propose improvements to skills. Run after using a skill to capture learnings. Use when user says "reflect", "improve skill", "learn from this", or at end of skill-heavy sessions.
---

# Reflect Skill

Analyze the current conversation and propose improvements to skills based on what worked, what didn't, and edge cases discovered.

## Trigger

Run `/reflect` or `/reflect [skill-name]` after a session where you used a skill.

## Successive Reflections

If `/reflect` is run multiple times in the same session:

1. **Reference prior changes** - Acknowledge any skill edits made earlier
2. **Look for new signals** - Focus on what happened AFTER the last reflection
3. **Avoid duplicate proposals** - Don't re-propose changes already applied

For **meta-reflection** (reflecting on reflect itself):
- This is a valid use case for iterative skill improvement
- Check if earlier reflect changes are working as intended
- Propose refinements based on the reflection workflow itself

## Workflow

### Step 1: Identify the Skill(s)

If skill name not provided:

1. **MANDATORY FIRST: Read user's CLAUDE.md** — Check `~/.claude/CLAUDE.md` or the project's CLAUDE.md for declared skill locations. DO NOT skip this step. DO NOT guess paths. The CLAUDE.md file explicitly lists where skills are stored.
2. **Only then scan directories** listed in CLAUDE.md (not generic defaults)
3. **List actual installed skills** for selection (not generic examples)
4. **Accept full paths** if user provides one (e.g., `/path/to/skill` or `skill-name`)

**CRITICAL:** Do not search `~/.claude/skills/` or other default paths before reading CLAUDE.md. The user's configuration takes precedence.

```
Which skill should I analyze this session for?
[List skills actually found in user's environment]
```

**Multiple skills**: If user provides multiple skill names (e.g., "skill-a, skill-b"), analyze each and present findings side-by-side or sequentially. Apply changes to each skill separately with individual commits.

### Step 2: Analyze the Conversation

Look for these signals in the current conversation:

**Corrections** (HIGH confidence):
- User said "no", "not like that", "I meant..."
- User explicitly corrected output
- User asked for changes immediately after generation

**Successes** (MEDIUM confidence):
- User said "perfect", "great", "yes", "exactly"
- User accepted output without modification
- User built on top of the output

**Edge Cases** (MEDIUM confidence):
- Questions the skill didn't anticipate
- Scenarios requiring workarounds
- Features user asked for that weren't covered

**Preferences** (accumulate over sessions):
- Repeated patterns in user choices
- Style preferences shown implicitly
- Tool/framework preferences

**Coverage Gaps** (potential new skills):
- Session involved work no existing skill covers
- User needed functionality outside current skill scope
- Workarounds suggest missing skill or skill extension
- Note these as potential new skill opportunities

### Step 3: Propose Changes

Present findings using accessible colors (WCAG AA 4.5:1 contrast ratio):

```
┌─ Skill Reflection: [skill-name] ─────────────────────────────┐
│                                                              │
│  Signals: X corrections, Y successes                         │
│                                                              │
│  Proposed changes:                                           │
│                                                              │
│  🔴 [HIGH] + Add constraint: "[specific constraint]"         │
│  🟡 [MED]  + Add preference: "[specific preference]"         │
│  🔵 [LOW]  ~ Note for review: "[observation]"                │
│                                                              │
│  Commit: "[skill]: [summary of changes]"                     │
│                                                              │
└──────────────────────────────────────────────────────────────┘

Apply these changes? [Y/n] or describe tweaks
```

**Accessible Color Palette** (use ANSI codes in terminal output):
- HIGH: `\033[1;31m` (bold red #FF6B6B - 4.5:1 on dark)
- MED: `\033[1;33m` (bold yellow #FFE066 - 4.8:1 on dark)
- LOW: `\033[1;36m` (bold cyan #6BC5FF - 4.6:1 on dark)
- Reset: `\033[0m`

Avoid: pure red (#FF0000) on black, green on red (colorblind users)

- **Y** — Apply changes, commit, and push
- **n** — Skip this update
- Or describe any tweaks to the proposed changes

### Step 4: If Approved

1. Read the current skill file from the identified path
2. Apply the changes using the Edit tool
3. Run git commands from the skill's parent directory:
   ```bash
   cd [skill-parent-directory]  # Use actual path, not hardcoded
   git add [skill-name]/SKILL.md
   git commit -m "[skill]: [change summary]"
   git push origin main
   ```
4. Confirm: "Skill updated and pushed to GitHub"

**Note:** If the skill directory is not a git repo, skip git operations and just confirm the edit was saved.

### Step 5: If Declined

Ask: "Would you like to save these observations for later review?"

If yes, append to `~/.claude/skills/[skill-name]/OBSERVATIONS.md`

## Custom Skill Locations

**IMPORTANT:** Always check CLAUDE.md first to find the user's actual skill location. Do not assume defaults.

Skills may be located in various places (check CLAUDE.md for which applies):

| Priority | Location | Example |
|----------|----------|---------|
| 1 | **User's CLAUDE.md** | Read `~/.claude/CLAUDE.md` first — it declares the actual path |
| 2 | iCloud sync | `~/Library/Mobile Documents/com~apple~CloudDocs/claude-code/skills/` |
| 3 | Project-local | `./.claude/skills/` |
| 4 | Default | `~/.claude/skills/` |

When user provides a full path, use that path directly. When given just a skill name, **read CLAUDE.md first** to find the configured location.

## Git Integration

This skill has permission to:
- Read skill files from any user-specified location
- Edit skill files (with user approval)
- Run `git add`, `git commit`, `git push` in the skill's parent directory

The skills directory should be a git repo with a remote origin for push to work.

## Important Notes

- Always show the exact changes before applying
- Never modify skills without explicit user approval
- Commit messages should be concise and descriptive
- Push only after successful commit

## Example Session

User runs `/reflect frontend-design` after a UI session:

```
┌─ Skill Reflection: frontend-design ──────────────────────────┐
│                                                              │
│  Signals: 2 corrections, 3 successes                         │
│                                                              │
│  Proposed changes:                                           │
│                                                              │
│  🔴 [HIGH] + Constraints/NEVER:                              │
│            "Use gradients unless explicitly requested"       │
│                                                              │
│  🔴 [HIGH] + Color & Theme:                                  │
│            "Dark backgrounds: use #000, not #1a1a1a"         │
│                                                              │
│  🟡 [MED]  + Layout:                                         │
│            "Prefer CSS Grid for card layouts"                │
│                                                              │
│  Commit: "frontend-design: no gradients, #000 dark"          │
│                                                              │
└──────────────────────────────────────────────────────────────┘

Apply these changes? [Y/n] or describe tweaks
```

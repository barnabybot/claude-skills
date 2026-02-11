# Email Processor Examples

Sample templates and patterns for email processing workflows.

## Files

| Example | Description |
|---------|-------------|
| `triage_rules.json` | Sample email triage rules (priority, labels, actions) |
| `response_templates.md` | Common response templates for different scenarios |

## Common Patterns

### Triage Flow
1. Extract sender, subject, body
2. Match against rules (domain, keywords, patterns)
3. Apply actions (label, priority, draft response)
4. Surface important items

### Key Signals
- **Urgent**: "URGENT", "ASAP", "deadline", sender in VIP list
- **Action needed**: "please", "can you", "need you to", question marks
- **FYI only**: "FYI", "no action", newsletters, automated reports

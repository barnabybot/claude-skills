# DOCX Skill Examples

Practical examples for Word document creation, editing, and analysis.

## Contents

| Example | Description |
|---------|-------------|
| `create_document.js` | Create a new Word document with docx-js |
| `extract_text.sh` | Extract text with tracked changes using pandoc |
| `analyze_document.py` | Analyze document structure via OOXML |

## Quick Start

```bash
# Create a new document
node create_document.js

# Extract text showing tracked changes
./extract_text.sh document.docx

# Analyze document structure
python analyze_document.py document.docx
```

## Dependencies

```bash
# For document creation
npm install docx

# For text extraction
# pandoc (usually pre-installed)

# For OOXML analysis
pip install lxml
```

## Notes

- For editing someone else's documents, use the redlining workflow in SKILL.md
- docx-js is ideal for creating new documents from scratch
- OOXML manipulation is needed for tracked changes and comments

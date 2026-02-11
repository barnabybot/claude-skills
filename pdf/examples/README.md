# PDF Skill Examples

Practical examples for PDF processing, extraction, and manipulation.

## Contents

| Example | Description |
|---------|-------------|
| `extract_text.py` | Extract text content from PDF pages |
| `extract_tables.py` | Extract tables to CSV using pdfplumber |
| `merge_split.py` | Merge multiple PDFs or split into pages |
| `pdf_info.py` | Display PDF metadata and page info |

## Quick Start

```bash
# Extract all text
python extract_text.py document.pdf

# Extract tables to CSV
python extract_tables.py document.pdf

# Merge PDFs
python merge_split.py merge doc1.pdf doc2.pdf -o combined.pdf

# Split PDF into pages
python merge_split.py split document.pdf -o output_dir/

# Get PDF info
python pdf_info.py document.pdf
```

## Dependencies

```bash
pip install pypdf pdfplumber
```

## Notes

- For form filling, see `forms.md` in the parent directory
- pdfplumber excels at table extraction
- pypdf is best for structural operations (merge, split, rotate)
- For advanced operations, see `reference.md`

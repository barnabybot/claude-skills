#!/bin/bash
# Extract text content from a PowerPoint file
#
# Usage:
#   ./extract_text.sh presentation.pptx
#   ./extract_text.sh presentation.pptx output.md
#
# Dependencies:
#   pip install markitdown

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <presentation.pptx> [output.md]"
    exit 1
fi

INPUT="$1"
OUTPUT="${2:-}"

if [ ! -f "$INPUT" ]; then
    echo "Error: File not found: $INPUT"
    exit 1
fi

if [ -n "$OUTPUT" ]; then
    python -m markitdown "$INPUT" > "$OUTPUT"
    echo "Extracted to: $OUTPUT"
else
    python -m markitdown "$INPUT"
fi

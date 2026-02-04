#!/bin/bash
# Extract text from a Word document with tracked changes visibility
#
# Usage:
#   ./extract_text.sh document.docx                    # Show all tracked changes
#   ./extract_text.sh document.docx accept             # Show with changes accepted
#   ./extract_text.sh document.docx reject             # Show with changes rejected
#   ./extract_text.sh document.docx all output.md     # Save to file
#
# Dependencies:
#   pandoc (usually pre-installed on most systems)

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <document.docx> [accept|reject|all] [output.md]"
    echo ""
    echo "Track changes modes:"
    echo "  accept  - Show document with all changes accepted"
    echo "  reject  - Show document with all changes rejected"
    echo "  all     - Show insertions and deletions marked (default)"
    exit 1
fi

INPUT="$1"
MODE="${2:-all}"
OUTPUT="${3:-}"

if [ ! -f "$INPUT" ]; then
    echo "Error: File not found: $INPUT"
    exit 1
fi

# Validate mode
case "$MODE" in
    accept|reject|all)
        ;;
    *)
        echo "Error: Invalid mode '$MODE'. Use: accept, reject, or all"
        exit 1
        ;;
esac

if [ -n "$OUTPUT" ]; then
    pandoc --track-changes="$MODE" "$INPUT" -o "$OUTPUT"
    echo "Extracted to: $OUTPUT (track-changes=$MODE)"
else
    pandoc --track-changes="$MODE" "$INPUT" -t markdown
fi

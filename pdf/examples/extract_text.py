#!/usr/bin/env python3
"""
Extract text content from a PDF file.

This example demonstrates:
- Opening and reading PDF files
- Extracting text from all or specific pages
- Handling multi-page documents
- Output to file or stdout

Usage:
    python extract_text.py document.pdf
    python extract_text.py document.pdf --page 1
    python extract_text.py document.pdf --output text.txt
"""

import sys
import argparse
from pypdf import PdfReader


def extract_text(pdf_path: str, page_num: int = None, output_path: str = None):
    """Extract text from a PDF file."""
    
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)
    
    print(f"File: {pdf_path}", file=sys.stderr)
    print(f"Pages: {total_pages}", file=sys.stderr)
    print("-" * 40, file=sys.stderr)
    
    text_parts = []
    
    if page_num is not None:
        # Extract specific page (1-indexed for user, 0-indexed internally)
        if page_num < 1 or page_num > total_pages:
            print(f"Error: Page {page_num} out of range (1-{total_pages})", file=sys.stderr)
            sys.exit(1)
        
        page = reader.pages[page_num - 1]
        text = page.extract_text()
        text_parts.append(f"=== Page {page_num} ===\n{text}")
    else:
        # Extract all pages
        for i, page in enumerate(reader.pages, 1):
            text = page.extract_text()
            if text.strip():
                text_parts.append(f"=== Page {i} ===\n{text}")
    
    full_text = "\n\n".join(text_parts)
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_text)
        print(f"Written to: {output_path}", file=sys.stderr)
    else:
        print(full_text)


def main():
    parser = argparse.ArgumentParser(
        description="Extract text from a PDF file"
    )
    parser.add_argument("pdf", help="Path to PDF file")
    parser.add_argument("-p", "--page", type=int, help="Extract specific page (1-indexed)")
    parser.add_argument("-o", "--output", help="Output file path")
    
    args = parser.parse_args()
    extract_text(args.pdf, args.page, args.output)


if __name__ == "__main__":
    main()

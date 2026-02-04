#!/usr/bin/env python3
"""
Merge multiple PDFs or split a PDF into individual pages.

This example demonstrates:
- Merging multiple PDF files
- Splitting a PDF into separate page files
- Using pypdf's PdfReader and PdfWriter

Usage:
    # Merge PDFs
    python merge_split.py merge file1.pdf file2.pdf file3.pdf -o merged.pdf
    
    # Split PDF into pages
    python merge_split.py split document.pdf -o output_directory/
"""

import sys
import argparse
from pathlib import Path
from pypdf import PdfReader, PdfWriter


def merge_pdfs(pdf_paths: list, output_path: str):
    """Merge multiple PDF files into one."""
    
    writer = PdfWriter()
    total_pages = 0
    
    for pdf_path in pdf_paths:
        print(f"Adding: {pdf_path}", file=sys.stderr)
        reader = PdfReader(pdf_path)
        
        for page in reader.pages:
            writer.add_page(page)
            total_pages += 1
    
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)
    
    print(f"\nMerged {len(pdf_paths)} files ({total_pages} pages) → {output_path}", file=sys.stderr)


def split_pdf(pdf_path: str, output_dir: str):
    """Split a PDF into individual page files."""
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    reader = PdfReader(pdf_path)
    stem = Path(pdf_path).stem
    
    print(f"Splitting: {pdf_path} ({len(reader.pages)} pages)", file=sys.stderr)
    
    for i, page in enumerate(reader.pages, 1):
        writer = PdfWriter()
        writer.add_page(page)
        
        page_path = output_path / f"{stem}_page{i:03d}.pdf"
        with open(page_path, 'wb') as f:
            writer.write(f)
        
        print(f"  Created: {page_path}", file=sys.stderr)
    
    print(f"\nSplit into {len(reader.pages)} files in {output_dir}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Merge or split PDF files"
    )
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # Merge command
    merge_parser = subparsers.add_parser('merge', help='Merge multiple PDFs')
    merge_parser.add_argument('pdfs', nargs='+', help='PDF files to merge')
    merge_parser.add_argument('-o', '--output', required=True, help='Output PDF path')
    
    # Split command
    split_parser = subparsers.add_parser('split', help='Split PDF into pages')
    split_parser.add_argument('pdf', help='PDF file to split')
    split_parser.add_argument('-o', '--output', required=True, help='Output directory')
    
    args = parser.parse_args()
    
    if args.command == 'merge':
        merge_pdfs(args.pdfs, args.output)
    elif args.command == 'split':
        split_pdf(args.pdf, args.output)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

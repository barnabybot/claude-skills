#!/usr/bin/env python3
"""
Extract tables from a PDF file using pdfplumber.

This example demonstrates:
- Detecting tables in PDF pages
- Extracting table data
- Exporting to CSV format
- Handling multiple tables per page

Usage:
    python extract_tables.py document.pdf
    python extract_tables.py document.pdf --page 2
    python extract_tables.py document.pdf --output tables/
"""

import sys
import csv
import argparse
from pathlib import Path
import pdfplumber


def extract_tables(pdf_path: str, page_num: int = None, output_dir: str = None):
    """Extract tables from a PDF file."""
    
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    
    table_count = 0
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"File: {pdf_path}", file=sys.stderr)
        print(f"Pages: {len(pdf.pages)}", file=sys.stderr)
        print("-" * 40, file=sys.stderr)
        
        pages_to_process = [pdf.pages[page_num - 1]] if page_num else pdf.pages
        
        for page in pages_to_process:
            page_number = page.page_number
            tables = page.extract_tables()
            
            if not tables:
                continue
            
            print(f"Page {page_number}: Found {len(tables)} table(s)", file=sys.stderr)
            
            for table_idx, table in enumerate(tables, 1):
                table_count += 1
                
                if output_dir:
                    # Save to CSV
                    csv_path = output_path / f"page{page_number}_table{table_idx}.csv"
                    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        for row in table:
                            # Clean up None values
                            cleaned_row = [cell if cell else '' for cell in row]
                            writer.writerow(cleaned_row)
                    print(f"  Saved: {csv_path}", file=sys.stderr)
                else:
                    # Print to stdout
                    print(f"\n=== Page {page_number}, Table {table_idx} ===")
                    for row in table:
                        cleaned_row = [str(cell)[:20] if cell else '' for cell in row]
                        print(" | ".join(cleaned_row))
    
    print(f"\nTotal tables found: {table_count}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Extract tables from a PDF file"
    )
    parser.add_argument("pdf", help="Path to PDF file")
    parser.add_argument("-p", "--page", type=int, help="Extract from specific page only")
    parser.add_argument("-o", "--output", help="Output directory for CSV files")
    
    args = parser.parse_args()
    extract_tables(args.pdf, args.page, args.output)


if __name__ == "__main__":
    main()

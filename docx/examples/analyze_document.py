#!/usr/bin/env python3
"""
Analyze the structure of a Word document via OOXML.

This example demonstrates:
- Unpacking a .docx file (which is a ZIP archive)
- Reading document.xml structure
- Extracting comments
- Finding tracked changes

Usage:
    python analyze_document.py document.docx
"""

import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


# Word OOXML namespaces
NAMESPACES = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}


def get_text(element):
    """Extract text from a Word XML element."""
    texts = []
    for t in element.findall('.//w:t', NAMESPACES):
        if t.text:
            texts.append(t.text)
    return ''.join(texts)


def analyze_document(docx_path: str):
    """Analyze and print the structure of a Word document."""
    
    print(f"=== Document: {docx_path} ===\n")
    
    with zipfile.ZipFile(docx_path, 'r') as zf:
        # List contents
        print("=== Archive Contents ===")
        for name in sorted(zf.namelist()):
            info = zf.getinfo(name)
            print(f"  {name} ({info.file_size:,} bytes)")
        print()
        
        # Parse main document
        print("=== Document Structure ===")
        if 'word/document.xml' in zf.namelist():
            doc_xml = zf.read('word/document.xml')
            root = ET.fromstring(doc_xml)
            
            # Count paragraphs
            paragraphs = root.findall('.//w:p', NAMESPACES)
            print(f"Paragraphs: {len(paragraphs)}")
            
            # Count tables
            tables = root.findall('.//w:tbl', NAMESPACES)
            print(f"Tables: {len(tables)}")
            
            # Find tracked changes
            insertions = root.findall('.//w:ins', NAMESPACES)
            deletions = root.findall('.//w:del', NAMESPACES)
            print(f"Tracked insertions: {len(insertions)}")
            print(f"Tracked deletions: {len(deletions)}")
            print()
            
            # Show first few paragraphs
            print("=== First 5 Paragraphs ===")
            for i, para in enumerate(paragraphs[:5], 1):
                text = get_text(para)
                if text.strip():
                    preview = text[:60]
                    if len(text) > 60:
                        preview += "..."
                    print(f"  {i}. {preview}")
            print()
            
            # Show tracked changes detail
            if insertions or deletions:
                print("=== Tracked Changes ===")
                
                for ins in insertions[:5]:
                    author = ins.get(f'{{{NAMESPACES["w"]}}}author', 'Unknown')
                    text = get_text(ins)[:40]
                    print(f"  + INSERT ({author}): \"{text}\"")
                
                for del_ in deletions[:5]:
                    author = del_.get(f'{{{NAMESPACES["w"]}}}author', 'Unknown')
                    # Deletions use w:delText instead of w:t
                    texts = [t.text for t in del_.findall('.//w:delText', NAMESPACES) if t.text]
                    text = ''.join(texts)[:40]
                    print(f"  - DELETE ({author}): \"{text}\"")
                
                if len(insertions) > 5 or len(deletions) > 5:
                    print(f"  ... and {len(insertions) + len(deletions) - 10} more changes")
                print()
        
        # Check for comments
        if 'word/comments.xml' in zf.namelist():
            print("=== Comments ===")
            comments_xml = zf.read('word/comments.xml')
            comments_root = ET.fromstring(comments_xml)
            
            comments = comments_root.findall('.//w:comment', NAMESPACES)
            for comment in comments[:5]:
                author = comment.get(f'{{{NAMESPACES["w"]}}}author', 'Unknown')
                text = get_text(comment)[:50]
                print(f"  • {author}: \"{text}\"")
            
            if len(comments) > 5:
                print(f"  ... and {len(comments) - 5} more comments")
        else:
            print("=== Comments ===")
            print("  (no comments)")


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_document.py <document.docx>")
        print()
        print("This script analyzes a Word document's OOXML structure,")
        print("showing paragraphs, tables, tracked changes, and comments.")
        sys.exit(1)
    
    analyze_document(sys.argv[1])


if __name__ == "__main__":
    main()

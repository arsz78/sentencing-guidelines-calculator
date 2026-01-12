#!/usr/bin/env python3
"""
Extract section numbers from USSG PDFs and build an index.

This script analyzes all 553 PDF files to extract section numbers
(e.g., §2D1.1, §2B1.1) and maps them to page numbers.
"""

import pdfplumber
import json
import re
from pathlib import Path
from collections import defaultdict

# Regex patterns for section numbers
# Primary pattern: §2D1.1, §2B1.1, §1A1.1, etc.
SECTION_PATTERN = re.compile(r'§(\d[A-Z]\d+\.\d+[a-z]?)')

# Alternative pattern without § symbol (for cases where it's missing)
ALT_SECTION_PATTERN = re.compile(r'(?:^|\s)(\d[A-Z]\d+\.\d+[a-z]?)(?:\s|$|\.)')


def is_likely_primary_section(text_before, text_after, y_position, page_height):
    """
    Determine if a section number is likely a primary section header
    (as opposed to a cross-reference).

    Heuristics:
    - Near top of page (upper 40%)
    - At beginning of line or after minimal text
    - Followed by title-like text (capitalized words)
    """
    # Check vertical position (top 40% of page)
    if page_height and y_position:
        relative_position = y_position / page_height
        if relative_position > 0.40:  # Below top 40%
            return False

    # Check if at start of line or minimal text before
    if text_before and len(text_before.strip()) > 50:
        return False

    # Check if followed by title-like text
    if text_after:
        # Look for capitalized words (typical of section titles)
        title_words = re.findall(r'\b[A-Z][a-z]+\b', text_after[:100])
        if len(title_words) >= 2:
            return True

    return True  # Default to True if we can't determine


def extract_sections_from_pdf(pdf_path, page_number):
    """
    Extract section numbers from a single PDF.
    Returns a list of section numbers found in this PDF.
    """
    sections_found = set()

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_idx, page in enumerate(pdf.pages):
                # Extract text
                text = page.extract_text()
                if not text:
                    continue

                # Get page dimensions for position analysis
                page_height = page.height if hasattr(page, 'height') else None

                # Find all section matches
                lines = text.split('\n')
                for line_idx, line in enumerate(lines):
                    # Try primary pattern with § symbol
                    for match in SECTION_PATTERN.finditer(line):
                        section = match.group(1)

                        # Get context
                        text_before = line[:match.start()]
                        text_after = line[match.end():]

                        # Calculate approximate y position (top of page = 0)
                        # Estimate based on line position
                        estimated_y_ratio = line_idx / max(len(lines), 1)

                        # Check if this is likely a primary section
                        if is_likely_primary_section(
                            text_before,
                            text_after,
                            estimated_y_ratio,
                            1.0  # Normalized height
                        ):
                            sections_found.add(section)

                # Also check for sections without § symbol at line starts
                for line_idx, line in enumerate(lines):
                    line_stripped = line.strip()
                    if line_stripped:
                        alt_match = re.match(r'^(\d[A-Z]\d+\.\d+[a-z]?)', line_stripped)
                        if alt_match and line_idx < len(lines) * 0.3:  # Top 30% of page
                            sections_found.add(alt_match.group(1))

    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")

    return list(sections_found)


def build_section_index():
    """
    Build complete section-to-page mapping for all PDFs.
    """
    print("Building section index from 553 PDFs...")
    print("This will take 5-10 minutes...\n")

    section_to_pages = defaultdict(list)
    guidelines_dir = Path("Guidelines")

    # Check if directory exists
    if not guidelines_dir.exists():
        print(f"ERROR: Directory {guidelines_dir} not found!")
        return None

    # Process each PDF
    for i in range(1, 554):  # Pages 1-553
        pdf_path = guidelines_dir / f"GLMFull {i}.pdf"

        if not pdf_path.exists():
            print(f"WARNING: {pdf_path} not found, skipping...")
            continue

        # Extract sections from this PDF
        sections = extract_sections_from_pdf(pdf_path, i)

        # Add to index
        for section in sections:
            section_to_pages[section].append(i)

        # Progress indicator
        if i % 50 == 0:
            print(f"Processed {i}/553 PDFs... ({len(section_to_pages)} sections found so far)")

    print(f"\nExtraction complete!")
    print(f"Total sections found: {len(section_to_pages)}")

    # Sort page numbers for each section
    for section in section_to_pages:
        section_to_pages[section].sort()

    # Convert defaultdict to regular dict and sort by section
    sorted_index = dict(sorted(section_to_pages.items()))

    return sorted_index


def save_index(index, output_file="section-index.json"):
    """Save index to JSON file."""
    if index is None:
        print("ERROR: No index to save!")
        return False

    output_path = Path(output_file)

    try:
        with open(output_path, 'w') as f:
            json.dump(index, f, indent=2, sort_keys=True)

        print(f"\nSection index saved to: {output_path}")
        print(f"File size: {output_path.stat().st_size / 1024:.1f} KB")

        # Print sample sections
        print("\nSample sections found:")
        sample_count = 0
        for section, pages in sorted(index.items()):
            if sample_count < 20:
                page_list = ', '.join(map(str, pages[:5]))
                if len(pages) > 5:
                    page_list += f" ... ({len(pages)} total)"
                print(f"  §{section}: pages {page_list}")
                sample_count += 1

        return True

    except Exception as e:
        print(f"ERROR saving index: {e}")
        return False


def main():
    """Main execution function."""
    print("=" * 60)
    print("USSG Section Index Builder")
    print("=" * 60)
    print()

    # Build the index
    index = build_section_index()

    if index:
        # Save to file
        success = save_index(index)

        if success:
            print("\n" + "=" * 60)
            print("SUCCESS! Section index created.")
            print("=" * 60)
            return 0

    print("\n" + "=" * 60)
    print("FAILED to create section index.")
    print("=" * 60)
    return 1


if __name__ == "__main__":
    exit(main())

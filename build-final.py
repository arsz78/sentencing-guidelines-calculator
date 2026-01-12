#!/usr/bin/env python3
"""
Build the final complete HTML file with embedded PDFs and section index.

This script combines:
1. HTML template (guideline-viewer-template.html)
2. Section index (section-index.json)
3. PDF data (pdf-data.js)

Output: guideline-viewer-complete.html (~100MB)
"""

from pathlib import Path
import json


def read_file(file_path):
    """Read a file and return its contents."""
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"ERROR reading {file_path}: {e}")
        return None


def build_final_html():
    """Build the complete HTML file with all embedded data."""
    print("=" * 60)
    print("USSG Complete Viewer Builder")
    print("=" * 60)
    print()

    # Check that all required files exist
    required_files = {
        'template': Path('guideline-viewer-template.html'),
        'section_index': Path('section-index.json'),
        'pdf_data': Path('pdf-data.js')
    }

    for name, path in required_files.items():
        if not path.exists():
            print(f"ERROR: Required file not found: {path}")
            print(f"\nPlease run the following scripts first:")
            print(f"1. python3 build-section-index.py")
            print(f"2. python3 embed-pdfs.py")
            return None

    print("Reading template...")
    template = read_file(required_files['template'])
    if not template:
        return None

    print("Reading section index...")
    section_index_json = read_file(required_files['section_index'])
    if not section_index_json:
        return None

    print("Reading PDF data... (this may take a moment)")
    pdf_data_js = read_file(required_files['pdf_data'])
    if not pdf_data_js:
        return None

    print("\nBuilding final HTML...")

    # Create the section index JavaScript code
    section_index_code = f"const SECTION_INDEX = {section_index_json};"

    # Inject the section index
    final_html = template.replace(
        '// INJECT_SECTION_INDEX_HERE',
        section_index_code
    )

    # Inject the PDF data
    final_html = final_html.replace(
        '// INJECT_PDF_DATA_HERE',
        pdf_data_js
    )

    print("Assembly complete!")

    return final_html


def save_final_html(html_content, output_file="guideline-viewer-complete.html"):
    """Save the complete HTML file."""
    if html_content is None:
        print("ERROR: No content to save!")
        return False

    output_path = Path(output_file)

    try:
        print(f"\nWriting final file: {output_path}")
        print("This may take a moment...")

        with open(output_path, 'w') as f:
            f.write(html_content)

        file_size = output_path.stat().st_size
        print(f"\nFinal file saved: {output_path}")
        print(f"File size: {file_size / (1024*1024):.1f} MB")

        return True

    except Exception as e:
        print(f"ERROR saving file: {e}")
        return False


def main():
    """Main execution function."""
    # Build the complete HTML
    final_html = build_final_html()

    if final_html:
        # Save to file
        success = save_final_html(final_html)

        if success:
            print("\n" + "=" * 60)
            print("SUCCESS! Complete viewer created.")
            print("=" * 60)
            print("\nYou can now open guideline-viewer-complete.html in your browser.")
            print("\nFeatures:")
            print("  - Search by page number (1-553)")
            print("  - Search by section number (e.g., 2D1.1, 2B1.1)")
            print("  - Autocomplete for section search")
            print("  - Fully portable (works offline)")
            print("\nNote: Initial load may take 10-20 seconds due to file size.")
            return 0

    print("\n" + "=" * 60)
    print("FAILED to create complete viewer.")
    print("=" * 60)
    return 1


if __name__ == "__main__":
    exit(main())

#!/usr/bin/env python3
"""
Embed all PDFs as base64-encoded data.

This script reads all 553 PDF files and encodes them as base64 strings,
creating a JavaScript object that can be embedded in HTML.
"""

import base64
from pathlib import Path
import json


def encode_pdf(pdf_path):
    """Read PDF and return base64 encoded string."""
    try:
        with open(pdf_path, 'rb') as f:
            pdf_data = f.read()
        return base64.b64encode(pdf_data).decode('utf-8')
    except Exception as e:
        print(f"ERROR encoding {pdf_path}: {e}")
        return None


def build_pdf_data_js():
    """
    Create JavaScript file with all PDFs embedded as base64.
    Returns the generated JavaScript code.
    """
    print("=" * 60)
    print("USSG PDF Embedder")
    print("=" * 60)
    print("\nEncoding 553 PDFs as base64...")
    print("This will take 2-5 minutes...\n")

    guidelines_dir = Path("Guidelines")

    # Check if directory exists
    if not guidelines_dir.exists():
        print(f"ERROR: Directory {guidelines_dir} not found!")
        return None

    # Start building JavaScript object
    js_lines = ['const PDF_DATA = {']

    total_size = 0
    success_count = 0

    # Process each PDF
    for i in range(1, 554):  # Pages 1-553
        pdf_path = guidelines_dir / f"GLMFull {i}.pdf"

        if not pdf_path.exists():
            print(f"WARNING: {pdf_path} not found, skipping...")
            continue

        # Encode PDF
        encoded = encode_pdf(pdf_path)

        if encoded:
            # Add to JavaScript object (escape any quotes in base64 string)
            js_lines.append(f'  {i}: "{encoded}",')

            # Track stats
            file_size = pdf_path.stat().st_size
            total_size += file_size
            success_count += 1

            # Progress indicator
            if i % 50 == 0:
                print(f"Encoded {i}/553 PDFs... ({total_size / (1024*1024):.1f} MB raw, "
                      f"~{total_size * 1.33 / (1024*1024):.1f} MB base64)")

    # Close JavaScript object
    js_lines.append('};')

    print(f"\nEncoding complete!")
    print(f"Successfully encoded: {success_count}/553 PDFs")
    print(f"Total raw PDF size: {total_size / (1024*1024):.1f} MB")
    print(f"Estimated base64 size: {total_size * 1.33 / (1024*1024):.1f} MB")

    return '\n'.join(js_lines)


def save_pdf_data(js_code, output_file="pdf-data.js"):
    """Save JavaScript code to file."""
    if js_code is None:
        print("ERROR: No data to save!")
        return False

    output_path = Path(output_file)

    try:
        with open(output_path, 'w') as f:
            f.write(js_code)

        file_size = output_path.stat().st_size
        print(f"\nPDF data saved to: {output_path}")
        print(f"File size: {file_size / (1024*1024):.1f} MB")

        return True

    except Exception as e:
        print(f"ERROR saving file: {e}")
        return False


def main():
    """Main execution function."""
    # Build the JavaScript code
    js_code = build_pdf_data_js()

    if js_code:
        # Save to file
        success = save_pdf_data(js_code)

        if success:
            print("\n" + "=" * 60)
            print("SUCCESS! PDF data embedded.")
            print("=" * 60)
            print("\nNext step: Run build-final.py to create the complete HTML file.")
            return 0

    print("\n" + "=" * 60)
    print("FAILED to embed PDF data.")
    print("=" * 60)
    return 1


if __name__ == "__main__":
    exit(main())

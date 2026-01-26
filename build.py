#!/usr/bin/env python3
"""
Build script for Federal Sentencing Guidelines Calculator.
Inlines JSON data files into the HTML for complete offline functionality.
"""

import json
import re
from pathlib import Path


def main():
    # Paths
    base_dir = Path(__file__).parent
    data_dir = base_dir / "data"
    html_file = base_dir / "index.html"
    output_file = base_dir / "calculator.html"

    print("Building Federal Sentencing Guidelines Calculator...")

    # Read data files
    print("  Loading offense-guidelines.json...")
    with open(data_dir / "offense-guidelines.json", "r") as f:
        offense_data = json.load(f)

    print("  Loading chapter3-adjustments.json...")
    with open(data_dir / "chapter3-adjustments.json", "r") as f:
        chapter3_data = json.load(f)

    # Read HTML template
    print("  Loading index.html template...")
    with open(html_file, "r") as f:
        html_content = f.read()

    # Replace placeholder data with actual JSON
    # The placeholders are marked with comments like /*OFFENSE_DATA_PLACEHOLDER*/.../*END_OFFENSE_DATA*/

    offense_json = json.dumps(offense_data, indent=2)
    chapter3_json = json.dumps(chapter3_data, indent=2)

    # Replace OFFENSE_DATA using string find/replace to avoid regex escape issues
    start_marker = "/*OFFENSE_DATA_PLACEHOLDER*/"
    end_marker = "/*END_OFFENSE_DATA*/"
    start_idx = html_content.find(start_marker)
    end_idx = html_content.find(end_marker) + len(end_marker)
    if start_idx != -1 and end_idx != -1:
        html_content = (
            html_content[:start_idx] +
            f"{start_marker}{offense_json}{end_marker}" +
            html_content[end_idx:]
        )

    # Replace CHAPTER3_DATA
    start_marker = "/*CHAPTER3_DATA_PLACEHOLDER*/"
    end_marker = "/*END_CHAPTER3_DATA*/"
    start_idx = html_content.find(start_marker)
    end_idx = html_content.find(end_marker) + len(end_marker)
    if start_idx != -1 and end_idx != -1:
        html_content = (
            html_content[:start_idx] +
            f"{start_marker}{chapter3_json}{end_marker}" +
            html_content[end_idx:]
        )

    # Write output file
    print(f"  Writing {output_file.name}...")
    with open(output_file, "w") as f:
        f.write(html_content)

    # Calculate file sizes
    html_size = html_file.stat().st_size / 1024
    output_size = output_file.stat().st_size / 1024

    print()
    print("Build complete!")
    print(f"  Input:  {html_file.name} ({html_size:.1f} KB)")
    print(f"  Output: {output_file.name} ({output_size:.1f} KB)")
    print()
    print("The calculator.html file is now ready for offline use.")
    print("Open it directly in a web browser - no server required.")


if __name__ == "__main__":
    main()

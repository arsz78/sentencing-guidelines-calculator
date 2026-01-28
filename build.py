#!/usr/bin/env python3
"""
Build script for Federal Sentencing Guidelines Calculator.
Inlines JSON data files into the HTML for complete offline functionality.
"""

import json
from pathlib import Path


def main():
    # Paths
    base_dir = Path(__file__).parent
    data_dir = base_dir / "data"
    html_file = base_dir / "index.html"
    output_file = base_dir / "calculator.html"

    print("Building Federal Sentencing Guidelines Calculator...")

    # Find all year directories in data/
    year_dirs = sorted([d for d in data_dir.iterdir() if d.is_dir() and d.name.isdigit()])

    if not year_dirs:
        print("  Error: No year directories found in data/")
        return

    # Build combined data structure keyed by year
    all_offense_data = {}
    all_chapter3_data = {}

    for year_dir in year_dirs:
        year = year_dir.name
        print(f"  Loading {year} guidelines...")

        # Load and merge all offense files for this year
        offenses_dir = year_dir / "offenses"
        year_offenses = {}
        if offenses_dir.exists():
            offense_files = sorted(offenses_dir.glob("*.json"))
            for offense_file in offense_files:
                print(f"    Loading offenses/{offense_file.name}...")
                with open(offense_file, "r") as f:
                    file_data = json.load(f)
                    year_offenses.update(file_data)

        all_offense_data[year] = year_offenses
        print(f"    Loaded {len(year_offenses)} offense guideline(s)")

        # Load chapter3 adjustments for this year
        chapter3_file = year_dir / "chapter3-adjustments.json"
        if chapter3_file.exists():
            print(f"    Loading chapter3-adjustments.json...")
            with open(chapter3_file, "r") as f:
                all_chapter3_data[year] = json.load(f)
        else:
            print(f"    Warning: No chapter3-adjustments.json found for {year}")
            all_chapter3_data[year] = {}

    print(f"  Total: {len(year_dirs)} guideline year(s) loaded")

    # Read HTML template
    print("  Loading index.html template...")
    with open(html_file, "r") as f:
        html_content = f.read()

    # Replace placeholder data with actual JSON
    offense_json = json.dumps(all_offense_data, indent=2)
    chapter3_json = json.dumps(all_chapter3_data, indent=2)

    # Replace OFFENSE_DATA
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

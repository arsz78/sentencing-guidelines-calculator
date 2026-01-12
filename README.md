# Szekely Guidelines Project

**Version 0.0.2** - Enhanced Guideline Viewer (2026-01-12)

A collection of tools for working with the United States Sentencing Guidelines Manual (2025 edition).

## Overview

This project provides web-based tools to assist federal criminal defense attorneys with sentencing calculations and guideline analysis. The flagship tool is an enhanced, portable guidelines viewer with section-based search and navigation.

## Current Features

### Enhanced Guidelines Viewer v0.0.2

A fully-featured, portable PDF viewer for the 2025 U.S. Sentencing Guidelines Manual.

**Key Features:**
- **Dual Search Modes**: Search by page number (1-553) OR section number (e.g., §2D1.1, §2B1.1)
- **Section Autocomplete**: Type-ahead suggestions for all 299 guideline sections
- **Page Navigation**: Previous/Next buttons and arrow key support for flipping through pages
- **Completely Portable**: Single 98MB HTML file with all 553 PDFs embedded (works offline)
- **Fast**: No server requests, instant page switching after initial load

**Available Versions:**
- **`guideline-viewer-complete.html`** (98 MB) - Recommended. Complete standalone version with all PDFs embedded
- **`guideline-viewer.html`** (5 KB) - Original lightweight version requiring local PDF files

**Usage (Complete Version):**
1. Open `guideline-viewer-complete.html` in your web browser
2. Wait 10-20 seconds for initial load (one-time, then instant)
3. **Page Mode**: Enter page number 1-553 and click View
4. **Section Mode**: Click "Section Number" toggle, enter section (e.g., 2D1.1) and click View
5. **Navigate**: Use Previous/Next buttons or arrow keys to flip through pages
6. **Autocomplete**: Start typing a section number to see suggestions

**Sample Sections:**
- `2D1.1` - Drug Offenses (primary drug guideline)
- `2B1.1` - Theft, Property Destruction, and Fraud
- `2A1.1` - First Degree Murder
- `2A2.1` - Assault with Intent to Commit Murder
- `2K2.1` - Unlawful Possession or Trafficking in Firearms

**Build Scripts** (for rebuilding or updating):
```bash
python3 build-section-index.py  # Extract sections from PDFs (5-10 min)
python3 embed-pdfs.py           # Encode PDFs as base64 (2-5 min)
python3 build-final.py          # Build complete HTML (1 min)
```

## Planned Features

Future calculator tools:
- Drug weight conversion calculator
- Fraud guideline walk-through calculator
- Drug guideline walk-through calculator
- VOSR (Violation of Supervised Release) guideline table calculator
- Sentencing table generator
- Gun guideline calculator

## Requirements

**For Complete Viewer:**
- A modern web browser (Chrome, Firefox, Safari, Edge)
- 100MB+ available RAM for browser
- No internet connection required after download

**For Development/Rebuilding:**
- Python 3.9+
- `pdfplumber` library (`pip3 install pdfplumber`)
- Guidelines directory containing PDF files

## License

MIT License - Copyright (c) 2026 Andrew Szekely

See [LICENSE](LICENSE) file for details.

## About

Created to streamline federal sentencing calculations and guideline lookups for legal professionals.

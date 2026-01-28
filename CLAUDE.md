# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Federal Sentencing Guidelines Calculator - an offline, single-file HTML calculator for determining Total Offense Level under the U.S. Sentencing Guidelines Manual.

**Version:** 0.0.3
**Coverage:** 98 offense guidelines across all 18 Chapter 2 categories (2A-2X)
**Architecture:** Year-based data structure with chapter-organized JSON files, build system merges into standalone 338 KB HTML file

## Build Command

```bash
python3 build.py
```

This inlines JSON data from `data/` into `index.html` and outputs `calculator.html` (the standalone offline version).

## Architecture

**Year-based data structure**: Data is organized by guideline year to support the "one book rule" (defendant benefits from whichever year produces lower offense level).

```
data/
  TEMPLATE.json         # Template with field documentation for contributors
  2025/
    offenses/
      2A.json           # Chapter 2A - Offenses Against the Person (15 guidelines)
      2B.json           # Chapter 2B - Property (10 guidelines)
      2C.json           # Chapter 2C - Public Officials (4 guidelines)
      2D.json           # Chapter 2D - Drugs (10 guidelines)
      2E.json           # Chapter 2E - Criminal Enterprises (6 guidelines)
      2G.json           # Chapter 2G - Commercial Sex Acts (6 guidelines)
      2H.json           # Chapter 2H - Individual Rights (5 guidelines)
      2J.json           # Chapter 2J - Administration of Justice (5 guidelines)
      2K.json           # Chapter 2K - Firearms (10 guidelines)
      2L.json           # Chapter 2L - Immigration (4 guidelines)
      2M.json           # Chapter 2M - National Defense/WMD (7 guidelines)
      2N.json           # Chapter 2N - Food/Drugs/Agricultural (2 guidelines)
      2P.json           # Chapter 2P - Prisons (3 guidelines)
      2Q.json           # Chapter 2Q - Environment (4 guidelines)
      2R.json           # Chapter 2R - Antitrust (1 guideline)
      2S.json           # Chapter 2S - Money Laundering (2 guidelines)
      2T.json           # Chapter 2T - Tax (7 guidelines)
      2X.json           # Chapter 2X - Other Offenses (7 guidelines)
    chapter3-adjustments.json
  2026/                 # Future year - copy and modify as needed
    ...
Guidelines/
  2025/
    GLMFull *.pdf       # Source PDFs for 2025 manual (553 files)
  2026/                 # Future year
    ...
```

**Offense JSON structure** (`data/{year}/offenses/*.json`):

Each chapter file contains multiple guidelines:
- `baseOffenseQuestions`: Decision tree for base offense level (uses `yesNext`/`noNext` for branching, `yesResult`/`noResult` for terminal nodes)
- `specificOffenseCharacteristics`: Sequential adjustments with `type: "select"` or `type: "yesno"`
- See `data/TEMPLATE.json` for complete field documentation and examples

**Build process**: `build.py` finds all year directories, merges ALL offense files within each year (2A.json, 2B.json, etc.), and outputs a combined structure keyed by year. Currently loads 98 guidelines into calculator.html.

**UI flow**: Mode selection (Wizard/Checklist) → Year selection → Offense selection → `base` → `soc` → `ch3` → `result`

**Parsing**: `parse_guidelines.py` automates extraction from PDF sources (71% success rate, 98/149 guidelines). Failed parses logged in `parse_failures.log` for manual review.

## Adding or Modifying Offenses

1. **Locate the chapter file**: Find `data/{year}/offenses/{chapter}.json` (e.g., `2K.json` for firearms)
2. **Reference the template**: See `data/TEMPLATE.json` for all field types with examples and documentation
3. **Edit the JSON**: Add/modify guidelines in the chapter file
   - Remove all `_comment` fields from your JSON
   - Reference source PDFs as `Guidelines/{year}/GLMFull {page}.pdf`
4. **Rebuild**: Run `python3 build.py` to regenerate calculator.html
5. **Test**: Open calculator.html in browser and verify your changes

**Note:** If creating a new chapter file, ensure it's in `data/{year}/offenses/` and follows the structure in TEMPLATE.json. The build script will automatically detect and merge it.

## Adding a New Guideline Year

1. Copy the previous year's data directory: `cp -r data/2025 data/2026`
2. Copy the PDFs: `cp -r Guidelines/2025 Guidelines/2026` (replace with new year's PDFs)
3. Update JSON files for any changes in the new guidelines
4. Update `pdfReference` paths in JSON files to point to new year
5. Run `python3 build.py`

## Data Sources

Guideline data sourced from U.S. Sentencing Guidelines Manual PDFs in `Guidelines/{year}/` folder:

- **2025 Guidelines Manual**: 553 PDF files (GLMFull 1.pdf through GLMFull 553.pdf)
- **Automated parsing**: `parse_guidelines.py` extracts offense data from PDFs
- **Success rate**: 98 of 149 guidelines parsed successfully (71%)
- **Failed parses**: See `parse_failures.log` for list of 43 guidelines needing manual review

**Key sections**:
- Chapter 2 Offenses: Pages vary by chapter (see `pdfReference` in each JSON)
- Chapter 3 Role: Pages 333-334
- Chapter 3 Obstruction: Pages 340-342
- Chapter 3 Acceptance: Pages 357-358

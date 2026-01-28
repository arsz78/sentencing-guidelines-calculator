# Federal Sentencing Guidelines Calculator

An offline calculator for determining the Total Offense Level under the 2025 U.S. Sentencing Guidelines Manual.

**Current Version:** 0.0.3

## Overview

This calculator helps users determine the **Total Offense Level** by:

1. Selecting an offense and calculating the base offense level
2. Applying specific offense characteristics (SOCs)
3. Applying Chapter 3 adjustments (role, obstruction, acceptance)
4. Displaying the final offense level with a breakdown

**Note:** This version calculates offense level only. Criminal History calculation is not included - users must determine their Criminal History Category separately and use the Sentencing Table to find the guideline range.

## Coverage

**98 offense guidelines** across all 18 Chapter 2 categories:

- **2A** - Offenses Against the Person (15 guidelines)
- **2B** - Offenses Involving Property (10 guidelines)
- **2C** - Offenses Involving Public Officials (4 guidelines)
- **2D** - Drug Offenses (10 guidelines)
- **2E** - Offenses Involving Criminal Enterprises (6 guidelines)
- **2G** - Offenses Involving Commercial Sex Acts (6 guidelines)
- **2H** - Offenses Involving Individual Rights (5 guidelines)
- **2J** - Administration of Justice (5 guidelines)
- **2K** - Firearms Offenses (10 guidelines)
- **2L** - Immigration Offenses (4 guidelines)
- **2M** - National Defense and WMD (7 guidelines)
- **2N** - Food, Drugs, Agricultural Products (2 guidelines)
- **2P** - Prisons and Correctional Facilities (3 guidelines)
- **2Q** - Environmental Offenses (4 guidelines)
- **2R** - Antitrust Offenses (1 guideline)
- **2S** - Money Laundering (2 guidelines)
- **2T** - Tax and Related Offenses (7 guidelines)
- **2X** - Other Offenses (7 guidelines)

## Usage

### Quick Start

1. Open `calculator.html` in any web browser
2. Choose a mode:
   - **Wizard Mode**: Step-by-step guided flow (default)
   - **Checklist Mode**: See all questions at once
3. Select an offense from the dropdown
4. Answer questions and view the final offense level with breakdown

### Building from Source

The `index.html` file contains the full application with embedded data. To rebuild after modifying the JSON data files:

```bash
python3 build.py
```

This creates `calculator.html` with the latest data inlined.

## File Structure

```
/Users/andy/Claude/guidelines/
├── Guidelines/
│   └── 2025/                        # 553 PDF files from 2025 Guidelines Manual
├── data/
│   ├── TEMPLATE.json                # Template with field documentation
│   └── 2025/
│       ├── offenses/
│       │   ├── 2A.json              # Chapter 2A offenses
│       │   ├── 2B.json              # Chapter 2B offenses
│       │   └── ... (2C-2X)          # All 18 chapters
│       └── chapter3-adjustments.json
├── index.html                       # Main calculator app (source)
├── calculator.html                  # Built calculator (standalone, 338 KB)
├── build.py                         # Build script (merges all data by year)
├── parse_guidelines.py              # Automated PDF parser
└── README.md                        # This file
```

## Test Cases

The calculator has been verified against these test scenarios:

| Scenario | Base | SOCs | Ch.3 | Total |
|----------|------|------|------|-------|
| Prohibited person + stolen firearm + acceptance | 14 | +2 | -3 | **13** |
| Prohibited person w/semiauto + stolen + acceptance | 20 | +2 | -3 | **19** |
| 2+ prior COV/CSO + 5 firearms + obstruction | 24 | +2 | +2 | **28** |

## Data Sources

All guideline data is sourced from the **2025 U.S. Sentencing Guidelines Manual** (November 1, 2025):

- **2K2.1 Firearms**: Pages 237-250
- **Chapter 3 Part B (Role)**: Pages 333-334
- **Chapter 3 Part C (Obstruction)**: Pages 340-342
- **Chapter 3 Part E (Acceptance)**: Pages 357-358

## Disclaimer

This calculator is for **educational purposes only**. It does not constitute legal advice. Consult a qualified attorney for actual sentencing matters. The calculator may not account for all possible enhancements, departures, or unique case circumstances.

## Architecture

The calculator uses a **year-based data structure** to support the "one book rule" (defendant benefits from whichever guideline year produces the lower offense level):

- **Year directories**: `data/2025/`, `data/2026/` (future)
- **Chapter-organized**: Each Chapter 2 category in separate JSON file for maintainability
- **Build-time merging**: `build.py` finds all years, merges chapter files, inlines into HTML
- **Template-driven**: `data/TEMPLATE.json` documents all field types for contributors

## Future Enhancements

See [ROADMAP.md](ROADMAP.md) for detailed development plan. Potential additions:

- Enhanced response states (flag for review, considered but N/A)
- Exportable decision trail (copy-to-clipboard summary)
- Criminal History Category calculator
- Sentencing Table lookup
- PDF viewer integration

## License

This project is provided as-is for educational use.

# Federal Sentencing Guidelines Calculator

An offline calculator for determining the Total Offense Level under the 2025 U.S. Sentencing Guidelines Manual.

## Overview

This calculator helps users determine the **Total Offense Level** by:

1. Selecting an offense and calculating the base offense level
2. Applying specific offense characteristics (SOCs)
3. Applying Chapter 3 adjustments (role, obstruction, acceptance)
4. Displaying the final offense level with a breakdown

**Note:** This version calculates offense level only. Criminal History calculation is not included - users must determine their Criminal History Category separately and use the Sentencing Table to find the guideline range.

## Currently Supported Offenses

- **2K2.1** - Unlawful Receipt, Possession, or Transportation of Firearms or Ammunition

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
├── Guidelines/                      # 553 PDF files from 2025 Guidelines Manual
├── data/
│   ├── offense-guidelines.json      # Offense rules (2K2.1 Firearms)
│   └── chapter3-adjustments.json    # Chapter 3 adjustments
├── index.html                       # Main calculator app (source)
├── calculator.html                  # Built calculator (standalone)
├── build.py                         # Build script
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

## Future Enhancements

Potential additions for future versions:

- Additional offense guidelines (2D1.1 drugs, 2B1.1 fraud, 2L1.2 reentry)
- Criminal History Category calculator
- Sentencing Table lookup
- PDF viewer integration

## License

This project is provided as-is for educational use.

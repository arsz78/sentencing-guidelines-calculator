# Development Roadmap

This file guides future development sessions. Edit priorities and add notes as needed.

## Current Status

- **Version**: 0.0.1
- **Completed**: §2K2.1 Firearms offense calculator with Chapter 3 adjustments
- **Architecture**: Standalone offline HTML with data-driven JSON configuration

---

## Priority 1: Additional Offense Guidelines

### §2D1.1 - Drug Trafficking
- [ ] Extract base offense levels from drug quantity tables
- [ ] Add specific offense characteristics
- [ ] Handle multiple drug types and conversions
- **Notes**: Complex due to drug quantity tables and marijuana equivalency

### §2B1.1 - Fraud/Theft
- [ ] Base offense levels based on loss amount
- [ ] Specific offense characteristics (victims, sophisticated means, etc.)
- **Notes**: Loss tables have many tiers

### §2L1.2 - Unlawfully Entering or Remaining
- [ ] Base offense levels
- [ ] Prior deportation enhancements
- **Notes**: Relatively straightforward

---

## Priority 2: Criminal History Calculator

- [ ] Count prior sentences
- [ ] Apply recency rules
- [ ] Calculate Criminal History Points
- [ ] Determine Criminal History Category (I-VI)
- **Notes**: Complex rules around concurrent sentences, related cases, etc.

---

## Priority 3: Sentencing Table Integration

- [ ] Implement the sentencing table lookup
- [ ] Display guideline range (months)
- [ ] Show Zone A/B/C/D information
- **Notes**: Requires both offense level and criminal history category

---

## Priority 4: UI Enhancements

- [ ] PDF viewer integration (open relevant guideline sections)
- [ ] Print-friendly summary
- [ ] Save/load calculations
- [ ] Mobile-responsive improvements

---

## Backlog / Ideas

- Multiple count calculations (§3D1.2-1.5)
- Departures and variances information
- Career offender provisions (§4B1.1)
- Armed career criminal provisions
- Export calculations to PDF

---

## Session Notes

_Add notes here for the next coding session:_

```
Next session focus:

Blockers/questions:

Other notes:

```

---

## Data Sources

All guideline data from **2025 U.S. Sentencing Guidelines Manual** (November 1, 2025):
- PDFs located in `Guidelines/` folder (553 files)
- Key sections extracted to `data/*.json` files

## Build Commands

```bash
# Rebuild calculator after editing data files
python3 build.py

# Output: calculator.html (standalone offline file)
```

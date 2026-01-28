# Development Roadmap

This file guides future development sessions. Edit priorities and add notes as needed.

## Current Status

- **Version**: 0.0.3
- **Completed**: 98 offense guidelines across all 18 Chapter 2 categories with Chapter 3 adjustments, Wizard/Checklist mode toggle
- **Architecture**: Year-based data structure with chapter-organized JSON files, build system merges all data into standalone offline HTML

---

## Design Philosophy

**Core insight**: The target users are experienced federal defense attorneys who know the guidelines cold as well as newer attorneys who need more guidance in working througn the guidelines. The problem isn't lack of knowledge—it's that under time pressure (especially in correctional facility visits), steps get skipped. This tool is a **checklist**, not a calculator. Think "Checklist Manifesto" for sentencing guidelines.

**Key principles**:

- Ensure every applicable adjustment is *considered*, not just computed
- Create a documented trail of what was reviewed and why
- Support both learning (guided) and expert (checklist) workflows
- Offline-first for use in correctional facilities without internet

---

## Priority 1: UX Mode Toggle (Wizard vs Checklist) ✅ COMPLETED

The current "wizard" flow steps through questions one at a time. Experienced attorneys may prefer to see everything at once.

### Wizard Mode

- Step-by-step guided flow
- Good for unfamiliar guidelines or training
- System prevents skipping steps

### Checklist Mode

- [x] Display all base offense questions at once
- [x] Display all SOCs simultaneously with current selections visible
- [x] Allow marking items in any order
- [x] Visual indicator for "not yet reviewed" vs "reviewed and answered"
- [x] Same calculation logic, different presentation

**Status**: ✅ Implemented in v0.0.2. Mode toggle added at start screen; both modes use same JSON data structure. Checklist mode extracts base levels from decision tree and presents as flat selectable list.

---

## Priority 2: Enhanced Response States

Currently SOCs have binary yes/no or select options. Add richer states to support the checklist workflow:

### For all SOC questions

- [ ] Add "Needs Review / Flagged" state (distinct from yes/no/select)
- [ ] Add "Considered but N/A" state (distinct from "No")
- [ ] Visual differentiation: unanswered vs answered vs flagged
- [ ] Prevent final calculation if any items still flagged

### Exportable Decision Trail

- [ ] Generate summary showing each SOC considered
- [ ] Format: "§2K2.1(b)(1) Firearm count: 3-7 firearms (+2) — APPLIED"
- [ ] Format: "§2K2.1(b)(2) Sporting purpose: Considered, not applicable"
- [ ] Format: "§2K2.1(b)(4) Stolen/serial: FLAGGED FOR REVIEW"
- [ ] Copy-to-clipboard or print-friendly output

---

## Priority 3: Comprehensive Chapter 2 Coverage ✅ COMPLETED

Add all Chapter 2 offense guidelines to validate architecture and provide comprehensive coverage.

- [x] Year-based data directory structure (`data/2025/`)
- [x] Chapter-organized offense files (`offenses/2A.json`, `offenses/2B.json`, etc.)
- [x] Build system merges all chapter files by year
- [x] Parse all 18 Chapter 2 categories from source PDFs
- [x] 98 offense guidelines successfully parsed and integrated
- [x] Template file documents all field types for contributors

**Status**: ✅ Implemented in v0.0.3. Architecture validated across diverse guideline types:
- Simple guidelines (2R1.1 Antitrust)
- Complex decision trees (2A1.1 Murder, 2K2.1 Firearms)
- Drug quantity tables (2D1.1)
- Loss amount tables (2B1.1)
- Immigration enhancements (2L1.2)

**Known Issues**: 43 guidelines failed automated parsing (71% success rate) due to PDF text extraction issues. These require manual review or improved extraction logic. See `parse_failures.log` for details.

---

## Priority 4: Data Quality Review

With 98 guidelines now integrated, focus shifts to validation and refinement.

- [ ] Manual review of high-priority guidelines (most common offenses)
- [ ] Fix 43 failed parses from automated extraction
- [ ] Validate calculations against known case examples
- [ ] Add test cases for each guideline category
- [ ] Verify PDF references link correctly
- **Notes**: Priority guidelines for review: 2K2.1 (firearms), 2D1.1 (drugs), 2B1.1 (fraud), 2L1.2 (immigration), 2G2.2 (child exploitation)

---

## Priority 5: Criminal History Calculator

- [ ] Count prior sentences
- [ ] Apply recency rules
- [ ] Calculate Criminal History Points
- [ ] Determine Criminal History Category (I-VI)
- **Notes**: Complex rules around concurrent sentences, related cases, etc. Defer until offense level calculator is solid.

---

## Priority 6: Sentencing Table Integration

- [ ] Implement the sentencing table lookup
- [ ] Display guideline range (months)
- [ ] Show Zone A/B/C/D information
- **Notes**: Requires both offense level and criminal history category

---

## Priority 7: UI Enhancements

- [ ] PDF viewer integration (open relevant guideline sections)
- [ ] Print-friendly summary with decision trail
- [ ] Save/load calculations (localStorage for offline use)
- [ ] Mobile-responsive improvements

---

## Backlog / Ideas

- Multiple count calculations (§3D1.2-1.5)
- Departures and variances information
- Career offender provisions (§4B1.1)
- Armed career criminal provisions
- Export calculations to PDF
- Dark mode for low-light facility environments

---

## Session Notes

*Add notes here for the next coding session:*

### v0.0.3 Achievements
- ✅ Expanded from 1 to 98 offense guidelines
- ✅ Reorganized architecture: year-based dirs, chapter-organized files
- ✅ Build system merges all chapters
- ✅ Automated PDF parsing (71% success rate)
- ✅ Created TEMPLATE.json for contributors

### Next session focus:
- Data quality: Review and fix high-priority guidelines (2K2.1, 2D1.1, 2B1.1, 2L1.2)
- Enhanced response states (flagged, considered but N/A)
- Exportable decision trail (copy-to-clipboard)

### Blockers/questions resolved:
- ✅ Export format: Plain text or PDF export
- ✅ Flagged items: Allow provisional result (need to present "known unknowns" to clients)
- ✅ Architecture scales: Validated with 98 guidelines across 18 chapters

### Other notes:
- Target user: experienced attorney, knows guidelines, needs process discipline
- Environment: offline, correctional facility, time-pressured
- Calculator size: 338 KB standalone (works in any browser)

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

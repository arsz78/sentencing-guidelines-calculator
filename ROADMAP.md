# Development Roadmap

This file guides future development sessions. Edit priorities and add notes as needed.

## Current Status

- **Version**: 0.0.2
- **Completed**: §2K2.1 Firearms offense calculator with Chapter 3 adjustments, Wizard/Checklist mode toggle
- **Architecture**: Standalone offline HTML with data-driven JSON configuration

---

## Design Philosophy

**Core insight**: The target users are experienced federal defense attorneys who know the guidelines cold as well as newer attorneys who need more guidance in working througn the guidelines. The problem isn't lack of knowledge—it's that under time pressure (especially in correctional facility visits), steps get skipped. This tool is a **checklist**, not a calculator. Think "Checklist Manifesto" for sentencing guidelines.

**Key principles**:

- Ensure every applicable adjustment is *considered*, not just computed
- Create a documented trail of what was reviewed and why
- Support both learning (guided) and expert (checklist) workflows
- Offline-first for use in correctional facilities without internet

---

## Priority 1: UX Mode Toggle (Wizard vs Checklist)

The current "wizard" flow steps through questions one at a time. Experienced attorneys may prefer to see everything at once.

### Wizard Mode (current)

- Step-by-step guided flow
- Good for unfamiliar guidelines or training
- System prevents skipping steps

### Checklist Mode (new)

- [x] Display all base offense questions at once
- [x] Display all SOCs simultaneously with current selections visible
- [x] Allow marking items in any order
- [x] Visual indicator for "not yet reviewed" vs "reviewed and answered"
- [x] Same calculation logic, different presentation

**Implementation**: Mode toggle added at start screen; both modes use same JSON data structure. Checklist mode extracts base levels from decision tree and presents as flat selectable list.

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

## Priority 3: Validate Architecture with Second Guideline

Add one more guideline to confirm the data structure scales before building out many more.

### §2L1.2 - Unlawfully Entering or Remaining

- [ ] Base offense levels
- [ ] Prior deportation enhancements
- [ ] Validate JSON structure works for different guideline patterns
- **Notes**: Relatively straightforward; good test case

### Then consider

- §2B1.1 - Fraud/Theft (loss tables)
- §2D1.1 - Drug Trafficking (quantity tables, conversions)

---

## Priority 4: Additional Offense Guidelines

### §2D1.1 - Drug Trafficking

- [ ] Extract base offense levels from drug quantity tables
- [ ] Add specific offense characteristics
- [ ] Handle multiple drug types and conversions
- **Notes**: Complex due to drug quantity tables and drug equivalency table (will require math!)

### §2B1.1 - Fraud/Theft

- [ ] Base offense levels based on loss amount
- [ ] Specific offense characteristics (victims, sophisticated means, etc.)
- **Notes**: Loss tables have many tiers

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

Next session focus:

- Consider implementing Checklist Mode toggle as proof of concept
- Or add §2L1.2 to validate architecture scales

Blockers/questions:

- What's the preferred export format for decision trail? (plain text, PDF, copy-paste?) Plan text or PDF export
- Should flagged items block calculation entirely, or allow "provisional" result? Allow provision, we often have to present the "known unknowns" to clients

Other notes:

- Target user: experienced attorney, knows guidelines, needs process discipline
- Environment: offline, correctional facility, time-pressured

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

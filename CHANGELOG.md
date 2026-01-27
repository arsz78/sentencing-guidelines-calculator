# Changelog

All notable changes to this project will be documented in this file.

## [0.0.2] - 2026-01-27

### Added
- **Checklist Mode**: New UX mode that displays all questions at once
  - Toggle between Wizard Mode (step-by-step) and Checklist Mode on start screen
  - Collapsible sections for Base Offense Level, SOCs, and Chapter 3 adjustments
  - Review indicators show which items have been answered (green checkmark)
  - Sticky status bar with running offense level and review progress count
  - Allows marking items in any order
  - Same calculation logic as Wizard Mode

### Changed
- Start screen now includes mode selection before offense selection
- Base offense levels in Checklist Mode presented as flat selectable list (extracted from decision tree)

## [0.0.1] - 2025-01-25

### Added
- Interactive offense level calculator with Q&A flow
- Support for §2K2.1 (Unlawful Receipt, Possession, or Transportation of Firearms)
  - All base offense levels from §2K2.1(a)(1)-(8)
  - Specific offense characteristics (b)(1)-(7): firearms count, destructive devices, stolen/serial, conversion devices, trafficking, export/felony
- Chapter 3 adjustments
  - §3B1.1/3B1.2 Role in the Offense (+4 to -4)
  - §3C1.1 Obstruction of Justice (+2)
  - §3E1.1 Acceptance of Responsibility (-2 or -3)
- Running offense level display during calculation
- Back button to change previous answers
- Full breakdown of adjustments in results
- Build script to create standalone offline HTML
- Data-driven JSON configuration for offense rules

### Technical
- Vanilla HTML/CSS/JavaScript (no frameworks)
- Single-file output for complete offline functionality
- JSON data inlined during build process

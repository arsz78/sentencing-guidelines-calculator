# Changelog

All notable changes to this project will be documented in this file.

## [0.0.3] - 2026-01-27

### Added
- **Comprehensive Chapter 2 Offense Coverage**: Expanded from 1 to 98 offense guidelines across all 18 chapters
  - **2A** - Offenses Against the Person (15 guidelines)
  - **2B** - Offenses Involving Property (10 guidelines)
  - **2C** - Offenses Involving Public Officials (4 guidelines)
  - **2D** - Drug Offenses (10 guidelines)
  - **2E** - Offenses Involving Criminal Enterprises (6 guidelines)
  - **2G** - Offenses Involving Commercial Sex Acts and Sexual Exploitation of Minors (6 guidelines)
  - **2H** - Offenses Involving Individual Rights (5 guidelines)
  - **2J** - Offenses Involving the Administration of Justice (5 guidelines)
  - **2K** - Firearms Offenses (10 guidelines)
  - **2L** - Immigration Offenses (4 guidelines)
  - **2M** - Offenses Involving National Defense and Weapons of Mass Destruction (7 guidelines)
  - **2N** - Offenses Involving Food, Drugs, Agricultural Products, Consumer Products (2 guidelines)
  - **2P** - Offenses Involving Prisons and Correctional Facilities (3 guidelines)
  - **2Q** - Offenses Involving the Environment (4 guidelines)
  - **2R** - Antitrust Offenses (1 guideline)
  - **2S** - Money Laundering and Monetary Transaction Reporting (2 guidelines)
  - **2T** - Tax, Money Laundering, and Certain Other Offenses (7 guidelines)
  - **2X** - Other Offenses (7 guidelines)

### Changed
- **Architecture Evolution**: Reorganized data structure for scalability
  - Year-based directory structure (`data/{year}/`)
  - Chapter-based offense files (`offenses/2A.json`, `offenses/2B.json`, etc.)
  - Build system now merges all chapter files and supports multiple guideline years
  - Single template file (`data/TEMPLATE.json`) documents all field types for contributors

### Technical
- Automated parsing from PDF source guidelines (71% success rate)
- Build output now includes 98 offense guidelines (up from 1)
- Calculator size: 338 KB (fully standalone)

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

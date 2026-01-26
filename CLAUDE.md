# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Federal Sentencing Guidelines Calculator - an offline, single-file HTML calculator for determining Total Offense Level under the 2025 U.S. Sentencing Guidelines Manual. Currently supports §2K2.1 (Firearms offenses).

## Build Command

```bash
python3 build.py
```

This inlines JSON data from `data/` into `index.html` and outputs `calculator.html` (the standalone offline version).

## Architecture

**Data-driven question flow**: The calculator uses JSON configuration files to drive an interactive Q&A interface:

- `data/offense-guidelines.json` - Defines offense-specific rules with:
  - `baseOffenseQuestions`: Decision tree for determining base offense level (uses `yesNext`/`noNext` for branching, `yesResult`/`noResult` for terminal nodes)
  - `specificOffenseCharacteristics`: Sequential adjustments with `type: "select"` or `type: "yesno"`

- `data/chapter3-adjustments.json` - Universal Chapter 3 adjustments (role, obstruction, acceptance) applied after offense-specific calculations

**Build process**: `build.py` replaces placeholder markers (`/*OFFENSE_DATA_PLACEHOLDER*/.../*END_OFFENSE_DATA*/`) in `index.html` with actual JSON data to create the standalone `calculator.html`.

**UI flow phases**: `start` → `base` → `soc` → `ch3` → `result`

## Adding New Offenses

1. Add offense entry to `data/offense-guidelines.json` following the §2K2.1 structure
2. Reference source PDFs in `Guidelines/` folder (named `GLMFull {page}.pdf`)
3. Run `python3 build.py` to regenerate calculator

## Data Sources

Guideline data sourced from 2025 U.S. Sentencing Guidelines Manual PDFs in `Guidelines/` folder:
- §2K2.1 Firearms: Pages 237-250
- Chapter 3 Role: Pages 333-334
- Chapter 3 Obstruction: Pages 340-342
- Chapter 3 Acceptance: Pages 357-358

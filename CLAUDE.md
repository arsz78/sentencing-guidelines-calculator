# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This repository contains the United States Sentencing Guidelines Manual (2025 edition) from the U.S. Sentencing Commission, split into 553 individual PDF files. The owner is a federal criminal defense attorney with sub-novice coding skills who needs assistance with sentencing calculations and guideline analysis.

**Current Version**: v0.0.2 (2026-01-12)

## Content Structure

### Guidelines Directory
Contains 553 PDF files named `GLMFull 1.pdf` through `GLMFull 553.pdf`, representing sequential pages or sections of the 2025 U.S. Sentencing Guidelines Manual.

### Built Artifacts
- **`guideline-viewer-complete.html`** (98 MB) - Complete portable viewer with all 553 PDFs embedded as base64
- **`section-index.json`** (12 KB) - Mapping of 299 guideline sections to page numbers
- **`pdf-data.js`** (97.7 MB) - All PDFs encoded as base64 JavaScript object

### Build Scripts
- **`build-section-index.py`** - Extracts section numbers from PDFs using pdfplumber
- **`embed-pdfs.py`** - Encodes all PDFs as base64 for embedding
- **`build-final.py`** - Combines template, section index, and PDF data into complete HTML
- **`guideline-viewer-template.html`** - HTML/CSS/JS template for the enhanced viewer

### Key Guideline Components
The Guidelines Manual contains:
- **Chapter 1**: Introduction, Authority, and General Application Principles
- **Chapter 2**: Offense Conduct (organized by type)
  - Part A: Offenses Against the Person (homicide, assault, sexual abuse, kidnapping)
  - Part B: Basic Economic Offenses (theft, fraud, burglary, robbery, counterfeiting)
  - Part C: Public Officials and Election Campaign Violations
  - Part D: Drug Offenses and Narco-Terrorism (§2D1.1 is the primary drug guideline)
  - Part E: Criminal Enterprises and Racketeering
- **Additional chapters** cover adjustments, criminal history, sentencing procedures, and policy statements

### Citation Format
When referencing guidelines, use the standard abbreviated form:
- Guidelines: `USSG §2D1.1`
- Policy statements: `USSG §6A1.1, p.s.`
- Application notes: `USSG §2B1.1, comment. (n.1)`
- Background: `USSG §2B1.1, comment. (backg'd.)`
- Appendices: `USSG App. C`

## Completed Features

### Enhanced Guideline Viewer (v0.0.2)
A fully-featured, portable HTML viewer with:
- **Dual search modes**: Page number (1-553) or section number (e.g., §2D1.1)
- **Section autocomplete**: 299 guideline sections indexed and searchable
- **Page navigation**: Previous/Next buttons and arrow key support
- **Completely portable**: Single 98MB HTML file works offline
- **Section-to-page mapping**: Automatically extracted from PDFs using text analysis

**Key Sections Indexed:**
- Drug offenses: §2D1.1 and related
- Fraud/theft: §2B1.1 and related
- Violent crimes: §2A1.1-§2A6.2
- Firearms: §2K2.1 and related
- 299 total sections mapped

## Future Development Priorities

The owner has identified these calculator tools for future development:
1. Drug weight conversion calculator
2. Fraud guideline walk-through calculator
3. Drug guideline walk-through calculator
4. VOSR (Violation of Supervised Release) guideline table
5. Sentencing table generator
6. Gun guideline calculator

## Working with PDFs

When the owner asks about specific guidelines or calculations:
1. **For section lookups**: Use the section-index.json file to find page numbers
2. **For direct access**: Use Read tool to access relevant PDF files by number (Guidelines/GLMFull {number}.pdf)
3. The PDFs contain the authoritative text of the guidelines
4. Cross-reference between PDFs may be necessary as guidelines often reference other sections
5. Drug calculations typically involve §2D1.1 (in Part D of Chapter 2)
6. Fraud calculations typically involve §2B1.1 (in Part B of Chapter 2)

## Rebuilding the Viewer

To rebuild the complete viewer after PDF updates:
```bash
python3 build-section-index.py  # Extract sections (5-10 min)
python3 embed-pdfs.py           # Encode PDFs (2-5 min)
python3 build-final.py          # Build HTML (1 min)
```

Requires: Python 3.9+, pdfplumber library

## Important Context

The owner is an excellent federal criminal defense attorney but has limited coding experience. When building tools or calculators:
- Prioritize clear, simple interfaces
- Provide explanations of calculations showing guideline section references
- Assume the owner understands sentencing law deeply but may need technical guidance
- Focus on practical utility for legal practice (sentencing memos, client consultations, court filings)

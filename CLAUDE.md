# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This repository contains the United States Sentencing Guidelines Manual (2025 edition) from the U.S. Sentencing Commission, split into 553 individual PDF files. The owner is a federal criminal defense attorney with sub-novice coding skills who needs assistance with sentencing calculations and guideline analysis.

## Content Structure

### Guidelines Directory
Contains 553 PDF files named `GLMFull 1.pdf` through `GLMFull 553.pdf`, representing sequential pages or sections of the 2025 U.S. Sentencing Guidelines Manual.

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

## Project Goals (from ideas.md)

The owner has identified these development priorities:
1. Drug weight conversion calculator
2. Fraud guideline walk-through calculator
3. Drug guideline walk-through calculator
4. VOSR (Victim of State-Sponsored Removals) guideline table
5. Sentencing table generator
6. Gun guideline calculator

## Working with PDFs

When the owner asks about specific guidelines or calculations:
1. Use Read tool to access relevant PDF files by number
2. The PDFs contain the authoritative text of the guidelines
3. Cross-reference between PDFs may be necessary as guidelines often reference other sections
4. Drug calculations typically involve §2D1.1 (in Part D of Chapter 2)
5. Fraud calculations typically involve §2B1.1 (in Part B of Chapter 2)

## Important Context

The owner is an excellent federal criminal defense attorney but has limited coding experience. When building tools or calculators:
- Prioritize clear, simple interfaces
- Provide explanations of calculations showing guideline section references
- Assume the owner understands sentencing law deeply but may need technical guidance
- Focus on practical utility for legal practice (sentencing memos, client consultations, court filings)

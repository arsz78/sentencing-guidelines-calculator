#!/usr/bin/env python3
"""
PDF to JSON Parser for U.S. Sentencing Guidelines Chapter 2.

Converts guideline PDFs into structured JSON for the sentencing calculator.
Uses Claude API for interpreting complex legal decision trees.

Usage:
    python3 parse_guidelines.py                    # Process all Chapter 2 sections
    python3 parse_guidelines.py --section 2K2.1   # Process specific section
    python3 parse_guidelines.py --scan            # Only scan and list sections
    python3 parse_guidelines.py --dry-run         # Extract text but don't call API
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

try:
    import pdfplumber
except ImportError:
    print("Error: pdfplumber not installed. Run: pip install pdfplumber")
    sys.exit(1)

try:
    import anthropic
except ImportError:
    anthropic = None

try:
    from pydantic import BaseModel, ValidationError
except ImportError:
    BaseModel = None
    ValidationError = None


# ============================================================================
# Configuration
# ============================================================================

PDF_DIR = Path(__file__).parent / "Guidelines" / "2025"
OUTPUT_DIR = Path(__file__).parent / "data" / "2025" / "offenses"
TEMPLATE_PATH = Path(__file__).parent / "data" / "TEMPLATE.json"

# Section pattern: §2X.Y or §2XY.Z format
SECTION_PATTERN = re.compile(r'§(2[A-Z][0-9]?\.[0-9]+)')

# Pattern for actual section headers (section number followed by title)
# e.g., "§2K2.1. Unlawful Receipt, Possession..."
SECTION_HEADER_PATTERN = re.compile(
    r'^§(2[A-Z][0-9]?\.[0-9]+)\.\s+([A-Z][^()\n]{10,})',
    re.MULTILINE
)

# Model to use for interpretation
CLAUDE_MODEL = "claude-sonnet-4-20250514"


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class SectionLocation:
    """Location of a guideline section in the PDFs."""
    section: str
    title: str
    start_pdf: int  # PDF number (1-indexed)
    start_page: int  # Page within PDF (0-indexed)
    end_pdf: Optional[int] = None
    end_page: Optional[int] = None


@dataclass
class ExtractedText:
    """Text extracted from a guideline section."""
    section: str
    title: str
    full_text: str
    base_offense_text: str
    soc_text: str
    cross_references_text: str
    pdf_reference: str


# ============================================================================
# Section Mapper - Scans PDFs to find section locations
# ============================================================================

class SectionMapper:
    """Scans PDFs to build a map of section locations."""

    def __init__(self, pdf_dir: Path):
        self.pdf_dir = pdf_dir
        self.sections: dict[str, SectionLocation] = {}

    def scan_all(self, verbose: bool = True) -> dict[str, SectionLocation]:
        """Scan all PDFs and build section map."""
        pdf_files = sorted(
            self.pdf_dir.glob("GLMFull *.pdf"),
            key=lambda p: int(p.stem.split()[-1])
        )

        if verbose:
            print(f"Scanning {len(pdf_files)} PDF files...")

        current_section = None

        for pdf_path in pdf_files:
            pdf_num = int(pdf_path.stem.split()[-1])

            try:
                with pdfplumber.open(pdf_path) as pdf:
                    for page_num, page in enumerate(pdf.pages):
                        text = page.extract_text() or ""

                        # Look for actual section headers (not just mentions)
                        # Pattern: §2X.Y. Title Text (with period after section number)
                        for match in SECTION_HEADER_PATTERN.finditer(text):
                            section = match.group(1)
                            title = match.group(2).strip()

                            # Only process Chapter 2 sections (2A-2X)
                            if not section.startswith('2'):
                                continue

                            # Skip if this looks like a cross-reference or [Deleted] section
                            if '[Deleted]' in title or 'deleted' in title.lower():
                                continue

                            # Close previous section
                            if current_section and current_section in self.sections:
                                loc = self.sections[current_section]
                                if loc.end_pdf is None:
                                    loc.end_pdf = pdf_num
                                    loc.end_page = page_num

                            # Start new section (or update if we found a better location)
                            if section not in self.sections:
                                self.sections[section] = SectionLocation(
                                    section=section,
                                    title=title,
                                    start_pdf=pdf_num,
                                    start_page=page_num
                                )
                                current_section = section

                                if verbose:
                                    print(f"  Found §{section} at PDF {pdf_num}: {title[:50]}...")

            except Exception as e:
                print(f"  Warning: Error reading {pdf_path.name}: {e}")

        return self.sections

    def _extract_title(self, text: str, start_pos: int) -> str:
        """Extract section title from text after the section number."""
        # Look for title on same or next line
        remaining = text[start_pos:start_pos + 500]

        # Find text up to next section or paragraph break
        lines = remaining.split('\n')
        title_parts = []

        for line in lines[:3]:  # Check first 3 lines
            line = line.strip()
            if not line:
                break
            if line.startswith('('):  # Start of subsection
                break
            if SECTION_PATTERN.search(line):  # Another section
                break
            # Remove common artifacts
            line = re.sub(r'\s+', ' ', line)
            if line.startswith('.'):
                line = line[1:].strip()
            title_parts.append(line)

        title = ' '.join(title_parts).strip()
        # Clean up
        title = re.sub(r'\s+', ' ', title)
        title = title[:200]  # Limit length
        return title

    def get_chapter_sections(self, chapter: str) -> list[SectionLocation]:
        """Get all sections for a chapter (e.g., '2K' returns 2K1.x, 2K2.x)."""
        return [
            loc for section, loc in sorted(self.sections.items())
            if section.startswith(chapter)
        ]


# ============================================================================
# Text Extractor - Extracts and segments section text
# ============================================================================

class TextExtractor:
    """Extracts text from PDFs for a specific section."""

    def __init__(self, pdf_dir: Path):
        self.pdf_dir = pdf_dir

    def extract_section(self, location: SectionLocation) -> ExtractedText:
        """Extract full text for a section."""
        texts = []
        pdf_reference = f"Guidelines/2025/GLMFull {location.start_pdf}.pdf"

        # Determine PDF range to read
        start_pdf = location.start_pdf
        end_pdf = location.end_pdf or start_pdf + 5  # Default to checking 5 PDFs

        for pdf_num in range(start_pdf, min(end_pdf + 1, start_pdf + 10)):
            pdf_path = self.pdf_dir / f"GLMFull {pdf_num}.pdf"
            if not pdf_path.exists():
                continue

            try:
                with pdfplumber.open(pdf_path) as pdf:
                    for page_num, page in enumerate(pdf.pages):
                        # Skip pages before our section starts
                        if pdf_num == start_pdf and page_num < location.start_page:
                            continue

                        text = page.extract_text() or ""

                        # Check if we've hit the next section
                        next_section_match = SECTION_PATTERN.search(text)
                        if next_section_match:
                            found_section = next_section_match.group(1)
                            if found_section != location.section:
                                # Include text up to next section
                                text = text[:next_section_match.start()]
                                texts.append(text)
                                break

                        texts.append(text)

                        # Check for end markers
                        if location.end_pdf and pdf_num == location.end_pdf:
                            if location.end_page and page_num >= location.end_page:
                                break

            except Exception as e:
                print(f"  Warning: Error reading PDF {pdf_num}: {e}")

        full_text = '\n'.join(texts)

        # Segment the text
        base_text, soc_text, xref_text = self._segment_text(full_text)

        return ExtractedText(
            section=location.section,
            title=location.title,
            full_text=full_text,
            base_offense_text=base_text,
            soc_text=soc_text,
            cross_references_text=xref_text,
            pdf_reference=pdf_reference
        )

    def _segment_text(self, text: str) -> tuple[str, str, str]:
        """Segment text into base offense, SOC, and cross-references."""
        # Find subsection markers
        base_start = text.find('(a)')
        soc_start = text.find('(b)')
        xref_start = text.find('(c)')

        # Handle case where sections are labeled differently
        if base_start == -1:
            base_match = re.search(r'Base Offense Level', text, re.IGNORECASE)
            base_start = base_match.start() if base_match else 0

        if soc_start == -1:
            soc_match = re.search(r'Specific Offense Characteristics?', text, re.IGNORECASE)
            soc_start = soc_match.start() if soc_match else -1

        if xref_start == -1:
            xref_match = re.search(r'Cross Reference', text, re.IGNORECASE)
            xref_start = xref_match.start() if xref_match else -1

        # Extract segments
        if soc_start > base_start:
            base_text = text[base_start:soc_start]
        else:
            base_text = text[base_start:] if base_start >= 0 else text

        if soc_start >= 0:
            if xref_start > soc_start:
                soc_text = text[soc_start:xref_start]
            else:
                soc_text = text[soc_start:]
        else:
            soc_text = ""

        if xref_start >= 0:
            xref_text = text[xref_start:]
        else:
            xref_text = ""

        return base_text.strip(), soc_text.strip(), xref_text.strip()


# ============================================================================
# LLM Interpreter - Uses Claude to convert legal text to JSON
# ============================================================================

# System prompt for interpreting base offense levels
BASE_OFFENSE_PROMPT = '''You are a legal text parser converting U.S. Sentencing Guidelines into structured JSON.

Given the base offense level text from a sentencing guideline section, create a decision tree of yes/no questions that leads to the correct base offense level.

The guidelines use "apply the greatest" logic - multiple conditions can be true, and the highest applicable level is used. Your decision tree should check conditions in order from highest to lowest level.

Output format:
```json
{
  "baseOffenseQuestions": [
    {
      "id": "base_1",
      "text": "Question text ending with ?",
      "type": "yesno",
      "yesNext": "base_1a",  // or yesResult
      "noNext": "base_2"     // or noResult
    },
    {
      "id": "base_1a",
      "text": "Follow-up question?",
      "type": "yesno",
      "yesResult": { "baseLevel": 26, "description": "Brief description" },
      "noNext": "base_1b"
    }
  ]
}
```

Rules:
1. Every question must have id, text, type:"yesno"
2. Every path must terminate in a yesResult or noResult with baseLevel and description
3. Use yesNext/noNext to branch to other questions
4. Start with id "base_1"
5. Questions should be clear, unambiguous yes/no questions
6. Include all legal qualifications and thresholds in the question text
7. The decision tree must be complete - every possible scenario covered'''

SOC_PROMPT = '''You are a legal text parser converting U.S. Sentencing Guidelines into structured JSON.

Given the specific offense characteristics (SOC) text from a sentencing guideline section, create structured adjustments.

Output format:
```json
{
  "specificOffenseCharacteristics": [
    {
      "id": "soc_description",
      "text": "Question about the characteristic?",
      "type": "select",
      "reference": "§2X.Y(b)(1)",
      "options": [
        { "label": "No/None", "adjustment": 0 },
        { "label": "Condition for +2", "adjustment": 2 },
        { "label": "Condition for +4", "adjustment": 4 }
      ]
    },
    {
      "id": "soc_another",
      "text": "Yes/no question about characteristic?",
      "type": "yesno",
      "reference": "§2X.Y(b)(2)",
      "yesEffect": { "adjustment": 2, "description": "Why this applies" },
      "noEffect": { "adjustment": 0 }
    }
  ]
}
```

Rules:
1. Use type "select" for multiple levels/options, "yesno" for binary
2. Always include reference to the subsection (e.g., "§2K2.1(b)(1)")
3. Include all tiers/levels as separate options for select types
4. For yesno with minimum level: {"adjustment": X, "minimumLevel": Y}
5. For yesno that sets a fixed level: {"setLevel": X, "description": "..."}
6. Add "condition" field if the characteristic only applies under certain conditions
7. Order characteristics as they appear in the guidelines (b)(1), (b)(2), etc.'''


class LLMInterpreter:
    """Uses Claude API to interpret legal text into structured JSON."""

    def __init__(self):
        if anthropic is None:
            raise RuntimeError("anthropic package not installed. Run: pip install anthropic")

        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY environment variable not set")

        self.client = anthropic.Anthropic(api_key=api_key)

    def interpret_base_offense(self, text: str, section: str) -> dict:
        """Convert base offense text to decision tree."""
        response = self.client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=4096,
            system=BASE_OFFENSE_PROMPT,
            messages=[{
                "role": "user",
                "content": f"Section: §{section}\n\nBase Offense Level Text:\n{text}"
            }]
        )

        return self._parse_json_response(response.content[0].text)

    def interpret_soc(self, text: str, section: str) -> dict:
        """Convert SOC text to adjustments list."""
        response = self.client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=4096,
            system=SOC_PROMPT,
            messages=[{
                "role": "user",
                "content": f"Section: §{section}\n\nSpecific Offense Characteristics Text:\n{text}"
            }]
        )

        return self._parse_json_response(response.content[0].text)

    def _parse_json_response(self, text: str) -> dict:
        """Extract and parse JSON from response."""
        # Try to find JSON in code blocks
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))

        # Try to parse entire response as JSON
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Try to find JSON object in text
        brace_start = text.find('{')
        if brace_start >= 0:
            # Find matching closing brace
            depth = 0
            for i, char in enumerate(text[brace_start:]):
                if char == '{':
                    depth += 1
                elif char == '}':
                    depth -= 1
                    if depth == 0:
                        json_str = text[brace_start:brace_start + i + 1]
                        return json.loads(json_str)

        raise ValueError(f"Could not parse JSON from response: {text[:500]}")


# ============================================================================
# Validator - Checks decision tree integrity
# ============================================================================

class Validator:
    """Validates generated JSON for decision tree integrity."""

    def validate(self, data: dict, section: str) -> list[str]:
        """Validate a section's JSON structure. Returns list of errors."""
        errors = []

        if section not in data:
            return [f"Section {section} not found in data"]

        section_data = data[section]

        # Validate base offense questions
        if "baseOffenseQuestions" in section_data:
            errors.extend(self._validate_decision_tree(
                section_data["baseOffenseQuestions"],
                section
            ))
        else:
            errors.append(f"{section}: Missing baseOffenseQuestions")

        # Validate SOC
        if "specificOffenseCharacteristics" in section_data:
            errors.extend(self._validate_soc(
                section_data["specificOffenseCharacteristics"],
                section
            ))

        return errors

    def _validate_decision_tree(self, questions: list, section: str) -> list[str]:
        """Validate decision tree has proper structure."""
        errors = []
        ids = {q["id"] for q in questions}

        # Check base_1 exists
        if "base_1" not in ids:
            errors.append(f"{section}: Decision tree must start with 'base_1'")

        # Check all references exist
        for q in questions:
            for key in ["yesNext", "noNext"]:
                if key in q and q[key] not in ids:
                    errors.append(f"{section}: {q['id']}.{key} references non-existent '{q[key]}'")

            # Check terminal nodes have results
            if "yesNext" not in q and "yesResult" not in q:
                errors.append(f"{section}: {q['id']} has no yesNext or yesResult")
            if "noNext" not in q and "noResult" not in q:
                errors.append(f"{section}: {q['id']} has no noNext or noResult")

        # Check reachability (BFS from base_1)
        reachable = set()
        to_visit = ["base_1"]
        while to_visit:
            current = to_visit.pop(0)
            if current in reachable:
                continue
            reachable.add(current)

            for q in questions:
                if q["id"] == current:
                    for key in ["yesNext", "noNext"]:
                        if key in q and q[key] not in reachable:
                            to_visit.append(q[key])

        unreachable = ids - reachable
        for uid in unreachable:
            errors.append(f"{section}: Question '{uid}' is not reachable from base_1")

        return errors

    def _validate_soc(self, socs: list, section: str) -> list[str]:
        """Validate SOC structure."""
        errors = []

        for soc in socs:
            if "id" not in soc:
                errors.append(f"{section}: SOC missing 'id' field")
                continue

            soc_id = soc["id"]

            if "type" not in soc:
                errors.append(f"{section}: {soc_id} missing 'type' field")
            elif soc["type"] == "select":
                if "options" not in soc or not soc["options"]:
                    errors.append(f"{section}: {soc_id} (select) missing options")
            elif soc["type"] == "yesno":
                if "yesEffect" not in soc:
                    errors.append(f"{section}: {soc_id} (yesno) missing yesEffect")
                if "noEffect" not in soc:
                    errors.append(f"{section}: {soc_id} (yesno) missing noEffect")

        return errors


# ============================================================================
# Main Parser - Orchestrates the parsing process
# ============================================================================

class GuidelinesParser:
    """Main parser that orchestrates PDF to JSON conversion."""

    def __init__(self, pdf_dir: Path = PDF_DIR, output_dir: Path = OUTPUT_DIR):
        self.pdf_dir = pdf_dir
        self.output_dir = output_dir
        self.mapper = SectionMapper(pdf_dir)
        self.extractor = TextExtractor(pdf_dir)
        self.validator = Validator()
        self.interpreter: Optional[LLMInterpreter] = None

    def scan_sections(self) -> dict[str, SectionLocation]:
        """Scan PDFs and return section map."""
        return self.mapper.scan_all()

    def parse_section(self, section: str, dry_run: bool = False) -> dict:
        """Parse a single section and return JSON structure."""
        # Find section location
        if section not in self.mapper.sections:
            self.mapper.scan_all(verbose=False)

        if section not in self.mapper.sections:
            raise ValueError(f"Section {section} not found in PDFs")

        location = self.mapper.sections[section]
        print(f"\nParsing §{section}: {location.title}")

        # Extract text
        print("  Extracting text from PDFs...")
        extracted = self.extractor.extract_section(location)

        if dry_run:
            print("  [DRY RUN] Would call Claude API with extracted text")
            print(f"  Base offense text length: {len(extracted.base_offense_text)} chars")
            print(f"  SOC text length: {len(extracted.soc_text)} chars")
            return {"_dry_run": True, "extracted": extracted}

        # Initialize interpreter if needed
        if self.interpreter is None:
            self.interpreter = LLMInterpreter()

        # Interpret with LLM
        print("  Interpreting base offense levels...")
        base_result = self.interpreter.interpret_base_offense(
            extracted.base_offense_text,
            section
        )

        print("  Interpreting specific offense characteristics...")
        soc_result = self.interpreter.interpret_soc(
            extracted.soc_text,
            section
        ) if extracted.soc_text else {"specificOffenseCharacteristics": []}

        # Build final structure
        result = {
            section: {
                "title": extracted.title,
                "section": section,
                "pdfReference": extracted.pdf_reference,
                **base_result,
                **soc_result
            }
        }

        # Validate
        print("  Validating structure...")
        errors = self.validator.validate(result, section)
        if errors:
            print("  Validation warnings:")
            for error in errors:
                print(f"    - {error}")
        else:
            print("  Validation passed!")

        return result

    def parse_chapter(self, chapter: str, dry_run: bool = False) -> dict:
        """Parse all sections in a chapter (e.g., '2K')."""
        if not self.mapper.sections:
            self.mapper.scan_all()

        sections = self.mapper.get_chapter_sections(chapter)
        if not sections:
            raise ValueError(f"No sections found for chapter {chapter}")

        print(f"\nParsing {len(sections)} sections in Chapter {chapter}")

        combined = {}
        for location in sections:
            try:
                result = self.parse_section(location.section, dry_run)
                if not dry_run:
                    combined.update(result)
            except Exception as e:
                print(f"  Error parsing {location.section}: {e}")

        return combined

    def save_chapter(self, chapter: str, data: dict):
        """Save chapter data to JSON file."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        output_path = self.output_dir / f"{chapter}.json"

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"\nSaved to {output_path}")


# ============================================================================
# CLI Entry Point
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Parse U.S. Sentencing Guidelines PDFs to JSON"
    )
    parser.add_argument(
        "--section", "-s",
        help="Parse a specific section (e.g., 2K2.1)"
    )
    parser.add_argument(
        "--chapter", "-c",
        help="Parse an entire chapter (e.g., 2K)"
    )
    parser.add_argument(
        "--scan", action="store_true",
        help="Only scan PDFs and list found sections"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Extract text but don't call Claude API"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file path (default: data/2025/offenses/{chapter}.json)"
    )

    args = parser.parse_args()

    # Initialize parser
    guidelines_parser = GuidelinesParser()

    # Scan mode
    if args.scan:
        sections = guidelines_parser.scan_sections()
        print(f"\nFound {len(sections)} Chapter 2 sections")

        # Group by chapter
        chapters: dict[str, list] = {}
        for section in sorted(sections.keys()):
            chapter = section[:2]  # e.g., "2K" from "2K2.1"
            if chapter not in chapters:
                chapters[chapter] = []
            chapters[chapter].append(section)

        for chapter in sorted(chapters.keys()):
            print(f"\n{chapter} ({len(chapters[chapter])} sections):")
            for section in chapters[chapter]:
                loc = sections[section]
                print(f"  §{section}: {loc.title[:60]}...")
        return

    # Section mode
    if args.section:
        result = guidelines_parser.parse_section(args.section, args.dry_run)
        if not args.dry_run:
            # Determine output path
            chapter = args.section[:2]
            output_path = Path(args.output) if args.output else OUTPUT_DIR / f"{chapter}.json"

            # Load existing file if it exists
            existing = {}
            if output_path.exists():
                with open(output_path) as f:
                    existing = json.load(f)

            # Merge and save
            existing.update(result)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(existing, f, indent=2)
            print(f"\nSaved to {output_path}")
        return

    # Chapter mode
    if args.chapter:
        result = guidelines_parser.parse_chapter(args.chapter, args.dry_run)
        if not args.dry_run:
            guidelines_parser.save_chapter(args.chapter, result)
        return

    # Default: parse all Chapter 2 sections
    print("Parsing all Chapter 2 sections...")
    print("Use --scan to see available sections first")
    print("Use --section 2K2.1 to parse a specific section")
    print("Use --chapter 2K to parse a specific chapter")
    print("Use --dry-run to test without API calls")


if __name__ == "__main__":
    main()

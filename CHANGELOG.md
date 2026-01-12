# Changelog

All notable changes to the Szekely Guidelines Project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.2] - 2026-01-12

### Added
- **Enhanced Guideline Viewer** with full feature set
  - Section-based search: Look up guidelines by section number (e.g., §2D1.1, §2B1.1)
  - Page-based search: Direct navigation to any of 553 pages
  - Autocomplete dropdown: Type-ahead suggestions for all 299 indexed sections
  - Page navigation controls: Previous/Next buttons for flipping through consecutive pages
  - Keyboard shortcuts: Arrow keys (← →) for quick page navigation
  - Completely portable: Single 98MB HTML file with all PDFs embedded as base64
  - Offline functionality: Works without internet connection after download
  - Section index: Automatically extracted mapping of 299 guideline sections to page numbers

- **Build System**
  - `build-section-index.py`: Extracts section numbers from PDFs using pdfplumber and text analysis
  - `embed-pdfs.py`: Encodes all 553 PDFs as base64 for embedding in HTML
  - `build-final.py`: Combines template, section index, and PDF data into complete viewer
  - `guideline-viewer-template.html`: Modular HTML/CSS/JS template for easy updates

- **Documentation**
  - Comprehensive README.md with usage instructions
  - Updated CLAUDE.md with project structure and build instructions
  - Enhanced ideas.md tracking completed and planned features
  - CHANGELOG.md (this file) for version history

- **Generated Artifacts**
  - `guideline-viewer-complete.html` (98 MB): Complete standalone viewer
  - `section-index.json` (12 KB): Section-to-page mapping
  - `pdf-data.js` (97.7 MB): All PDFs encoded as base64

### Technical Details
- Total sections indexed: 299
- Total PDF pages: 553
- Section extraction accuracy: High (with heuristics for primary sections vs. cross-references)
- Browser compatibility: Chrome, Firefox, Safari, Edge (modern versions)
- Initial load time: 10-20 seconds (one-time, then instant navigation)

### Known Limitations
- Large file size (98MB) requires modern browser with adequate memory
- Initial page load can take 10-20 seconds
- Section extraction is automated but may miss some obscure sections
- Requires modern browser (no IE support)

## [0.0.1] - 2026-01-11

### Added
- Initial project structure
- Basic guideline viewer (`guideline-viewer.html`)
  - Simple page number navigation (1-553)
  - Loads PDFs from local Guidelines directory
  - Clean, modern UI
- 553 PDF files of 2025 U.S. Sentencing Guidelines Manual
- Basic project documentation
- MIT License

### Features (v0.0.1)
- Page number entry (1-553)
- PDF display in iframe
- Input validation
- Enter key support
- Auto-focus on load

---

## Future Releases

### Planned for v0.1.0
- Enhanced section navigation with subsections (e.g., §2D1.1(a))
- "Related sections" suggestions
- Bookmarks/favorites functionality
- Print-friendly page mode

### Planned for v1.0.0
- Calculator Tools Suite:
  - Drug weight conversion calculator
  - Fraud guideline walk-through calculator
  - Drug guideline walk-through calculator
  - VOSR (Violation of Supervised Release) table
  - Sentencing table generator
  - Gun guideline calculator

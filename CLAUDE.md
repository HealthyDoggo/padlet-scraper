# Padlet Scraper Project

## Project Overview

This tool scrapes Padlets from a provided link and converts them into structured, readable data types. The primary use case is for students/professionals who store their employer projects and experiences in a Padlet over time, enabling them to convert this data into starter content for personal statements, CVs, and other professional documents.

## Padlet Structure

### Visual Hierarchy
- **Padlet** (top level)
  - **Columns** (sections with headers)
    - **Posts** (individual entries with subject and body)

### HTML Structure Details

#### Sections/Columns
- Top-level `<section>` elements represent rows/columns
- Section example HTML:
  ```html
  <section id="section-321330921"
           data-id="321330921"
           data-rank="1757458616"
           class="relative flex-none flex flex-col first:!ms-auto last:!me-auto surface-section"
           style="width: 272px; min-height: 290px;"
           data-drop-target-for-element="true">
  ```
- Section headers use: `data-testid="sectionTitleText"`

#### Posts
- Post wrappers use: `data-testid="surfacePost"`
- Post subject uses: `data-pw="postSubject"`
- Post body uses: `data-pw="postBody"`
- Note: Each post also contains a section for the like button, so section elements alone cannot uniquely identify columns

## Technology Stack

- **Web Scraping**: nodriver (Python library for browser automation)
- **Language**: Python 3.11
- **Data Models**: Pydantic for structured data validation

## Data Flow

1. **Input**: Padlet URL
2. **Scraping**: Use nodriver to load page and extract structured data
3. **Parsing**: Extract sections (columns) and posts from HTML
4. **Output**: Structured data (JSON/Python objects) with:
   - Section titles
   - Posts containing:
     - Subject
     - Body content
5. **Future**: Convert to AI-ready prompts (not implemented yet)

## Project Structure

```
/
├── CLAUDE.md              # This file - project context
├── README.md              # User-facing documentation
├── requirements.txt       # Python dependencies
├── padlet_scraper/        # Main package
│   ├── __init__.py
│   ├── models.py          # Data models (Padlet, Section, Post)
│   ├── scraper.py         # nodriver scraping logic
│   └── utils.py           # Helper functions
└── examples/              # Example usage scripts
    └── scrape_example.py
```

## Implementation Notes

### Scraping Strategy
1. Use nodriver to navigate to Padlet URL
2. Wait for dynamic content to load (Padlets use JavaScript)
3. Extract all sections using `data-testid="sectionTitleText"`
4. For each section, find posts using `data-testid="surfacePost"`
5. For each post, extract:
   - Subject: `data-pw="postSubject"`
   - Body: `data-pw="postBody"`

### Key Challenges
- Padlets are dynamic/JavaScript-heavy (hence nodriver vs requests)
- Need to handle various Padlet layouts (column, grid, stream, etc.)
- Posts may contain rich media (images, videos, links) - initially focus on text

### Future Enhancements
- Support for extracting images and attachments
- Convert to AI-ready prompts for CV/personal statement generation
- Handle different Padlet layouts (wall, canvas, timeline)
- Export to multiple formats (JSON, Markdown, PDF)

## Usage Example

```python
from padlet_scraper import PadletScraper

# Initialize scraper
scraper = PadletScraper()

# Scrape a Padlet
padlet_data = await scraper.scrape("https://padlet.com/example/board")

# Access structured data
for section in padlet_data.sections:
    print(f"Section: {section.title}")
    for post in section.posts:
        print(f"  - {post.subject}: {post.body}")
```

## Development Status

- [x] Basic project structure
- [x] Data models (Padlet, Section, Post)
- [x] nodriver scraper implementation
- [x] Export to JSON
- [x] Export to Markdown
- [x] Command-line interface
- [x] Container-based scrolling for lazy-loaded content
- [x] Headless mode with viewport fix
- [x] Paragraph spacing preservation
- [ ] Error handling and retries
- [ ] AI prompt generation

## Known Issues & Solutions

- **Event loop cleanup warning on exit** - Cosmetic issue, doesn't affect functionality. Fixed with proper async cleanup in CLI.
- **Browser requirement** - Requires Chromium or Chrome browser. Arc not compatible with nodriver.
- **macOS keychain prompt** - First run may require approving browser automation via keychain.
- **Sandbox parameter** - Most systems require `sandbox=False` parameter for proper operation.
- **Lazy-loaded content** - Fixed by scrolling individual section containers and setting proper viewport size in headless mode.

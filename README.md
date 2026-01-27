# Padlet Scraper

Tool to scrape Padlets from links and convert them to readable data types so they can be fed to an AI model.

## Purpose

This tool helps students and professionals who store their experiences, projects, and achievements in Padlet boards. It extracts the structured content and converts it into formats suitable for creating personal statements, CVs, and other professional documents.

## Installation

### Quick Install (Recommended)

**macOS/Linux:**
```bash
./install.sh
```

**Windows:**
```cmd
install.bat
```

### Usage After Install

**macOS/Linux:**
```bash
./run-scraper.sh "https://padlet.com/user/board" -o output.json
```

**Windows:**
```cmd
run-scraper.bat "https://padlet.com/user/board" -o output.json
```

See [TEACHER_GUIDE.md](TEACHER_GUIDE.md) for a simplified guide.

### Manual Install

If you prefer manual installation:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line (Recommended)

```bash
# Scrape and save to JSON
./padlet-scraper "https://padlet.com/user/board" --headless --no-sandbox -o output.json

# Scrape and save to Markdown
./padlet-scraper "https://padlet.com/user/board" --headless --no-sandbox -o output.md

# Print JSON to stdout (for piping)
./padlet-scraper "https://padlet.com/user/board" --headless --no-sandbox --format json
```

See [CLI_USAGE.md](CLI_USAGE.md) for more examples and integration with other languages.

### Python API

#### Basic Example

```python
import asyncio
from padlet_scraper import scrape_padlet

async def main():
    # Scrape a Padlet
    padlet = await scrape_padlet("https://padlet.com/your-padlet-url")

    # Access the data
    print(padlet)
    for section in padlet.sections:
        print(f"{section.title}: {len(section.posts)} posts")

asyncio.run(main())
```

#### Advanced Example with Export

```python
import asyncio
from padlet_scraper import PadletScraper
from padlet_scraper.utils import save_to_json, save_to_markdown

async def main():
    scraper = PadletScraper(headless=True)
    padlet = await scraper.scrape("https://padlet.com/your-padlet-url")

    # Save to JSON
    save_to_json(padlet, "output.json")

    # Save to Markdown
    save_to_markdown(padlet, "output.md")

asyncio.run(main())
```

See the `examples/` directory for more examples.

## Data Structure

The scraper extracts:
- **Sections**: Column headers/titles
- **Posts**: Individual entries within sections
  - Subject: Post title
  - Body: Post content

## Project Structure

```
├── padlet_scraper/       # Main package
│   ├── models.py         # Data models (Padlet, Section, Post)
│   ├── scraper.py        # Scraping logic using nodriver
│   └── utils.py          # Export utilities
├── examples/             # Usage examples
├── CLAUDE.md            # Detailed project documentation
└── requirements.txt     # Python dependencies
```

## Future Enhancements

- Extract images and attachments
- Support different Padlet layouts (wall, canvas, timeline)
- AI prompt generation for CV/personal statement creation
- Export to additional formats
# Quick Reference Card

## Install (One Command)

```bash
pip install git+https://github.com/HealthyDoggo/padlet-scraper.git
```

## Basic Usage

```bash
# JSON output (headless by default)
padlet-scraper "PADLET_URL" --no-sandbox -o output.json

# Markdown output
padlet-scraper "PADLET_URL" --no-sandbox -o output.md

# Show summary
padlet-scraper "PADLET_URL" --no-sandbox

# Show browser (for debugging)
padlet-scraper "PADLET_URL" --no-headless --no-sandbox -o output.json
```

## Common Options

| Flag | Description |
|------|-------------|
| `--no-headless` | Show browser window (default is headless) |
| `--no-sandbox` | Required on most systems |
| `-o FILE` | Save to file (.json or .md) |
| `--format json` | Print JSON to stdout |
| `--help` | Show all options |

## For Google AI Studio

```bash
# 1. Scrape to markdown
padlet-scraper "URL" --no-sandbox -o student.md

# 2. Open student.md and copy-paste into AI Studio
```

## Troubleshooting

**"Command not found"**
```bash
python3 -m padlet_scraper.cli "URL" -o output.json
```

**Browser errors**
- Install Chromium: `brew install --cask chromium` (Mac)
- Always use `--no-sandbox` flag

**Upgrade**
```bash
pip install --upgrade git+https://github.com/HealthyDoggo/padlet-scraper.git
```

## Examples

```bash
# Single student
padlet-scraper "https://padlet.com/student1/work" -o student1.json

# Markdown for reading
padlet-scraper "https://padlet.com/student1/work" -o student1.md

# Pipe to jq (JSON processing)
padlet-scraper "URL" --format json | jq '.sections[0].posts'
```

## GitHub Repository

https://github.com/HealthyDoggo/padlet-scraper

## Share This

Send teachers this link:
https://github.com/HealthyDoggo/padlet-scraper#readme

Or share the one-liner:
```bash
pip install git+https://github.com/HealthyDoggo/padlet-scraper.git
```

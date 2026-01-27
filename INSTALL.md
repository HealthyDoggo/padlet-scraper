# Installation Guide

## Quick Install (Recommended)

### macOS/Linux

1. Open Terminal
2. Navigate to the project folder:
   ```bash
   cd "/path/to/Padlet Scraper"
   ```
3. Run the installer:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

### Windows

1. Open Command Prompt
2. Navigate to the project folder:
   ```cmd
   cd "C:\path\to\Padlet Scraper"
   ```
3. Run the installer:
   ```cmd
   install.bat
   ```

## Manual Installation

If the automatic installer doesn't work, follow these steps:

### 1. Install Python

Make sure you have Python 3.8 or higher:
- **macOS/Linux**: Usually pre-installed, or use `brew install python3`
- **Windows**: Download from https://python.org (check "Add Python to PATH")

### 2. Install Chromium Browser

**macOS:**
```bash
brew install --cask chromium
xattr -dr com.apple.quarantine /Applications/Chromium.app
```

**Windows:**
Download from https://www.chromium.org/getting-involved/download-chromium/

**Linux:**
```bash
sudo apt install chromium-browser
```

### 3. Install the Package

```bash
# Navigate to project directory
cd "/path/to/Padlet Scraper"

# Install with pip
pip3 install -e .
```

## Verify Installation

```bash
padlet-scraper --help
```

You should see the help message with usage instructions.

## Usage

```bash
# Basic usage
padlet-scraper "https://padlet.com/user/board" --headless --no-sandbox -o output.json

# Save as Markdown
padlet-scraper "https://padlet.com/user/board" --headless --no-sandbox -o output.md
```

## Sharing with Others

### Option 1: Share the Folder

1. Zip the entire "Padlet Scraper" folder
2. Send to your teacher
3. They run `install.sh` (Mac/Linux) or `install.bat` (Windows)

### Option 2: Create a Package

```bash
# Create a distributable package
python3 setup.py sdist bdist_wheel

# Share the generated file in dist/
# They can install with: pip install padlet-scraper-1.0.0.tar.gz
```

### Option 3: PyPI (for wider distribution)

If you want anyone to install with just `pip install padlet-scraper`, you would need to:
1. Create account on https://pypi.org
2. Upload: `python3 -m twine upload dist/*`

## Troubleshooting

### "Command not found: padlet-scraper"

Try:
```bash
python3 -m padlet_scraper.cli --help
```

Or reinstall:
```bash
pip3 install -e . --force-reinstall
```

### Browser Issues

If you get browser errors:
1. Make sure Chromium is installed
2. Try without `--headless` flag to see the browser
3. Always use `--no-sandbox` flag

### Python Version Issues

Check your Python version:
```bash
python3 --version
```

Must be 3.8 or higher.

## Uninstalling

```bash
pip3 uninstall padlet-scraper
```

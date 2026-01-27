# Install Directly from GitHub

## Super Quick Install (One Command)

The easiest way to install is directly from GitHub using pip:

```bash
pip install git+https://github.com/HealthyDoggo/padlet-scraper.git
```

That's it! After installation, you can use `padlet-scraper` from anywhere.

## System Requirements

1. **Python 3.8+** - Check with: `python3 --version`
2. **Chromium or Chrome browser**
   - macOS: `brew install --cask chromium`
   - Windows: Download from https://www.chromium.org/
   - Linux: `sudo apt install chromium-browser`

## Usage After Install

```bash
# Basic usage
padlet-scraper "https://padlet.com/user/board" --headless --no-sandbox -o output.json

# Save as Markdown
padlet-scraper "https://padlet.com/user/board" --headless --no-sandbox -o output.md

# Get help
padlet-scraper --help
```

## For Teachers (Non-Technical Users)

If you're not comfortable with command line:

1. **Download the zip** from GitHub (green "Code" button → Download ZIP)
2. **Unzip** the folder
3. **Double-click** `install.sh` (Mac) or `install.bat` (Windows)
4. **Use the wrapper**: `./run-scraper.sh "URL" -o output.json`

See [TEACHER_GUIDE.md](TEACHER_GUIDE.md) for more details.

## Virtual Environment (Recommended)

If you want to install in a virtual environment:

```bash
# Create virtual environment
python3 -m venv padlet-env

# Activate it
source padlet-env/bin/activate  # Mac/Linux
# or
padlet-env\Scripts\activate  # Windows

# Install from GitHub
pip install git+https://github.com/HealthyDoggo/padlet-scraper.git

# Use it
padlet-scraper "URL" -o output.json
```

## Upgrading

To get the latest version:

```bash
pip install --upgrade git+https://github.com/HealthyDoggo/padlet-scraper.git
```

## Uninstalling

```bash
pip uninstall padlet-scraper
```

## Alternative: Clone and Install

If you want to modify the code:

```bash
# Clone the repository
git clone https://github.com/HealthyDoggo/padlet-scraper.git
cd padlet-scraper

# Install in development mode
pip install -e .
```

## Troubleshooting

### "Command not found: padlet-scraper"

Make sure pip's bin directory is in your PATH, or use:
```bash
python3 -m padlet_scraper.cli --help
```

### Browser Issues

If you get browser errors:
1. Install Chromium: `brew install --cask chromium` (Mac)
2. Remove quarantine: `xattr -dr com.apple.quarantine /Applications/Chromium.app`
3. Always use `--no-sandbox` flag

### Permission Errors

If you get permission errors during install, use:
```bash
pip install --user git+https://github.com/HealthyDoggo/padlet-scraper.git
```

## Integration Examples

### From Node.js

```javascript
const { execSync } = require('child_process');

// One-time install
execSync('pip install git+https://github.com/HealthyDoggo/padlet-scraper.git');

// Use it
const result = execSync('padlet-scraper "URL" --headless --no-sandbox --format json');
const data = JSON.parse(result);
```

### From Python

```python
import subprocess
import sys

# One-time install
subprocess.check_call([
    sys.executable, '-m', 'pip', 'install',
    'git+https://github.com/HealthyDoggo/padlet-scraper.git'
])

# Use it
from padlet_scraper import PadletScraper

scraper = PadletScraper(headless=True, sandbox=False)
padlet = await scraper.scrape("URL")
```

### From Shell Script

```bash
#!/bin/bash

# Check if installed
if ! command -v padlet-scraper &> /dev/null; then
    echo "Installing padlet-scraper..."
    pip install git+https://github.com/HealthyDoggo/padlet-scraper.git
fi

# Use it
padlet-scraper "$1" --headless --no-sandbox -o output.json
```

## What Gets Installed

When you run the pip install command:
- `padlet-scraper` command-line tool
- `padlet_scraper` Python package
- All dependencies (nodriver, pydantic)

You can then import it in Python:
```python
from padlet_scraper import PadletScraper, Padlet, Section, Post
from padlet_scraper.utils import save_to_json, save_to_markdown
```

## Why This Works

The repository includes a `setup.py` file that tells pip:
- Package name and version
- Python version requirements
- Dependencies to install
- Command-line entry points

This makes it installable like any PyPI package, but directly from GitHub.

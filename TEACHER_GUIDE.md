# Teacher's Quick Start Guide

## Installation Options

### Option A: One-Line Install (If you have pip)

Open Terminal (Mac) or Command Prompt (Windows) and run:

```bash
pip install git+https://github.com/HealthyDoggo/padlet-scraper.git
```

Then you can use `padlet-scraper` from anywhere! Skip to "How to Use It" below.

### Option B: Download and Install (No pip needed)

## Super Simple Installation (3 Steps)

### macOS

1. **Download** the "Padlet Scraper" folder
2. **Open Terminal** (Applications → Utilities → Terminal)
3. **Run these commands:**
   ```bash
   cd ~/Downloads/Padlet\ Scraper
   ./install.sh
   ```

### Windows

1. **Download** the "Padlet Scraper" folder
2. **Open Command Prompt** (Win+R, type `cmd`, press Enter)
3. **Run these commands:**
   ```cmd
   cd Downloads\Padlet Scraper
   install.bat
   ```

That's it! Installation takes about 2-3 minutes.

## How to Use It

### Basic Usage

**macOS/Linux:**
```bash
./run-scraper.sh "https://padlet.com/your/padlet" --no-sandbox -o output.json
```

**Windows:**
```cmd
run-scraper.bat "https://padlet.com/your/padlet" --no-sandbox -o output.json
```

Note: The scraper runs in headless mode by default (no browser window). Add `--no-headless` if you want to see the browser.

This creates a file called `output.json` with all the Padlet content.

### What You Get

The scraper creates a structured file with:
- All section titles
- All post titles and content
- Preserved paragraph spacing
- Everything in JSON or Markdown format

### Example Output

**JSON format** (for AI processing):
```json
{
  "title": "Student Projects",
  "sections": [
    {
      "title": "Year 12 Work",
      "posts": [
        {
          "subject": "Science Fair Project",
          "body": "Description of the project..."
        }
      ]
    }
  ]
}
```

**Markdown format** (for reading):
```markdown
# Student Projects

## Year 12 Work

### Science Fair Project

Description of the project...
```

## Using with Google AI Studio / Firebase

Once you have the JSON file, you can:

### Option 1: Copy-Paste

1. Run the scraper to get `output.md` (Markdown format)
2. Open `output.md` in any text editor
3. Copy the content
4. Paste into Google AI Studio prompt

### Option 2: Automated (Advanced)

Create a simple script to send to AI:

```python
import json
import google.generativeai as genai

# Configure API
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel('gemini-pro')

# Load scraped data
with open('output.json') as f:
    padlet_data = json.load(f)

# Create prompt
prompt = f"""
Please help write a personal statement based on this student's work:

{json.dumps(padlet_data, indent=2)}

Focus on their achievements and growth.
"""

# Get AI response
response = model.generate_content(prompt)
print(response.text)
```

## Tips for Teachers

1. **Save Padlet Links**: Keep a list of student Padlet URLs in a text file
2. **Batch Processing**: Create a script to process multiple students at once
3. **Regular Backups**: Run the scraper periodically to backup student work
4. **Format Choice**:
   - Use JSON if feeding to AI
   - Use Markdown if you want to read it yourself

## Troubleshooting

### "Command not found"

Make sure you ran `./install.sh` first

### Browser Window Appears

The scraper runs in headless mode by default (no window). If you see a window, that's fine - it means you used `--no-headless` flag.

### "No posts found"

The Padlet might be private. Make sure it's public or shared with you.

## Getting Help

Run this for all options:
```bash
./run-scraper.sh --help
```

## Common Use Cases

### 1. Single Student

```bash
./run-scraper.sh "https://padlet.com/student1/work" -o student1.json
```

### 2. Export as Markdown for Reading

```bash
./run-scraper.sh "https://padlet.com/student1/work" -o student1.md
```

### 3. Quick View (No File)

```bash
./run-scraper.sh "https://padlet.com/student1/work"
```

This just shows a summary in the terminal.

## Privacy Note

This tool only scrapes **public** or **shared** Padlets. It doesn't access private content without permission.

## Questions?

Contact your IT support or the person who gave you this tool.

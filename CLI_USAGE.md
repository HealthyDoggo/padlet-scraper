# Padlet Scraper CLI Usage

## Basic Usage

```bash
# Scrape and save to JSON (headless by default)
./padlet-scraper "https://padlet.com/user/board" --no-sandbox -o output.json

# Scrape and save to Markdown
./padlet-scraper "https://padlet.com/user/board" --no-sandbox -o output.md

# Scrape with browser visible (for debugging)
./padlet-scraper "https://padlet.com/user/board" --no-headless --no-sandbox -o output.json

# Print JSON to stdout (for piping to other tools)
./padlet-scraper "https://padlet.com/user/board" --no-sandbox --format json

# Print Markdown to stdout
./padlet-scraper "https://padlet.com/user/board" --no-sandbox --format markdown

# Show summary (no output file)
./padlet-scraper "https://padlet.com/user/board" --no-sandbox
```

## Options

- `--no-headless` - Show browser window (default is headless mode)
- `--no-sandbox` - Disable browser sandbox (required on most systems)
- `-o, --output FILE` - Save to file (.json or .md extension)
- `--format {json,markdown}` - Output format for stdout
- `--browser PATH` - Path to specific browser executable
- `--timeout SECONDS` - Timeout for page elements (default: 30)

## Integration with Other Tools

### Shell Script Example

```bash
#!/bin/bash
URL="https://padlet.com/user/board"
OUTPUT_DIR="./scraped_padlets"

mkdir -p "$OUTPUT_DIR"
./padlet-scraper "$URL" --headless --no-sandbox -o "$OUTPUT_DIR/padlet.json"

echo "Scraped to $OUTPUT_DIR/padlet.json"
```

### Node.js Example

```javascript
const { execSync } = require('child_process');

const url = 'https://padlet.com/user/board';
const result = execSync(
  `./padlet-scraper "${url}" --headless --no-sandbox --format json`,
  { encoding: 'utf-8' }
);

const padletData = JSON.parse(result);
console.log(`Found ${padletData.sections.length} sections`);
```

### Python Example

```python
import subprocess
import json

url = "https://padlet.com/user/board"
result = subprocess.run(
    ["./padlet-scraper", url, "--headless", "--no-sandbox", "--format", "json"],
    capture_output=True,
    text=True
)

padlet_data = json.loads(result.stdout)
print(f"Found {len(padlet_data['sections'])} sections")
```

### cURL/HTTP Example (if using REST API)

```bash
# POST request with JSON body
curl -X POST http://localhost:5000/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://padlet.com/user/board", "headless": true}'

# GET request with query parameters
curl "http://localhost:5000/scrape?url=https://padlet.com/user/board&format=json"
```

## Output Format

### JSON Structure

```json
{
  "url": "https://padlet.com/user/board",
  "title": "Board Title",
  "sections": [
    {
      "title": "Section Name",
      "section_id": "123456",
      "posts": [
        {
          "subject": "Post Title",
          "body": "Post content with\n\nparagraphs preserved",
          "section_id": "123456"
        }
      ]
    }
  ]
}
```

### Markdown Structure

```markdown
# Board Title

## Section Name

### Post Title

Post content with

paragraphs preserved
```

## Tips

1. **Headless is default** - runs without showing browser window (faster)
2. **Always use `--no-sandbox`** unless you have specific security requirements
3. **Paragraph spacing is preserved** - single newlines become `\n`, double newlines become `\n\n`
4. **"Suggested Content" sections are automatically filtered out**
5. **For debugging**, use `--no-headless` to see the browser
6. **Large padlets** - automatically scrolls to load all sections and posts

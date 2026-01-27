"""Command-line interface for Padlet scraper."""

import argparse
import asyncio
import sys
from pathlib import Path
from .scraper import PadletScraper
from .utils import save_to_json, save_to_markdown


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Scrape Padlet boards and export to JSON or Markdown",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape and save to JSON (headless by default)
  padlet-scraper https://padlet.com/user/board -o output.json

  # Scrape and save to Markdown
  padlet-scraper https://padlet.com/user/board -o output.md

  # Show browser window (for debugging)
  padlet-scraper https://padlet.com/user/board --no-headless -o output.json

  # Print JSON to stdout
  padlet-scraper https://padlet.com/user/board --format json
        """
    )

    parser.add_argument(
        "url",
        help="URL of the Padlet to scrape"
    )

    parser.add_argument(
        "-o", "--output",
        help="Output file path (extension determines format: .json or .md)"
    )

    parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        help="Output format when printing to stdout (use with no -o flag)"
    )

    parser.add_argument(
        "--no-headless",
        action="store_true",
        help="Show browser window (default is headless mode)"
    )

    parser.add_argument(
        "--no-sandbox",
        action="store_true",
        help="Disable browser sandbox (may be needed on some systems)"
    )

    parser.add_argument(
        "--browser",
        help="Path to browser executable (Chrome, Chromium, etc.)"
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Timeout in seconds for page elements (default: 30)"
    )

    args = parser.parse_args()

    # Run the scraper with proper event loop cleanup
    try:
        # Create and manage event loop manually for proper cleanup
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            padlet = loop.run_until_complete(scrape_with_args(args))
        finally:
            # Cleanup pending tasks
            try:
                # Cancel all remaining tasks
                pending = asyncio.all_tasks(loop)
                for task in pending:
                    task.cancel()
                # Wait for task cancellations to complete
                if pending:
                    loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
            except Exception:
                pass
            # Give subprocesses time to cleanup
            loop.run_until_complete(asyncio.sleep(0.25))
            # Close the loop
            loop.close()

        # Output handling
        if args.output:
            output_path = Path(args.output)

            if output_path.suffix.lower() == ".json":
                save_to_json(padlet, output_path)
                print(f"✓ Saved to {output_path}")
            elif output_path.suffix.lower() == ".md":
                save_to_markdown(padlet, output_path)
                print(f"✓ Saved to {output_path}")
            else:
                print(f"Error: Unsupported file extension '{output_path.suffix}'. Use .json or .md", file=sys.stderr)
                sys.exit(1)

        elif args.format:
            if args.format == "json":
                import json
                print(json.dumps(padlet.model_dump(), indent=2, ensure_ascii=False))
            elif args.format == "markdown":
                print(padlet.to_markdown())

        else:
            # Default: print summary
            print(f"\n{padlet}")
            print(f"\nSections:")
            for section in padlet.sections:
                print(f"  - {section.title}: {len(section.posts)} post(s)")

    except KeyboardInterrupt:
        print("\nCancelled by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


async def scrape_with_args(args):
    """Scrape Padlet with CLI arguments."""
    scraper = PadletScraper(
        headless=not args.no_headless,  # Headless by default, unless --no-headless
        timeout=args.timeout,
        browser_executable_path=args.browser,
        sandbox=not args.no_sandbox
    )

    print(f"Scraping {args.url}...", file=sys.stderr)
    padlet = await scraper.scrape(args.url)
    print(f"✓ Scraped {len(padlet.sections)} sections, {padlet.total_posts} posts", file=sys.stderr)

    return padlet


if __name__ == "__main__":
    main()

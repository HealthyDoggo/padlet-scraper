"""Example script demonstrating how to use the Padlet scraper."""

import asyncio
from padlet_scraper import PadletScraper
from padlet_scraper.utils import save_to_json, save_to_markdown


async def main():
    """Main example function."""
    # Replace with your Padlet URL
    padlet_url = "https://padlet.com/22scassidy/employable-my-skills-my-voice-my-record-tfjw095jo0jlpz7l"

    # Initialize the scraper
    # Note: Set headless=True to run without showing the browser window
    # sandbox=False may be needed on some systems
    scraper = PadletScraper(headless=False, sandbox=False)

    print(f"Scraping Padlet: {padlet_url}")
    print("This may take a few seconds...\n")

    # Scrape the Padlet
    padlet = await scraper.scrape(padlet_url)

    # Print summary
    print(f"✓ Successfully scraped: {padlet}")
    print()

    # Print detailed structure
    for section in padlet.sections:
        print(f"\n{section}")
        for post in section.posts:
            print(f"  - {post.subject}")
            if post.body:
                preview = post.body[:100] + "..." if len(post.body) > 100 else post.body
                print(f"    {preview}")

    # Save to JSON
    save_to_json(padlet, "output.json")
    print("\n✓ Saved to output.json")

    # Save to Markdown
    save_to_markdown(padlet, "output.md")
    print("✓ Saved to output.md")


if __name__ == "__main__":
    asyncio.run(main())

"""Simplified example for quick scraping."""

import asyncio
from padlet_scraper import scrape_padlet


async def main():
    """Quick scrape example."""
    url = "https://padlet.com/YOUR_PADLET_URL_HERE"

    # Scrape the Padlet
    padlet = await scrape_padlet(url, headless=True)

    # Print the results
    print(padlet)
    print("\nSections:")
    for section in padlet.sections:
        print(f"  - {section.title}: {len(section.posts)} posts")


if __name__ == "__main__":
    asyncio.run(main())

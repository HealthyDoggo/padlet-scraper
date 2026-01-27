"""Padlet scraper using nodriver for browser automation."""

import asyncio
from typing import Optional
import nodriver as uc
from nodriver import cdp
from .models import Post, Section, Padlet


class PadletScraper:
    """Scraper for extracting structured data from Padlet boards."""

    def __init__(self, headless: bool = True, timeout: int = 30, browser_executable_path: Optional[str] = None, sandbox: bool = True):
        """
        Initialize the Padlet scraper.

        Args:
            headless: Whether to run browser in headless mode
            timeout: Maximum time to wait for page elements (seconds)
            browser_executable_path: Path to browser executable (Chrome, Edge, Brave, Arc).
                                    If None, nodriver will attempt to download Chromium.
            sandbox: Whether to use Chrome sandbox (set to False if having connection issues)
        """
        self.headless = headless
        self.timeout = timeout
        self.browser_executable_path = browser_executable_path
        self.sandbox = sandbox

    async def scrape(self, url: str) -> Padlet:
        """
        Scrape a Padlet board and return structured data.

        Args:
            url: The URL of the Padlet to scrape

        Returns:
            Padlet object containing all sections and posts
        """
        # Start browser
        try:
            if self.browser_executable_path:
                browser = await uc.start(
                    headless=self.headless,
                    browser_executable_path=self.browser_executable_path,
                    sandbox=self.sandbox
                )
            else:
                browser = await uc.start(headless=self.headless, sandbox=self.sandbox)
        except FileNotFoundError as e:
            raise FileNotFoundError(
                "Chrome/Chromium browser not found. Please either:\n"
                "1. Install Chrome from https://www.google.com/chrome/\n"
                "2. Or specify browser path: PadletScraper(browser_executable_path='/path/to/browser')\n"
                "   Common paths:\n"
                "   - Arc: '/Applications/Arc.app/Contents/MacOS/Arc'\n"
                "   - Chrome: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'\n"
                "   - Brave: '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'\n"
                "   - Edge: '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge'"
            ) from e

        try:
            page = await browser.get(url)

            # Set viewport size in headless mode to fix scrolling/lazy-loading
            if self.headless:
                try:
                    await page.send(
                        cdp.emulation.set_device_metrics_override(
                            width=1920, height=1080,
                            device_scale_factor=1,
                            mobile=False,
                            # These two are important for changing window.screen.* values
                            screen_width=1920, screen_height=1080,
                            position_x=0, position_y=0
                        )
                    )
                except Exception as e:
                    print(f"Warning: Could not set viewport size: {e}")

            # Wait for the page to load - Padlets are JavaScript-heavy
            await page.sleep(3)  # Initial load time

            # Try to wait for sections to appear
            try:
                await page.find('[data-testid="sectionTitleText"]', timeout=self.timeout)
            except Exception:
                # Padlet might not have sections, or they might be named differently
                pass

            # Scroll to load all dynamic content
            await self._scroll_to_load_all(page)

            # Extract Padlet title
            title = await self._extract_title(page)

            # Extract all sections
            sections = await self._extract_sections(page)

            return Padlet(
                url=url,
                title=title,
                sections=sections
            )

        finally:
            # Stop browser and cleanup properly
            browser.stop()
            # Give browser process time to cleanup before event loop closes
            await asyncio.sleep(0.1)

    async def _scroll_to_load_all(self, page) -> None:
        """Scroll each section container to load all dynamic content."""
        try:
            # Find all section containers with scrollable posts
            # These have class "overflow-y-auto" and id like "group-posts-{section_id}"
            scroll_containers = await page.query_selector_all('[class*="overflow-y-auto"][id^="group-posts-"]')

            print(f"Found {len(scroll_containers)} scrollable section containers", flush=True)

            for container in scroll_containers:
                # Get container ID for logging
                container_id = container.attrs.get('id', 'unknown')

                # Count initial posts
                prev_count = 0

                # Scroll this specific container
                for scroll_attempt in range(15):  # Max 15 scrolls per container
                    # Scroll the container to its bottom
                    await page.evaluate(f'''
                        (function() {{
                            const container = document.getElementById("{container_id}");
                            if (container) {{
                                container.scrollTop = container.scrollHeight;
                            }}
                        }})()
                    ''')

                    # Wait for content to load
                    await page.sleep(1.5)

                    # Re-query the container and count posts (don't use cached container)
                    fresh_container = await page.query_selector(f'#{container_id}')
                    if fresh_container:
                        current_posts = await fresh_container.query_selector_all('[data-testid="surfacePost"]')
                        current_count = len(current_posts) if current_posts else 0
                    else:
                        current_count = prev_count

                    # If no new posts loaded for 2 consecutive attempts, we've reached the end
                    if current_count == prev_count and scroll_attempt > 1:
                        break

                    prev_count = current_count

                print(f"  {container_id}: loaded {prev_count} posts", flush=True)

        except Exception as e:
            print(f"Warning: Error during scrolling: {e}")

    async def _extract_title(self, page) -> Optional[str]:
        """Extract the Padlet board title."""
        try:
            # Try common title selectors
            title_element = await page.query_selector('h1')
            if title_element:
                return title_element.text_all
        except Exception:
            pass

        return None

    async def _extract_sections(self, page) -> list[Section]:
        """Extract all sections/columns from the Padlet."""
        sections = []

        try:
            # Find all top-level sections (columns)
            section_elements = await page.query_selector_all('section[data-id][data-rank]')

            for section_element in section_elements:
                # Get section ID
                section_id = section_element.attrs.get('data-id')

                # Get section title
                title = await self._extract_section_title(section_element)

                # Skip "Suggested Content" section
                if title and title.lower() == "suggested content":
                    continue

                # Get all posts in this section
                posts = await self._extract_posts(section_element, section_id)

                # Only add sections that have a title or posts
                if title or posts:
                    sections.append(Section(
                        title=title or "Untitled Section",
                        section_id=section_id,
                        posts=posts
                    ))

        except Exception as e:
            print(f"Error extracting sections: {e}")

        return sections

    async def _extract_section_title(self, section_element) -> Optional[str]:
        """Extract the title of a section."""
        try:
            title_element = await section_element.query_selector('[data-testid="sectionTitleText"]')
            if title_element:
                return title_element.text_all
        except Exception:
            pass

        return None

    async def _extract_posts(self, section_element, section_id: str) -> list[Post]:
        """Extract all posts from a section."""
        posts = []

        try:
            # Find all post wrappers in this section
            post_elements = await section_element.query_selector_all('[data-testid="surfacePost"]')

            for post_element in post_elements:
                # Extract subject
                subject = await self._extract_post_subject(post_element)

                # Extract body
                body = await self._extract_post_body(post_element)

                # Only add posts that have content
                if subject or body:
                    posts.append(Post(
                        subject=subject or "Untitled",
                        body=body or "",
                        section_id=section_id
                    ))

        except Exception as e:
            print(f"Error extracting posts from section {section_id}: {e}")

        return posts

    async def _extract_post_subject(self, post_element) -> Optional[str]:
        """Extract the subject/title of a post."""
        try:
            subject_element = await post_element.query_selector('[data-pw="postSubject"]')
            if subject_element:
                return subject_element.text_all
        except Exception:
            pass

        return None

    async def _extract_post_body(self, post_element) -> Optional[str]:
        """Extract the body content of a post, preserving exact spacing."""
        try:
            body_element = await post_element.query_selector('[data-pw="postBody"]')
            if body_element:
                # Get HTML to analyze structure
                html = await body_element.get_html()

                if html:
                    # Get all paragraph tags within the body
                    paragraphs = await body_element.query_selector_all('p')

                    if paragraphs:
                        result_parts = []
                        prev_had_spacer = False

                        for i, p in enumerate(paragraphs):
                            text = p.text_all.strip()

                            # Check if this is a spacer paragraph (<p><br></p>)
                            if not text or text == '':
                                prev_had_spacer = True
                                continue

                            # Add spacing before this paragraph (except for the first one)
                            if result_parts:
                                if prev_had_spacer:
                                    result_parts.append('\n\n')
                                else:
                                    result_parts.append('\n')

                            result_parts.append(text)
                            prev_had_spacer = False

                        return ''.join(result_parts) if result_parts else None

                # Fallback to text_all if no HTML or paragraphs found
                return body_element.text_all
        except Exception:
            pass

        return None


async def scrape_padlet(url: str, headless: bool = True) -> Padlet:
    """
    Convenience function to scrape a Padlet.

    Args:
        url: The URL of the Padlet to scrape
        headless: Whether to run browser in headless mode

    Returns:
        Padlet object containing all sections and posts
    """
    scraper = PadletScraper(headless=headless)
    return await scraper.scrape(url)

"""Padlet scraper using nodriver for browser automation."""

import asyncio
import json
import os
import sys
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
            await page.sleep(0.5)  # Initial load time

            # Try to wait for sections to appear
            try:
                await page.find('[data-testid="sectionTitleText"]', timeout=self.timeout)
            except Exception:
                # Padlet might not have sections, or they might be named differently
                pass

            # First scroll the main page to load all sections/rows
            await self._scroll_main_page(page)

            # Then scroll individual section containers to load all posts
            await self._scroll_section_containers(page)

            # Wait for DOM to fully render all lazy-loaded content
            await page.sleep(1.0)

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
            # IMPORTANT: nodriver Browser.stop() schedules async disconnect work
            # on the current loop; keep the loop alive briefly so stdout output
            # isn't followed by asyncio warnings/errors.
            try:
                browser.stop()
            finally:
                await asyncio.sleep(0.75)

    async def _scroll_main_page(self, page) -> None:
        """Scroll the main page to load all sections/rows."""
        try:
            print("Scrolling main page to load all sections...", file=sys.stderr, flush=True)

            prev_section_count = 0

            # Scroll the main page multiple times to load all sections
            for scroll_attempt in range(15):
                # Scroll to bottom of page
                await page.evaluate('''
                    (function() {
                        window.scrollTo(0, document.body.scrollHeight);
                    })()
                ''')

                # Wait for content to load
                await page.sleep(0.01)

                # Count sections
                sections = await page.query_selector_all('section[data-id][data-rank]')
                current_count = len(sections) if sections else 0

                # If no new sections loaded for 2 consecutive attempts, we're done
                if current_count == prev_section_count and scroll_attempt > 1:
                    break

                prev_section_count = current_count

            # Scroll back to top
            await page.evaluate('window.scrollTo(0, 0)')
            await page.sleep(0.1)

            print(f"Loaded {prev_section_count} sections", file=sys.stderr, flush=True)

        except Exception as e:
            print(f"Warning: Error during main page scrolling: {e}", file=sys.stderr)

    async def _scroll_section_containers(self, page) -> None:
        """Scroll each section container to load all posts within sections."""
        try:
            # Find all section containers with scrollable posts
            # These have class "overflow-y-auto" and id like "group-posts-{section_id}"
            scroll_containers = await page.query_selector_all('[class*="overflow-y-auto"][id^="group-posts-"]')

            print(f"Found {len(scroll_containers)} scrollable section containers", file=sys.stderr, flush=True)

            for container in scroll_containers:
                # Scroll the container into view first (may trigger lazy loading)
                try:
                    await container.scroll_into_view()
                    await page.sleep(0.01)
                except Exception:
                    pass  # Ignore if scrollIntoView fails
                # Get container ID for logging
                container_id = container.attrs.get('id', 'unknown')

                # Count initial posts
                prev_count = 0

                # Scroll this specific container
                for scroll_attempt in range(15):  # Max 15 scrolls per container
                    # Scroll the container to its bottom and count posts in one JS call
                    current_count = await page.evaluate(f'''
                        (function() {{
                            const container = document.getElementById("{container_id}");
                            if (!container) return 0;
                            
                            // Scroll to bottom
                            container.scrollTop = container.scrollHeight;
                            
                            // Count posts
                            const posts = container.querySelectorAll('[data-testid="surfacePost"]');
                            return posts.length;
                        }})()
                    ''')
                    
                    # Wait briefly for lazy loading
                    await page.sleep(0.01)

                    # If no new posts loaded for 2 consecutive attempts, we've reached the end
                    if current_count == prev_count and scroll_attempt > 1:
                        break

                    prev_count = current_count

                print(f"  {container_id}: loaded {prev_count} posts", file=sys.stderr, flush=True)

        except Exception as e:
            print(f"Warning: Error during scrolling: {e}", file=sys.stderr)

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
        """Extract all sections/columns from the Padlet (parallelized)."""
        try:
            # Find all top-level sections (columns)
            section_elements = await page.query_selector_all('section[data-id][data-rank]')

            # Create tasks for parallel extraction
            tasks = [
                self._extract_single_section(page, section_element)
                for section_element in section_elements
            ]

            # Process all sections in parallel
            sections = await asyncio.gather(*tasks, return_exceptions=True)

            # Filter out None values and exceptions
            valid_sections = []
            for section in sections:
                if isinstance(section, Section):
                    valid_sections.append(section)
                elif isinstance(section, Exception):
                    print(f"Warning: Section extraction failed: {section}")

            return valid_sections

        except Exception as e:
            print(f"Error extracting sections: {e}")
            return []

    async def _extract_single_section(self, page, section_element) -> Optional[Section]:
        """Extract a single section/column from the Padlet."""
        try:
            # Get section ID
            section_id = section_element.attrs.get('data-id')

            # Get section title
            title = await self._extract_section_title(section_element)

            # Skip "Suggested Content" section
            if title and title.lower() == "suggested content":
                return None

            # Get all posts in this section
            posts = await self._extract_posts(page, section_id)

            # Only return section if it has a title or posts
            if title or posts:
                return Section(
                    title=title or "Untitled Section",
                    section_id=section_id,
                    posts=posts
                )

            return None

        except Exception as e:
            print(f"Error extracting section: {e}")
            return None

    async def _extract_section_title(self, section_element) -> Optional[str]:
        """Extract the title of a section."""
        try:
            title_element = await section_element.query_selector('[data-testid="sectionTitleText"]')
            if title_element:
                return title_element.text_all
        except Exception:
            pass

        return None

    async def _extract_posts(self, page, section_id: str) -> list[Post]:
        """Extract all posts from a section using batch JavaScript extraction."""
        try:
            # NOTE: write logs to stderr so `--format json` stays valid JSON on stdout
            # print(f"  Extracting posts for section ID: {section_id}", file=sys.stderr, flush=True)
            # Use JavaScript to extract all posts in one call (much faster than sequential queries)
            # IMPORTANT: return a JSON string, not a JS object.
            # With nodriver's deep serialization, JS objects frequently come back as a
            # list-of-pairs structure; JSON.stringify gives us a plain Python `str`.
            result_json = await page.evaluate(f'''
                (function() {{
                    const section = document.querySelector('section[data-id="{section_id}"]');
                    if (!section) {{
                        return JSON.stringify({{debug: "Section not found", posts: [], sample: null}});
                    }}

                    const postElements = section.querySelectorAll('[data-testid="surfacePost"]');

                    const normalize = (s) => {{
                        if (!s) return null;
                        return s.replace(/\\r\\n/g, '\\n').replace(/\\u00a0/g, ' ').trim() || null;
                    }};

                    const getText = (el) => {{
                        if (!el) return null;
                        // Padlet often renders visible text in a way where `textContent`
                        // can be empty/odd; `innerText` matches what you see in DevTools.
                        return normalize(el.innerText || el.textContent || '');
                    }};

                    const posts = Array.from(postElements).map(post => {{
                        // Extract subject
                        const subjectEl = post.querySelector('[data-pw="postSubject"]');
                        const subject = getText(subjectEl);
                        
                        // Extract body with paragraph spacing logic
                        const bodyEl = post.querySelector('[data-pw="postBody"]');
                        let bodyText = null;
                        
                        if (bodyEl) {{
                            const paragraphs = Array.from(bodyEl.querySelectorAll('p'));
                            
                            if (paragraphs.length > 0) {{
                                const parts = [];
                                let prevWasSpacer = false;
                                
                                for (const p of paragraphs) {{
                                    const text = getText(p);
                                    
                                    // Check if this is a spacer paragraph (<p><br></p>)
                                    if (!text) {{
                                        prevWasSpacer = true;
                                        continue;
                                    }}
                                    
                                    // Add spacing before this paragraph (except for the first one)
                                    if (parts.length > 0) {{
                                        if (prevWasSpacer) {{
                                            parts.push('\\n\\n');
                                        }} else {{
                                            parts.push('\\n');
                                        }}
                                    }}
                                    
                                    parts.push(text);
                                    prevWasSpacer = false;
                                }}
                                
                                bodyText = normalize(parts.join(''));
                            }} else {{
                                // Fallback to what is visibly rendered
                                bodyText = getText(bodyEl);
                            }}
                        }}
                        
                        return {{
                            subject: subject,
                            body: bodyText
                        }};
                    }}).filter(post => post.subject || post.body);

                    let sample = null;
                    try {{
                        if (postElements.length) {{
                            const post = postElements[0];
                            const subj = post.querySelector('[data-pw="postSubject"]');
                            const body = post.querySelector('[data-pw="postBody"]');
                            sample = {{
                                postInnerText: normalize((post.innerText || '').slice(0, 400)),
                                postHTML: (post.outerHTML || '').slice(0, 400),
                                subjectFound: !!subj,
                                subjectTextContent: subj ? normalize((subj.textContent || '').slice(0, 200)) : null,
                                subjectInnerText: subj ? normalize((subj.innerText || '').slice(0, 200)) : null,
                                subjectHTML: subj ? (subj.outerHTML || '').slice(0, 250) : null,
                                bodyFound: !!body,
                                bodyTextContent: body ? normalize((body.textContent || '').slice(0, 200)) : null,
                                bodyInnerText: body ? normalize((body.innerText || '').slice(0, 200)) : null,
                                bodyHTML: body ? (body.outerHTML || '').slice(0, 250) : null,
                            }};
                        }}
                    }} catch (e) {{
                        // ignore
                    }}

                    return JSON.stringify({{
                        debug: `Found ${{postElements.length}} post elements, extracted ${{posts.length}} valid posts`,
                        posts: posts,
                        sample: sample
                    }});
                }})()
            ''')

            if not isinstance(result_json, str) or not result_json:
                return []

            result = json.loads(result_json)

            # Convert JSON data to Post objects
            if os.environ.get("PADLET_SCRAPER_DEBUG") == "1":
                try:
                    print(f"Section {section_id} JS debug: {result.get('debug')}", file=sys.stderr, flush=True)
                    print(f"Section {section_id} JS sample: {result.get('sample')}", file=sys.stderr, flush=True)
                except Exception:
                    pass

            posts_data = result.get('posts', []) if isinstance(result, dict) else []
            posts = []
            for post_data in posts_data:
                posts.append(Post(
                    subject=post_data.get('subject') or "Untitled",
                    body=post_data.get('body') or "",
                    section_id=section_id
                ))

            return posts

        except Exception as e:
            print(f"Error extracting posts from section {section_id}: {e}", file=sys.stderr)
            return []



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

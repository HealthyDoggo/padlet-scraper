"""Padlet Scraper - Extract structured data from Padlet boards."""

from .models import Post, Section, Padlet, Link
from .scraper import PadletScraper

__version__ = "0.1.0"
__all__ = ["Post", "Section", "Padlet", "Link", "PadletScraper"]

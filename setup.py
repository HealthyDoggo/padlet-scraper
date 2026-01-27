"""Setup configuration for Padlet Scraper."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="padlet-scraper",
    version="1.0.0",
    description="Tool to scrape Padlets and convert them to readable data types",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sean Cassidy",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "nodriver>=0.37",
        "pydantic>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "padlet-scraper=padlet_scraper.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)

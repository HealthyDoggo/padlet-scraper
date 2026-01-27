"""Utility functions for Padlet scraping."""

import json
from pathlib import Path
from typing import Union
from .models import Padlet


def save_to_json(padlet: Padlet, output_path: Union[str, Path]) -> None:
    """
    Save Padlet data to a JSON file.

    Args:
        padlet: The Padlet object to save
        output_path: Path where the JSON file should be saved
    """
    output_path = Path(output_path)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(padlet.model_dump(), f, indent=2, ensure_ascii=False)


def save_to_markdown(padlet: Padlet, output_path: Union[str, Path]) -> None:
    """
    Save Padlet data to a Markdown file.

    Args:
        padlet: The Padlet object to save
        output_path: Path where the Markdown file should be saved
    """
    output_path = Path(output_path)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(padlet.to_markdown())


def load_from_json(json_path: Union[str, Path]) -> Padlet:
    """
    Load Padlet data from a JSON file.

    Args:
        json_path: Path to the JSON file

    Returns:
        Padlet object
    """
    json_path = Path(json_path)

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return Padlet(**data)

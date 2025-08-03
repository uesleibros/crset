"""
Utility functions for parsing raw data from scraped content.
"""

import re

from app.models.player import Rating


def parse_rating(raw: str) -> Rating:
    """
    Parses a raw string containing a rating and optional delta.

    Args:
        raw: A string such as "78+2" or "85-1" or just "80".

    Returns:
        A Rating object with base and delta values.
    """
    base_match = re.match(r"\d+", raw.strip())
    delta_match = re.search(r"([+-]\d+)", raw.strip())
    base = int(base_match.group()) if base_match else 0
    delta = int(delta_match.group()) if delta_match else 0
    return Rating(base=base, delta=delta)

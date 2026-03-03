"""
Utility functions for the API.
"""

import re                           # Standard: Regex for string cleaning
import os                           # Standard: File path & extension tools
import uuid                         # Standard: Unique identifier generator


def slugify(text: str) -> str:
    """
    Converts 'Boeing 737' to 'boeing-737'.
    """
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text


def generate_record_filename(
    category: str,
    manufacturer: str,
    model: str,
    speed: float,
    original_filename: str
) -> str:
    """
    Builds a SEO-friendly unique filename for records.
    Example output: 'commercial-boeing-737-800-450kts-1a2b3c4d.jpg'
    """
    cat_slug = slugify(category)
    man_slug = slugify(manufacturer)
    mod_slug = slugify(model)
    speed_slug = f"{int(speed)}kts"
    unique_id = str(uuid.uuid4())[:8]
    extension = os.path.splitext(original_filename)[1].lower()

    return f"{cat_slug}-{man_slug}-{mod_slug}-{speed_slug}-{unique_id}{extension}"

"""
Utility functions for string manipulation and file handling.
"""

import re                           # Standard: Regex
import os                           # Standard: Path tools
import uuid                         # Standard: Unique IDs


def slugify(text: str) -> str:
    """
    Converts 'Boeing 737' to 'boeing-737'.
    """
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text


def generate_aircraft_image_filename(
    category: str,
    manufacturer: str, 
    model: str, 
    original_filename: str
) -> str:
    """
    Builds a clean filename for an aircraft's technical photo.
    Format: category-manufacturer-model-[uuid].jpg
    """
    cat_slug = slugify(category)
    man_slug = slugify(manufacturer)
    mod_slug = slugify(model)
    unique_id = str(uuid.uuid4())[:4]
    extension = os.path.splitext(original_filename)[1].lower()

    return f"{cat_slug}-{man_slug}-{mod_slug}-{unique_id}{extension}"


def generate_record_filename(
    category: str,
    manufacturer: str,
    model: str,
    speed: float,
    original_filename: str
) -> str:
    """Builds a SEO-friendly unique filename for records."""
    cat_slug = slugify(category)
    man_slug = slugify(manufacturer)
    mod_slug = slugify(model)
    speed_slug = f"{int(speed)}kts"
    unique_id = str(uuid.uuid4())[:8]
    extension = os.path.splitext(original_filename)[1].lower()

    return f"{cat_slug}-{man_slug}-{mod_slug}-{speed_slug}-{unique_id}{extension}"

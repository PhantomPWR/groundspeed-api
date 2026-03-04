"""
Utility functions for string manipulation and file handling.
"""

import re                           # Standard: Regex for string cleaning
import os                           # Standard: Path and extension tools
import uuid                         # Standard: Unique identifier generator


def slugify(text: str, max_length: int = 50) -> str:
    """
    Converts a string to a URL-friendly slug and clips it to 50 chars.
    Example: 'Boeing 737' -> 'boeing-737'
    """
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)

    # Clip and remove trailing hyphens to ensure filename safety
    return text[:max_length].rstrip('-')


def generate_manufacturer_logo_filename(
    manufacturer: str,
    original_filename: str
) -> str:
    """
    Builds a clean filename for a manufacturer's logo.
    Format: manufacturer-logo-[uuid].ext
    """
    man_slug = slugify(manufacturer)
    unique_id = str(uuid.uuid4())[:4]
    extension = os.path.splitext(original_filename)[1].lower()

    return f"{man_slug}-logo-{unique_id}{extension}"


def generate_aircraft_image_filename(
    category: str,
    manufacturer: str,
    model: str,
    original_filename: str
) -> str:
    """
    Builds a clean filename for an aircraft's technical photo.
    Format: category-manufacturer-model-[uuid].ext
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
    """
    Builds a SEO-friendly unique filename for groundspeed records.
    Format: category-manufacturer-model-speedkt-[uuid].ext
    """
    cat_slug = slugify(category)
    man_slug = slugify(manufacturer)
    mod_slug = slugify(model)
    speed_slug = f"{int(speed)}kt"
    unique_id = str(uuid.uuid4())[:8]
    extension = os.path.splitext(original_filename)[1].lower()

    return f"{cat_slug}-{man_slug}-{mod_slug}-{speed_slug}-{unique_id}{extension}"

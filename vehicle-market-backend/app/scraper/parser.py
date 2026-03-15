"""
HTML parser — extract structured fields from raw ikman.lk listing HTML.
"""

import re
from typing import Optional

from bs4 import BeautifulSoup, Tag

from app.core.logging import logger


# ---------------------------------------------------------------------------
# Listing index page
# ---------------------------------------------------------------------------

def parse_listing_cards(html: str) -> list[dict]:
    """
    Parse a listing index page and return a list of raw listing dicts
    extracted from each ad card.
    """
    soup = BeautifulSoup(html, "lxml")
    cards = soup.select("a[class*='gtm-ad-item']")
    logger.info("Found %d listing cards on page", len(cards))

    listings: list[dict] = []
    for card in cards:
        try:
            data = _parse_card(card)
            if data:
                listings.append(data)
        except Exception as exc:
            logger.debug("Failed to parse card: %s", exc)
    return listings


def _parse_card(card: Tag) -> Optional[dict]:
    """Extract fields from a single listing card element."""
    href = card.get("href", "")
    if not href or "/ad/" not in str(href):
        return None

    # Build full URL
    source_url = href if str(href).startswith("http") else f"https://ikman.lk{href}"

    # Title — usually in an <h2> tag
    title_tag = card.select_one("h2")
    title = title_tag.get_text(strip=True) if title_tag else ""

    # Get all visible text from the card to extract price, mileage, location
    card_text = card.get_text(" | ", strip=True)

    # Price — pattern: Rs X,XXX,XXX or Rs X,XXX
    price_raw = _extract_pattern(card_text, r"Rs[\s.]*([\d,]+)")

    # Mileage — pattern: X,XXX km
    mileage_raw = _extract_pattern(card_text, r"([\d,]+)\s*km")

    # Location and category — usually after mileage, format: "Location, Category"
    location = ""
    category = ""
    # Look for known Sri Lankan district names
    _districts = [
        "Colombo", "Gampaha", "Kalutara", "Kandy", "Matale", "Nuwara Eliya",
        "Galle", "Matara", "Hambantota", "Jaffna", "Kilinochchi", "Mannar",
        "Mullaitivu", "Vavuniya", "Batticaloa", "Ampara", "Trincomalee",
        "Kurunegala", "Puttalam", "Anuradhapura", "Polonnaruwa", "Badulla",
        "Monaragala", "Ratnapura", "Kegalle",
    ]
    for district in _districts:
        if district in card_text:
            location = district
            break

    # Category — look for known vehicle categories
    _categories = [
        "Cars", "Motorbikes", "Vans", "Three Wheelers", "Lorries",
        "Buses", "Bicycles", "Auto Parts & Accessories", "Rentals",
        "SUVs", "Crew Cabs", "Other Vehicles",
    ]
    for cat in _categories:
        if cat in card_text:
            category = cat
            break

    if not title:
        return None

    return {
        "title": title,
        "price_raw": price_raw or "",
        "mileage_raw": mileage_raw or "",
        "location": location,
        "category": category,
        "source_url": source_url,
    }


# ---------------------------------------------------------------------------
# Individual listing detail page
# ---------------------------------------------------------------------------

def parse_listing_detail(html: str) -> dict:
    """
    Parse a single ad detail page and return a dict with all available fields.
    """
    soup = BeautifulSoup(html, "lxml")
    data: dict = {}

    # Title
    title_tag = soup.select_one("h1")
    if title_tag:
        data["title"] = title_tag.get_text(strip=True)

    # Price
    price_text = ""
    for el in soup.find_all(string=re.compile(r"Rs\s*[\d,]+")):
        price_text = el.strip()
        break
    data["price_raw"] = _extract_pattern(price_text, r"Rs[\s.]*([\d,]+)") or ""

    # Description
    desc_section = soup.find("h2", string=re.compile(r"Description", re.I))
    if desc_section:
        desc_div = desc_section.find_next_sibling()
        if desc_div:
            data["description"] = desc_div.get_text(strip=True)

    # Vehicle attributes — usually in a structured list/table
    # Look for attribute labels and their values
    _attr_map = {
        "Brand": "make",
        "Model": "model",
        "Year of Manufacture": "year_raw",
        "Condition": "condition",
        "Transmission": "transmission",
        "Fuel type": "fuel_type",
        "Engine capacity": "engine_capacity",
        "Mileage": "mileage_raw",
    }

    # Try multiple selector strategies for attribute extraction
    # Strategy 1: Look for label-value pairs in spans/divs
    all_text_elements = soup.find_all(["span", "div", "td", "dt", "dd", "li"])
    for label_text, field_name in _attr_map.items():
        for el in all_text_elements:
            el_text = el.get_text(strip=True)
            if el_text == label_text:
                # Get the next sibling or parent's next child with the value
                value_el = el.find_next_sibling()
                if value_el:
                    data[field_name] = value_el.get_text(strip=True)
                    break
                # Try parent's next sibling
                parent = el.parent
                if parent:
                    next_sib = parent.find_next_sibling()
                    if next_sib:
                        data[field_name] = next_sib.get_text(strip=True)
                        break

    # Strategy 2: Look for meta-like attribute elements
    meta_links = soup.select("a[class*='ad-meta']")
    if meta_links:
        for link in meta_links:
            text = link.get_text(strip=True)
            href = link.get("href", "")
            if "brand" in str(href).lower() or "make" in str(href).lower():
                data.setdefault("make", text)
            elif "model" in str(href).lower():
                data.setdefault("model", text)

    # Location
    location_el = soup.select_one("span[class*='location']")
    if location_el:
        data["location"] = location_el.get_text(strip=True)

    # Image URLs
    images = []
    for img in soup.select("img[src*='ikman']"):
        src = img.get("src", "")
        if src and "ad-image" in src or "listing" in src:
            images.append(src)
    # Also check for lazy-loaded images
    for img in soup.select("img[data-src]"):
        src = img.get("data-src", "")
        if src:
            images.append(src)
    data["image_urls"] = list(set(images))

    return data


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _extract_pattern(text: str, pattern: str) -> Optional[str]:
    """Extract the first capture group matching ``pattern`` from ``text``."""
    match = re.search(pattern, text)
    return match.group(1) if match else None

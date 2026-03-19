"""
HTML parser — extract structured fields from raw ikman.lk listing HTML.
"""

import re
from datetime import date, datetime, timedelta
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

    _categories = [
        "Cars", "Motorbikes", "Vans", "Three Wheelers", "Lorries",
        "Buses", "Bicycles", "Auto Parts & Accessories", "Rentals",
        "SUVs", "Crew Cabs", "Other Vehicles",
    ]
    for cat in _categories:
        if cat in card_text:
            category = cat
            break

    # Posted date — ikman shows relative dates like "Today", "Yesterday", "3 days ago", etc.
    posted_date_raw = _extract_posted_date(card_text)

    if not title:
        return None

    return {
        "title": title,
        "price_raw": price_raw or "",
        "mileage_raw": mileage_raw or "",
        "location": location,
        "category": category,
        "source_url": source_url,
        "posted_date_raw": posted_date_raw or "",
    }


# ---------------------------------------------------------------------------
# Posted date extraction
# ---------------------------------------------------------------------------

def _extract_posted_date(text: str) -> Optional[str]:
    """
    Extract posted date from card text.

    ikman.lk shows relative dates:
      - "Today"           → today's date
      - "Yesterday"       → yesterday's date
      - "X days ago"      → date X days ago
      - "X weeks ago"     → date X * 7 days ago
      - "X months ago"    → date X * 30 days ago
      - "Jan 15"          → absolute date (current year assumed)
      - "2025 Jan 15"     → absolute date

    Returns ISO date string (YYYY-MM-DD) or None.
    """
    today = date.today()

    lower = text.lower()

    if "today" in lower:
        return today.isoformat()

    if "yesterday" in lower:
        return (today - timedelta(days=1)).isoformat()

    # "X days ago"
    days_match = re.search(r"(\d+)\s*days?\s*ago", lower)
    if days_match:
        return (today - timedelta(days=int(days_match.group(1)))).isoformat()

    # "X weeks ago"
    weeks_match = re.search(r"(\d+)\s*weeks?\s*ago", lower)
    if weeks_match:
        return (today - timedelta(weeks=int(weeks_match.group(1)))).isoformat()

    # "X months ago"
    months_match = re.search(r"(\d+)\s*months?\s*ago", lower)
    if months_match:
        return (today - timedelta(days=int(months_match.group(1)) * 30)).isoformat()

    # Absolute date: "Jan 15" or "2025 Jan 15"
    _months = {
        "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
        "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
    }
    abs_match = re.search(r"(\d{4})?\s*(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+(\d{1,2})", lower)
    if abs_match:
        yr = int(abs_match.group(1)) if abs_match.group(1) else today.year
        mo = _months[abs_match.group(2)]
        dy = int(abs_match.group(3))
        try:
            return date(yr, mo, dy).isoformat()
        except ValueError:
            pass

    return None


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

    # Vehicle attributes
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

    all_text_elements = soup.find_all(["span", "div", "td", "dt", "dd", "li"])
    for label_text, field_name in _attr_map.items():
        for el in all_text_elements:
            el_text = el.get_text(strip=True)
            if el_text == label_text:
                value_el = el.find_next_sibling()
                if value_el:
                    data[field_name] = value_el.get_text(strip=True)
                    break
                parent = el.parent
                if parent:
                    next_sib = parent.find_next_sibling()
                    if next_sib:
                        data[field_name] = next_sib.get_text(strip=True)
                        break

    # Location
    location_el = soup.select_one("span[class*='location']")
    if location_el:
        data["location"] = location_el.get_text(strip=True)

    # Posted date from detail page
    full_text = soup.get_text(" ", strip=True)
    posted = _extract_posted_date(full_text)
    if posted:
        data["posted_date_raw"] = posted

    return data


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _extract_pattern(text: str, pattern: str) -> Optional[str]:
    """Extract the first capture group matching ``pattern`` from ``text``."""
    match = re.search(pattern, text)
    return match.group(1) if match else None

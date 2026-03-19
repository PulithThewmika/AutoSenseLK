"""
Brand + model registry for ikman.lk Sri Lanka.

Provides:
  - BRAND_MODELS: dict mapping brand slug → list of (model_display, model_slug) tuples
  - Helpers to build brand-level and model-level scrape URLs
  - Condition constants
"""

from __future__ import annotations

BASE_URL = "https://ikman.lk"

# Vehicle conditions on ikman.lk
CONDITIONS: list[str] = ["used", "brand_new", "reconditioned"]

CONDITION_URL_MAP: dict[str, str] = {
    "used": "used",
    "brand_new": "brand_new",
    "reconditioned": "reconditioned",
}


def _slug(name: str) -> str:
    """Convert display name to URL slug: 'Land Cruiser Sahara' → 'land-cruiser-sahara'."""
    return name.strip().lower().replace(" ", "-")


def _models(names: list[str]) -> list[tuple[str, str]]:
    """Return list of (display_name, url_slug) pairs."""
    return [(n, _slug(n)) for n in names]


# ── Brand → Model registry ─────────────────────────────────────────────────
# Each entry: brand_slug → list of (display_name, url_slug)

BRAND_MODELS: dict[str, list[tuple[str, str]]] = {

    "toyota": _models([
        "Aqua", "Land Cruiser Sahara", "Prius", "Premio", "Yaris Cross", "Allion",
        "Harrier", "CHR", "Passo", "Carina", "Yaris Ativ", "RAV4", "Alphard", "Voxy",
        "Other Model", "Starlet", "Urban Cruiser", "Belta", "Corona", "Fortuner",
        "Rush", "Vellfire", "Vios", "Camry", "Crown", "Land Cruiser", "Sprinter",
        "Tercel", "Pixis", "Avanza", "Wigo", "Soluna", "Corsa", "Hyryder", "Caldina",
        "IST", "Mark", "Noah", "Sienta", "Vanguard", "Cami", "Fielder", "FJ Cruiser",
        "Hyryder V", "Land Cruiser 79", "Supra", "Tank", "UrbanCruiser Hyryder",
        "Veloz", "Verossa", "Auris", "Duet", "Esquire", "Estima", "Etios", "Progres",
        "Ractis", "TUNDRA", "Wish",
        # From user-provided example URLs
        "Raize", "Land Cruiser Prado", "Hilux", "Yaris", "Corolla", "Vitz",
        "Taisor", "Axio", "Roomy",
    ]),

    "honda": _models([
        "Vezel", "CRV", "Fit", "Civic", "City", "Grace", "N-Box", "Freed",
        "Fit Shuttle", "N-WGN", "ZRV Z", "Insight", "Fit Aria", "WR-V", "Accord",
        "HR-V", "S660", "Amaze", "Crossroad", "CRZ", "Fit She's", "Jade",
        "Step Wagon", "Airwave", "Integra", "Jazz",
    ]),

    "suzuki": _models([
        "Alto", "Wagon R", "Spacia", "Wagon R FX", "Swift", "Maruti", "Celerio",
        "Wagon R Stingray", "Wagon R FZ", "Wagon R ZX", "Hustler", "Fronx", "XBee",
        "A-Star", "Baleno", "Vitara", "Grand Vitara", "S-Cross", "Jimny", "Zen",
        "Ertiga", "Escudo", "Esteem", "Liana", "Cultus", "Estilo", "SX4", "Dzire",
    ]),

    "nissan": _models([
        "Sunny", "Dayz", "X-Trail", "Magnite", "March", "Roox", "Almera", "Leaf",
        "AD Wagon", "Clipper", "Tiida", "Dutsun", "ROOX HIGHWAY STAR X", "Serena",
        "Wingroad", "Qashqai", "Patrol", "Aura", "Bluebird", "Juke", "Navara",
        "Pulsar", "Cefiro", "Double cab", "Note", "Sakura", "Primera", "Dualis",
        "GT-R", "Teana", "Cube", "Lafesta", "Presea", "Sylphy", "Tekna",
    ]),

    "mercedes-benz": _models([
        "C200", "GLB", "E200", "C180", "CLA 180", "CLA 200", "E350", "E300",
        "A180", "S400", "CLA 250", "GLE 300D", "C300", "G Wagon", "E220", "S350",
        "C350", "S500", "A250", "C220", "E180", "EQS 450", "G400d", "GLA 180",
        "S300", "C160", "EQB", "GLA 200", "GLE 400", "B250e", "CLS", "EQE 300",
        "GLC 250", "Vito", "190D", "A140", "A200", "C230", "C250", "CLA45",
        "E240", "E250", "G450d", "GLC 300", "GLS 600", "S560", "W123",
    ]),

    "mitsubishi": _models([
        "Lancer", "Montero", "eK Wagon", "Outlander", "L200", "Eclipse Cross",
        "Pajero", "4DR", "EK Custom", "Mirage", "Triton GSR", "Galant", "Xpander",
        "eK Space", "ASX", "Attrage", "Delica", "Libero", "Strada", "i-MiEV",
        "RVR", "Sportero", "Towny",
    ]),

    "land-rover": _models([
        "Defender", "Range Rover", "Discovery", "Range Rover Sport",
        "Range Rover Evoque", "Freelander", "Discovery Sport",
        "Range Rover Velar", "Range Rover PHEV",
    ]),

    "daihatsu": _models([
        "Mira", "Taft", "Rocky", "Charade", "Thor", "Terios", "Hijet", "Move",
        "Tanto", "Boon", "Cast Activa", "Cuore", "Canbus", "Charmant", "Copen",
        "Altis", "Wake",
    ]),

    "audi": _models([
        "A3", "Q2", "Q3", "Q7", "A4", "A1", "A5", "A6", "e-tron",
        "Q5", "Q4 E-Tron S Line", "Q4", "80",
    ]),

    "bmw": _models([
        "X1", "318i", "X5", "520d", "218i", "523i", "740Le", "530e", "520i",
        "X3", "220i", "X2", "320d", "X5 eDrive", "525i", "740Li", "i7",
        "Mini Cooper", "225XE", "420i", "528i", "740e", "740i", "i3", "X5 M",
        "ActiveHybrid 7", "i5", "118i", "120i", "220d", "316i", "318ti", "320i",
        "335i", "420d", "430i", "530d", "725D", "730d", "730Ld", "750iL",
        "E90", "i4", "i8", "M3", "M5", "M760Li", "X6 M", "X7", "Z4",
    ]),

    "kia": _models([
        "Sonet", "Sorento", "Sportage", "Picanto", "Syros", "Carens", "Rio",
        "Seltos", "EV5", "Mentor", "Spectra", "Stonic", "Carnival", "Cerato",
        "Clarus", "Optima", "Sephia",
    ]),
}

# Brands without model-level data yet (fall back to brand-level crawl)
_BRAND_ONLY: list[str] = [
    "hyundai", "ford", "micro", "dfsk", "mazda", "perodua", "peugeot", "tata",
    "volkswagen", "mahindra", "mg", "maruti-suzuki", "lexus", "renault", "jeep",
    "ssang-yong", "mini", "chery", "byd", "porsche", "jaguar", "bajaj", "volvo",
    "zotye", "subaru", "austin", "morris", "daewoo", "isuzu", "proton", "baic",
    "bentley", "lamborghini", "tesla", "fiat", "aston-martin", "datsun",
    "chrysler", "jac", "maruti", "skoda", "alfa-romeo", "baw", "dodge",
]

# All known brands (those with model data + brand-only)
BRANDS: list[str] = list(BRAND_MODELS.keys()) + _BRAND_ONLY


def build_model_url(
    brand: str,
    model_slug: str,
    *,
    condition: str | None = None,
    page: int = 1,
) -> str:
    """
    Build model-specific URL.

    Pattern: /en/ads/sri-lanka/cars/{brand}/{model}?tree.brand={brand}_{brand}-{model}

    Example:
        build_model_url("toyota", "aqua")
        → https://ikman.lk/en/ads/sri-lanka/cars/toyota/aqua?tree.brand=toyota_toyota-aqua
    """
    tree = f"{brand}_{brand}-{model_slug}"
    url = f"{BASE_URL}/en/ads/sri-lanka/cars/{brand}/{model_slug}?tree.brand={tree}"

    if condition and condition in CONDITION_URL_MAP:
        url += f"&enum.condition={CONDITION_URL_MAP[condition]}"

    if page > 1:
        url += f"&page={page}"

    return url


def build_brand_url(
    brand: str,
    *,
    condition: str | None = None,
    page: int = 1,
) -> str:
    """
    Build brand-level URL (used for brands without model data yet).

    Example:
        build_brand_url("honda")
        → https://ikman.lk/en/ads/sri-lanka/cars/honda?tree.brand=honda
    """
    url = f"{BASE_URL}/en/ads/sri-lanka/cars/{brand}?tree.brand={brand}"

    if condition and condition in CONDITION_URL_MAP:
        url += f"&enum.condition={CONDITION_URL_MAP[condition]}"

    if page > 1:
        url += f"&page={page}"

    return url


def brand_display_name(slug: str) -> str:
    """'mercedes-benz' → 'Mercedes-Benz'."""
    return "-".join(word.capitalize() for word in slug.split("-"))

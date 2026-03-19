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

    # ─── Toyota (68 models) ────────────────────────────────────────────────
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
        "Raize", "Land Cruiser Prado", "Hilux", "Yaris", "Corolla", "Vitz",
        "Taisor", "Axio", "Roomy",
    ]),

    # ─── Honda (26 models) ─────────────────────────────────────────────────
    "honda": _models([
        "Vezel", "CRV", "Fit", "Civic", "City", "Grace", "N-Box", "Freed",
        "Fit Shuttle", "N-WGN", "ZRV Z", "Insight", "Fit Aria", "WR-V", "Accord",
        "HR-V", "S660", "Amaze", "Crossroad", "CRZ", "Fit She's", "Jade",
        "Step Wagon", "Airwave", "Integra", "Jazz",
    ]),

    # ─── Suzuki (28 models) ────────────────────────────────────────────────
    "suzuki": _models([
        "Alto", "Wagon R", "Spacia", "Wagon R FX", "Swift", "Maruti", "Celerio",
        "Wagon R Stingray", "Wagon R FZ", "Wagon R ZX", "Hustler", "Fronx", "XBee",
        "A-Star", "Baleno", "Vitara", "Grand Vitara", "S-Cross", "Jimny", "Zen",
        "Ertiga", "Escudo", "Esteem", "Liana", "Cultus", "Estilo", "SX4", "Dzire",
    ]),

    # ─── Nissan (35 models) ────────────────────────────────────────────────
    "nissan": _models([
        "Sunny", "Dayz", "X-Trail", "Magnite", "March", "Roox", "Almera", "Leaf",
        "AD Wagon", "Clipper", "Tiida", "Dutsun", "ROOX HIGHWAY STAR X", "Serena",
        "Wingroad", "Qashqai", "Patrol", "Aura", "Bluebird", "Juke", "Navara",
        "Pulsar", "Cefiro", "Double cab", "Note", "Sakura", "Primera", "Dualis",
        "GT-R", "Teana", "Cube", "Lafesta", "Presea", "Sylphy", "Tekna",
    ]),

    # ─── Mercedes-Benz (47 models) ─────────────────────────────────────────
    "mercedes-benz": _models([
        "C200", "GLB", "E200", "C180", "CLA 180", "CLA 200", "E350", "E300",
        "A180", "S400", "CLA 250", "GLE 300D", "C300", "G Wagon", "E220", "S350",
        "C350", "S500", "A250", "C220", "E180", "EQS 450", "G400d", "GLA 180",
        "S300", "C160", "EQB", "GLA 200", "GLE 400", "B250e", "CLS", "EQE 300",
        "GLC 250", "Vito", "190D", "A140", "A200", "C230", "C250", "CLA45",
        "E240", "E250", "G450d", "GLC 300", "GLS 600", "S560", "W123",
    ]),

    # ─── Mitsubishi (23 models) ────────────────────────────────────────────
    "mitsubishi": _models([
        "Lancer", "Montero", "eK Wagon", "Outlander", "L200", "Eclipse Cross",
        "Pajero", "4DR", "EK Custom", "Mirage", "Triton GSR", "Galant", "Xpander",
        "eK Space", "ASX", "Attrage", "Delica", "Libero", "Strada", "i-MiEV",
        "RVR", "Sportero", "Towny",
    ]),

    # ─── Land Rover (9 models) ─────────────────────────────────────────────
    "land-rover": _models([
        "Defender", "Range Rover", "Discovery", "Range Rover Sport",
        "Range Rover Evoque", "Freelander", "Discovery Sport",
        "Range Rover Velar", "Range Rover PHEV",
    ]),

    # ─── Daihatsu (17 models) ──────────────────────────────────────────────
    "daihatsu": _models([
        "Mira", "Taft", "Rocky", "Charade", "Thor", "Terios", "Hijet", "Move",
        "Tanto", "Boon", "Cast Activa", "Cuore", "Canbus", "Charmant", "Copen",
        "Altis", "Wake",
    ]),

    # ─── Audi (13 models) ──────────────────────────────────────────────────
    "audi": _models([
        "A3", "Q2", "Q3", "Q7", "A4", "A1", "A5", "A6", "e-tron",
        "Q5", "Q4 E-Tron S Line", "Q4", "80",
    ]),

    # ─── BMW (50 models) ───────────────────────────────────────────────────
    "bmw": _models([
        "X1", "318i", "X5", "520d", "218i", "523i", "740Le", "530e", "520i",
        "X3", "220i", "X2", "320d", "X5 eDrive", "525i", "740Li", "i7",
        "Mini Cooper", "225XE", "420i", "528i", "740e", "740i", "i3", "X5 M",
        "ActiveHybrid 7", "i5", "118i", "120i", "220d", "316i", "318ti", "320i",
        "335i", "420d", "430i", "530d", "725D", "730d", "730Ld", "750iL",
        "E90", "i4", "i8", "M3", "M5", "M760Li", "X6 M", "X7", "Z4",
    ]),

    # ─── Kia (17 models) ───────────────────────────────────────────────────
    "kia": _models([
        "Sonet", "Sorento", "Sportage", "Picanto", "Syros", "Carens", "Rio",
        "Seltos", "EV5", "Mentor", "Spectra", "Stonic", "Carnival", "Cerato",
        "Clarus", "Optima", "Sephia",
    ]),

    # ─── Hyundai (16 models) ───────────────────────────────────────────────
    "hyundai": _models([
        "Venue", "Santa Fe", "Eon", "Tucson", "Accent", "Sonata", "Elantra",
        "Matrix", "Stellar", "Grand i10", "Alcazar", "Creta", "Getz", "Santro",
        "i20", "Palisade",
    ]),

    # ─── Ford (12 models) ──────────────────────────────────────────────────
    "ford": _models([
        "Raptor Ranger", "Ranger", "Mustang", "Laser", "Focus", "Fiesta",
        "Ecosport", "Everest", "Festiva", "GT", "Kuga", "Mondeo",
    ]),

    # ─── Micro (15 models) ─────────────────────────────────────────────────
    "micro": _models([
        "Panda", "Panda Cross", "Rexton", "Actyon", "MX 7", "Kyron", "Tivoli",
        "Trend", "Almaz", "Geely", "Korondo", "Chery Tiggo Pro4", "Lifan",
        "Privilege", "X25",
    ]),

    # ─── DFSK (1 model) ───────────────────────────────────────────────────
    "dfsk": _models(["Glory"]),

    # ─── Perodua (6 models) ────────────────────────────────────────────────
    "perodua": _models([
        "Axia", "Viva Elite", "Bezza", "Kenari", "Kelisa", "Kancil",
    ]),

    # ─── Mazda (11 models) ─────────────────────────────────────────────────
    "mazda": _models([
        "Familia", "Flair", "Axela", "3", "6", "Butterfly", "Demio",
        "2 Skyactive", "CX-5", "Tribute", "Roadster",
    ]),

    # ─── Peugeot (12 models) ───────────────────────────────────────────────
    "peugeot": _models([
        "5008", "3008", "408", "2008", "407", "508", "308", "406",
        "505", "305", "405", "E-2008",
    ]),

    # ─── Tata (9 models) ───────────────────────────────────────────────────
    "tata": _models([
        "Nano", "Indica", "Indigo", "GenX Nano", "Nexon", "Sumo",
        "Curvv", "Safari", "Xenon",
    ]),

    # ─── Volkswagen (11 models) ────────────────────────────────────────────
    "volkswagen": _models([
        "T-Cross", "Polo", "Beetle", "Taigun", "Golf", "Tiguan", "ID",
        "Jetta", "Passat", "ID-4 STYLISH", "ID 5 | Pro",
    ]),

    # ─── MG (9 models) ─────────────────────────────────────────────────────
    "mg": _models([
        "ZS", "HS Hybrid+", "MG4 X", "MG4 Electric", "Other Model",
        "5 Long Range", "6", "Hector Plus", "MG4 V Long Range",
    ]),

    # ─── Mahindra (6 models) ───────────────────────────────────────────────
    "mahindra": _models([
        "Scorpio Pikup", "KUV 100", "Scorpio", "Bolero", "e2o", "Thar",
    ]),

    # ─── Maruti Suzuki (5 models) ──────────────────────────────────────────
    "maruti-suzuki": _models([
        "800", "Alto", "WagonR", "Zen", "Gypsy",
    ]),

    # ─── Lexus (13 models) ─────────────────────────────────────────────────
    "lexus": _models([
        "LX600", "GX550", "LBX", "RX450h", "LS600h", "RX350", "RX400",
        "HS250H", "Land Cruiser", "LS500h", "LX500d", "LX570", "NX",
    ]),

    # ─── Jeep (6 models) ───────────────────────────────────────────────────
    "jeep": _models([
        "Compass", "Wrangler", "Gladiator Rubicon", "Grand Cherokee",
        "Renegade", "Cherokee",
    ]),

    # ─── Renault (2 models) ────────────────────────────────────────────────
    "renault": _models(["KWID", "Kiger Emotion"]),

    # ─── SsangYong (7 models) ──────────────────────────────────────────────
    "ssang-yong": _models([
        "Rexton", "Korando", "Kyron", "Actyon", "Tivoli",
        "KGM Torres EVX", "Musso",
    ]),

    # ─── Mini (3 models) ───────────────────────────────────────────────────
    "mini": _models(["Cooper", "Countryman", "Clubman"]),

    # ─── Chery (3 models) ──────────────────────────────────────────────────
    "chery": _models(["QQ", "QQ3", "Tiggo 4 Pro"]),

    # ─── BYD (5 models) ────────────────────────────────────────────────────
    "byd": _models(["Sealion 6", "ATTO 3", "Seal", "ATTO 1", "Shark 6"]),

    # ─── Porsche (6 models) ────────────────────────────────────────────────
    "porsche": _models([
        "Cayenne", "Panamera", "718 Cayman", "911 Carrera", "718 Boxter", "Taycan",
    ]),

    # ─── Jaguar (8 models) ─────────────────────────────────────────────────
    "jaguar": _models([
        "F-Pace", "X-Type", "XF", "E-Pace", "F-Type", "I-Pace", "XE", "XJ",
    ]),

    # ─── Volvo (6 models) ──────────────────────────────────────────────────
    "volvo": _models(["XC90", "940", "S40", "S90", "XC40", "XC60"]),

    # ─── Subaru (5 models) ─────────────────────────────────────────────────
    "subaru": _models(["XV", "Forester", "Legacy", "R2", "STI"]),

    # ─── Austin (3 models) ─────────────────────────────────────────────────
    "austin": _models(["All models", "Mini Cooper", "Mini"]),

    # ─── Chevrolet (4 models) ──────────────────────────────────────────────
    "chevrolet": _models(["Cruze", "Aveo", "Camaro", "Corvette"]),

    # ─── Morris (1 model) ──────────────────────────────────────────────────
    "morris": _models(["Minor"]),

    # ─── Zotye (2 models) ──────────────────────────────────────────────────
    "zotye": _models(["Z100", "Nomad"]),

    # ─── BAIC (1 model) ────────────────────────────────────────────────────
    "baic": _models(["X55 II"]),

    # ─── Daewoo (2 models) ─────────────────────────────────────────────────
    "daewoo": _models(["Nubira", "Espero"]),

    # ─── Isuzu (4 models) ──────────────────────────────────────────────────
    "isuzu": _models(["Gemini", "D-Max", "MU-X", "Panther"]),

    # ─── Proton (4 models) ─────────────────────────────────────────────────
    "proton": _models(["Wira", "Saga", "Savvy", "Waja"]),

    # ─── Lamborghini (1 model) ─────────────────────────────────────────────
    "lamborghini": _models(["Urus"]),

    # ─── Tesla (2 models) ──────────────────────────────────────────────────
    "tesla": _models(["Model 3", "Model Y"]),

    # ─── Bentley (2 models) ────────────────────────────────────────────────
    "bentley": _models(["Flying Spur", "Bentayga"]),

    # ─── Fiat (2 models) ───────────────────────────────────────────────────
    "fiat": _models(["Punto", "Linea"]),

    # ─── Datsun (1 model) ──────────────────────────────────────────────────
    "datsun": _models(["Redi Go"]),

    # ─── Aston Martin (2 models) ───────────────────────────────────────────
    "aston-martin": _models(["DB11", "DB12 Volante"]),

    # ─── Chrysler (1 model) ────────────────────────────────────────────────
    "chrysler": _models(["300"]),

    # ─── JAC (1 model) ─────────────────────────────────────────────────────
    "jac": _models(["T9"]),

    # ─── Skoda (1 model) ───────────────────────────────────────────────────
    "skoda": _models(["Karoq"]),

    # ─── BAW (1 model) ─────────────────────────────────────────────────────
    "baw": _models(["E7"]),

    # ─── Dodge (1 model) ───────────────────────────────────────────────────
    "dodge": _models(["Challenger"]),
}

# Brands without model-level data yet (fall back to brand-level crawl)
_BRAND_ONLY: list[str] = [
    "bajaj", "maruti", "alfa-romeo",
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

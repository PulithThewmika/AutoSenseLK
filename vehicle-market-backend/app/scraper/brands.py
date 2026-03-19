"""
Brand registry — all known vehicle brands on ikman.lk with URL helpers.
"""

# Complete list of brands available on ikman.lk Sri Lanka
BRANDS: list[str] = [
    "toyota", "honda", "suzuki", "nissan", "mercedes-benz",
    "mitsubishi", "daihatsu", "land-rover", "audi", "bmw",
    "kia", "hyundai", "ford", "micro", "dfsk",
    "mazda", "perodua", "peugeot", "tata", "volkswagen",
    "mahindra", "mg", "maruti-suzuki", "lexus", "renault",
    "jeep", "ssang-yong", "mini", "chery", "byd",
    "porsche", "jaguar", "bajaj", "volvo", "zotye",
    "subaru", "austin", "morris", "daewoo", "isuzu",
    "proton", "baic", "bentley", "lamborghini", "tesla",
    "fiat", "aston-martin", "datsun", "chrysler", "jac",
    "maruti", "skoda", "alfa-romeo", "baw", "dodge",
]

# Vehicle conditions on ikman.lk
CONDITIONS: list[str] = ["used", "brand_new", "reconditioned"]

# ikman.lk condition URL values (enum.condition parameter)
CONDITION_URL_MAP: dict[str, str] = {
    "used": "used",
    "brand_new": "brand_new",
    "reconditioned": "reconditioned",
}

BASE_URL = "https://ikman.lk"


def build_brand_url(
    brand: str,
    *,
    condition: str | None = None,
    page: int = 1,
) -> str:
    """
    Build ikman.lk listing URL for a specific brand.

    Examples:
        build_brand_url("toyota")
        → https://ikman.lk/en/ads/sri-lanka/cars/toyota?tree.brand=toyota&page=1

        build_brand_url("honda", condition="used", page=2)
        → https://ikman.lk/en/ads/sri-lanka/cars/honda?tree.brand=honda&enum.condition=used&page=2
    """
    url = f"{BASE_URL}/en/ads/sri-lanka/cars/{brand}?tree.brand={brand}"

    if condition and condition in CONDITION_URL_MAP:
        url += f"&enum.condition={CONDITION_URL_MAP[condition]}"

    if page > 1:
        url += f"&page={page}"

    return url


def brand_display_name(slug: str) -> str:
    """Convert URL slug to display name: 'mercedes-benz' → 'Mercedes-Benz'."""
    return slug.replace("-", " ").title().replace(" ", "-") if "-" in slug else slug.title()

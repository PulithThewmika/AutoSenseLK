"""
Makes & Models seeder.

Seeds the `makes` and `models` MongoDB collections from the brand-model
registry in brands.py. Safe to re-run (upserts by slug).
"""

from __future__ import annotations

from app.core.logging import logger
from app.models.vehicle import Make, Model
from app.scraper.brands import (
    BRAND_MODELS, _BRAND_ONLY,
    build_brand_url, build_model_url, brand_display_name,
)


async def seed_makes_and_models() -> dict:
    """
    Upsert all known makes and their models into MongoDB.

    Returns summary stats.
    """
    makes_upserted = 0
    models_upserted = 0

    all_brands = list(BRAND_MODELS.keys()) + list(_BRAND_ONLY)

    for brand_slug in all_brands:
        display = brand_display_name(brand_slug)
        brand_url = build_brand_url(brand_slug)

        # Upsert Make
        existing_make = await Make.find_one(Make.slug == brand_slug)
        if existing_make:
            existing_make.name = display
            existing_make.scrape_url = brand_url
            await existing_make.save()
        else:
            await Make(name=display, slug=brand_slug, scrape_url=brand_url).insert()
        makes_upserted += 1

        # Upsert Models (only for brands with model data)
        if brand_slug not in BRAND_MODELS:
            continue

        for model_display, model_slug in BRAND_MODELS[brand_slug]:
            model_url = build_model_url(brand_slug, model_slug)

            existing_model = await Model.find_one(
                Model.make_slug == brand_slug,
                Model.slug == model_slug,
            )
            if existing_model:
                existing_model.name = model_display
                existing_model.scrape_url = model_url
                await existing_model.save()
            else:
                await Model(
                    name=model_display,
                    slug=model_slug,
                    make_slug=brand_slug,
                    scrape_url=model_url,
                ).insert()
            models_upserted += 1

    logger.info("Seeded %d makes, %d models", makes_upserted, models_upserted)
    return {"makes": makes_upserted, "models": models_upserted}

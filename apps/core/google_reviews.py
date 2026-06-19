"""Home-page guest review helpers (DB-backed, seeded or synced via sync_google_reviews)."""

from __future__ import annotations

from typing import Any

from django.conf import settings
from django.core.cache import cache

from .models import GuestReview, SiteSettings

CACHE_META_KEY = 'google_place_reviews_meta'
CACHE_TTL = 60 * 60 * 6


def get_reviews_meta() -> dict[str, Any]:
    cached = cache.get(CACHE_META_KEY)
    if cached:
        return cached

    site = SiteSettings.load()
    meta = {
        'rating': float(site.google_rating) if site.google_rating is not None else None,
        'count': site.google_review_count,
        'maps_url': (
            site.google_maps_reviews_url
            or site.map_url
            or getattr(settings, 'SITE_MAPS_URL', '')
        ),
    }
    if meta['rating'] is not None:
        cache.set(CACHE_META_KEY, meta, CACHE_TTL)
    return meta


def get_home_reviews(limit: int = 6) -> list[GuestReview]:
    qs = GuestReview.objects.filter(is_active=True).order_by('order', '-published_at', 'pk')
    return list(qs[:limit])

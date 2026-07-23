"""Google Places API (New) helpers for guest review sync."""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from typing import Any

from django.conf import settings

PLACES_BASE = 'https://places.googleapis.com/v1/places'
SEARCH_TEXT_URL = 'https://places.googleapis.com/v1/places:searchText'

DEFAULT_TEXT_QUERY = (
    'Black Diamond Spa Opletalova 1566/30 Praha'
)


def _api_key() -> str:
    return (os.getenv('GOOGLE_PLACES_API_KEY') or getattr(settings, 'GOOGLE_PLACES_API_KEY', '') or '').strip()


def place_id_from_env() -> str:
    return (os.getenv('GOOGLE_PLACE_ID') or getattr(settings, 'GOOGLE_PLACE_ID', '') or '').strip()


def text_query_from_settings() -> str:
    return (
        os.getenv('GOOGLE_PLACE_QUERY')
        or getattr(settings, 'GOOGLE_PLACE_QUERY', '')
        or DEFAULT_TEXT_QUERY
    ).strip()


def resolve_place_id(api_key: str, text_query: str | None = None) -> str:
    """Resolve Place ID via Text Search when GOOGLE_PLACE_ID is not set."""
    query = (text_query or text_query_from_settings()).strip()
    body = json.dumps({'textQuery': query, 'languageCode': 'cs'}).encode('utf-8')
    request = urllib.request.Request(
        SEARCH_TEXT_URL,
        data=body,
        headers={
            'X-Goog-Api-Key': api_key,
            'X-Goog-FieldMask': 'places.id',
            'Content-Type': 'application/json',
        },
        method='POST',
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode('utf-8', errors='replace')
        raise RuntimeError(f'Places searchText HTTP {exc.code}: {err_body}') from exc

    places = payload.get('places') or []
    if not places:
        raise RuntimeError(f'No place found for query: {query!r}')

    place_id = (places[0].get('id') or '').strip()
    if place_id.startswith('places/'):
        place_id = place_id[len('places/'):]
    if not place_id:
        raise RuntimeError('Place ID missing in searchText response.')
    return place_id


def get_place_id(api_key: str) -> str:
    """Return configured Place ID or resolve Black Diamond via Text Search."""
    configured = place_id_from_env()
    if configured:
        return configured
    return resolve_place_id(api_key)


def anonymize_author(display_name: str) -> str:
    """Turn 'David Schenk' into 'David S.' like Google Maps."""
    name = (display_name or '').strip()
    if not name:
        return 'Guest'
    parts = name.split()
    if len(parts) == 1:
        return parts[0][:40]
    initial = parts[-1][0].upper() if parts[-1] else ''
    return f'{parts[0]} {initial}.'[:40]


def slug_review_id(place_id: str, resource_name: str, author: str) -> str:
    raw = f'{place_id}:{resource_name}:{author}'
    slug = re.sub(r'[^a-z0-9]+', '-', raw.lower()).strip('-')
    return slug[:120] or 'google-review'


def fetch_place_reviews(place_id: str, api_key: str) -> list[dict[str, Any]]:
    """Return up to 5 reviews from Places API (New)."""
    url = f'{PLACES_BASE}/{place_id}'
    request = urllib.request.Request(
        url,
        headers={
            'X-Goog-Api-Key': api_key,
            'X-Goog-FieldMask': 'reviews',
        },
        method='GET',
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode('utf-8', errors='replace')
        raise RuntimeError(f'Places API HTTP {exc.code}: {body}') from exc

    reviews = payload.get('reviews') or []
    parsed: list[dict[str, Any]] = []
    for item in reviews:
        text_block = item.get('text') or {}
        text = (text_block.get('text') or '').strip()
        if not text:
            continue
        author_attr = item.get('authorAttribution') or {}
        display_name = (author_attr.get('displayName') or '').strip()
        resource_name = (item.get('name') or '').strip()
        parsed.append(
            {
                'text': text,
                'rating': int(item.get('rating') or 0) or None,
                'author_label': anonymize_author(display_name),
                'google_review_id': slug_review_id(place_id, resource_name, display_name),
            }
        )
    return parsed

"""Price catalog helpers — durations aligned with tantra-prague ceník (45 / 60 / 90 min)."""

from __future__ import annotations

from dataclasses import dataclass

from apps.services.models import Service

# Standard session lengths (no 75 min — see tantra-prague.com/cs/cenik/)
CATALOG_DURATIONS: tuple[int, ...] = (45, 60, 90)


@dataclass(frozen=True)
class CatalogEntry:
    service: Service
    duration_min: int
    price_czk: int


def normalize_duration(raw: int) -> int:
    """Map legacy durations (e.g. 75) to the nearest catalog length."""
    if raw in CATALOG_DURATIONS:
        return raw
    if raw < 53:
        return 45
    if raw <= 75:
        return 60
    return 90


def catalog_duration_for(service: Service) -> int:
    """Public duration (45 / 60 / 90 min) for cards and detail."""
    raw = service.base_duration_min or service.duration or 60
    return normalize_duration(int(raw))


def catalog_price_for(service: Service) -> int:
    """Public price in CZK for cards and detail."""
    return int(service.base_price_czk or service.price or 0)


def build_price_catalog() -> list[CatalogEntry]:
    """All active massages for the public ceník page."""
    entries: list[CatalogEntry] = []
    for service in Service.objects.filter(is_active=True).order_by('order', 'pk'):
        entries.append(
            CatalogEntry(
                service=service,
                duration_min=catalog_duration_for(service),
                price_czk=catalog_price_for(service),
            )
        )
    return entries

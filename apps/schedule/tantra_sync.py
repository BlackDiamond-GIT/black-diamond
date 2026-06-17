"""Sync schedule from tantra-prague.com Hub API (replaces HTML scraper).

Prev: scraped https://tantra-prague.com/cs/rozvrh/ via regex.
Now:  calls /api/v1/black-diamond/schedule/ with X-Site-Key auth → proper JSON.
"""

from __future__ import annotations

import datetime

from django.db import transaction

from apps.hub_client.client import HubClient
from apps.hub_client.exceptions import HubAPIError, HubUnavailableError
from apps.schedule.models import ScheduleEntry
from apps.schedule.shifts import infer_shift_type
from apps.therapists.models import Therapist

from .addresses import WORK_ADDRESS


def _therapist_map() -> dict[str, Therapist]:
    """Map hub_slug → Therapist. Falls back to slug if hub_slug is empty."""
    result: dict[str, Therapist] = {}
    for t in Therapist.objects.filter(is_active=True):
        key = t.hub_slug or t.slug
        result[key] = t
    return result


def sync_schedule_from_hub(
    *,
    from_date: datetime.date | None = None,
    days: int = 35,
    dry_run: bool = False,
) -> dict[str, int]:
    """Fetch schedule from hub API and upsert local ScheduleEntry rows."""
    client = HubClient()
    therapist_by_slug = _therapist_map()

    try:
        raw_entries = client.fetch_schedule_json(from_date=from_date, days=days)
    except HubAPIError as exc:
        if exc.status_code == 401:
            return {
                "error": (
                    "Hub API rejected the site key (401). "
                    "Set HUB_API_KEY on the cron service to match the web service."
                ),
                "fetched": 0,
                "created": 0,
                "updated": 0,
                "skipped": 0,
            }
        return {
            "error": str(exc),
            "fetched": 0,
            "created": 0,
            "updated": 0,
            "skipped": 0,
        }
    except HubUnavailableError as exc:
        return {"error": str(exc), "fetched": 0, "created": 0, "updated": 0, "skipped": 0}

    matched = [e for e in raw_entries if e["masseuse_slug"] in therapist_by_slug]
    skipped = len(raw_entries) - len(matched)
    created = updated = 0

    if dry_run:
        return {
            "fetched": len(raw_entries),
            "matched": len(matched),
            "created": 0,
            "updated": 0,
            "skipped": skipped,
        }

    with transaction.atomic():
        for entry in matched:
            therapist = therapist_by_slug[entry["masseuse_slug"]]
            time_from = datetime.time.fromisoformat(entry["time_from"])
            time_to = datetime.time.fromisoformat(entry["time_to"])
            shift_type = entry.get("shift_type") or infer_shift_type(time_from)

            defaults = {
                "time_to": time_to,
                "branch": None,
                "shift_type": shift_type,
                "location_address": WORK_ADDRESS,
                "note_cs": entry.get("note_cs", ""),
                "note_en": entry.get("note_en", ""),
            }
            _, was_created = ScheduleEntry.objects.update_or_create(
                therapist=therapist,
                date=datetime.date.fromisoformat(entry["date"]),
                time_from=time_from,
                defaults=defaults,
            )
            if was_created:
                created += 1
            else:
                updated += 1

    return {
        "fetched": len(raw_entries),
        "matched": len(matched),
        "created": created,
        "updated": updated,
        "skipped": skipped,
    }

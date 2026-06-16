"""Імпорт розкладу з tantra-prague.com/cs/rozvrh/."""

from __future__ import annotations

import datetime
import re
import urllib.error
import urllib.request
from dataclasses import dataclass

from django.db import transaction

from apps.schedule.addresses import WORK_ADDRESS
from apps.schedule.models import ScheduleEntry
from apps.schedule.shifts import infer_shift_type
from apps.schedule.week import MAX_WEEKS, ROLLING_DAYS, business_date
from apps.therapists.models import Therapist

SOURCE_URL = 'https://tantra-prague.com/cs/rozvrh/'
USER_AGENT = 'BlackDiamondScheduleSync/1.0'


@dataclass(frozen=True)
class ParsedEntry:
    date: datetime.date
    therapist_slug: str
    time_from: datetime.time
    time_to: datetime.time
    shift: str
    branch_key: str


def _parse_time(value: str) -> datetime.time:
    hour, minute = value.strip().split(':')
    return datetime.time(int(hour), int(minute))


def parse_time_range(raw: str) -> tuple[datetime.time, datetime.time]:
    normalized = raw.replace('\u2013', '-').replace('–', '-').strip()
    start_raw, end_raw = normalized.split('-', 1)
    return _parse_time(start_raw), _parse_time(end_raw)


def branch_key_from_label(label: str) -> str:
    lowered = label.lower()
    if 'diamond' in lowered:
        return 'diamond'
    if 'velvet' in lowered:
        return 'velvet'
    return ''


def fetch_schedule_html(anchor: datetime.date) -> str:
    url = f'{SOURCE_URL}?from={anchor.isoformat()}'
    request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.read().decode('utf-8')


def parse_schedule_html(html: str) -> list[ParsedEntry]:
    entries: list[ParsedEntry] = []
    day_sections = re.split(r'<section class="schedule-week-day', html)

    for section in day_sections[1:]:
        date_match = re.search(r'id="schedule-day-(\d{4}-\d{2}-\d{2})"', section)
        if not date_match:
            continue
        entry_date = datetime.date.fromisoformat(date_match.group(1))

        for item in re.split(r'<li class="schedule-timeline__item">', section)[1:]:
            time_match = re.search(
                r'<time class="schedule-timeline__time"[^>]*>\s*([^<]+)',
                item,
            )
            slug_match = re.search(r'/maserky/([^/]+)/', item)
            shift_match = re.search(r'schedule-timeline__shift[^"]*--(\w+)"', item)
            branch_match = re.search(r'schedule-timeline__address">([^<]+)', item)
            if not time_match or not slug_match:
                continue

            time_from, time_to = parse_time_range(time_match.group(1))
            entries.append(
                ParsedEntry(
                    date=entry_date,
                    therapist_slug=slug_match.group(1),
                    time_from=time_from,
                    time_to=time_to,
                    shift=shift_match.group(1) if shift_match else 'day',
                    branch_key=branch_key_from_label(
                        branch_match.group(1) if branch_match else ''
                    ),
                )
            )

    return entries


def _therapist_map() -> dict[str, Therapist]:
    return {
        therapist.slug: therapist
        for therapist in Therapist.objects.filter(is_active=True)
    }


def sync_schedule_from_tantra(
    *,
    weeks: int = MAX_WEEKS,
    anchor: datetime.date | None = None,
    dry_run: bool = False,
) -> dict[str, int]:
    """Fetch rolling weeks from tantra-prague and upsert ScheduleEntry rows."""
    start_anchor = anchor or business_date()
    therapist_by_slug = _therapist_map()

    parsed: list[ParsedEntry] = []
    fetch_errors = 0

    for week_index in range(weeks):
        week_anchor = start_anchor + datetime.timedelta(days=ROLLING_DAYS * week_index)
        try:
            html = fetch_schedule_html(week_anchor)
        except (urllib.error.URLError, TimeoutError, OSError):
            fetch_errors += 1
            continue
        parsed.extend(parse_schedule_html(html))

    matched = [
        entry for entry in parsed
        if entry.therapist_slug in therapist_by_slug
    ]

    created = 0
    updated = 0
    skipped = 0

    if dry_run:
        return {
            'fetched': len(parsed),
            'matched': len(matched),
            'created': 0,
            'updated': 0,
            'skipped': len(parsed) - len(matched),
            'fetch_errors': fetch_errors,
        }

    with transaction.atomic():
        for entry in matched:
            therapist = therapist_by_slug[entry.therapist_slug]
            shift_type = (
                ScheduleEntry.ShiftType.NIGHT
                if entry.shift == 'night'
                else ScheduleEntry.ShiftType.DAY
            )
            if not entry.shift:
                shift_type = infer_shift_type(entry.time_from)

            defaults = {
                'time_to': entry.time_to,
                'branch': None,
                'shift_type': shift_type,
                'location_address': WORK_ADDRESS,
            }

            obj, was_created = ScheduleEntry.objects.update_or_create(
                therapist=therapist,
                date=entry.date,
                time_from=entry.time_from,
                defaults=defaults,
            )
            if was_created:
                created += 1
            else:
                updated += 1

        skipped = len(parsed) - len(matched)

    return {
        'fetched': len(parsed),
        'matched': len(matched),
        'created': created,
        'updated': updated,
        'skipped': skipped,
        'fetch_errors': fetch_errors,
    }

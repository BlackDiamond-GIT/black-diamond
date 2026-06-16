"""Seed weekly schedule patterns (black-velvet style)."""

from __future__ import annotations

import datetime

from django.db import transaction

from apps.schedule.models import ScheduleEntry
from apps.schedule.shifts import infer_shift_type
from apps.schedule.week import MAX_WEEKS, monday_of, business_date
from apps.therapists.models import Therapist

# weekday 0=Mon … 6=Sun; times as HH:MM strings
WEEKLY_SHIFTS: dict[str, list[tuple[int, str, str, str]]] = {
    'julia': [
        (1, '09:00', '20:30', 'day'),
        (2, '09:00', '20:30', 'day'),
    ],
    'diana': [
        (1, '09:00', '20:30', 'day'),
        (2, '09:00', '20:30', 'day'),
        (5, '09:00', '20:30', 'day'),
    ],
    'laura': [
        (3, '18:30', '04:00', 'night'),
        (4, '00:00', '04:00', 'night'),
    ],
    'mira': [
        (5, '09:00', '20:30', 'day'),
    ],
    'vanessa': [
        (1, '11:00', '20:30', 'day'),
        (3, '09:00', '20:30', 'day'),
    ],
    'ella': [
        (2, '09:00', '20:30', 'day'),
        (4, '09:00', '20:30', 'day'),
    ],
}


def _parse_time(value: str) -> datetime.time:
    hour, minute = value.split(':')
    return datetime.time(int(hour), int(minute))


def seed_schedule_entries(
    *,
    weeks: int = MAX_WEEKS,
    week_start: datetime.date | None = None,
) -> dict[str, int]:
    """Upsert template shifts for active therapists (repeats each ISO week)."""
    start = monday_of(week_start or business_date())
    therapists = {
        therapist.slug: therapist
        for therapist in Therapist.objects.filter(is_active=True)
    }

    created = 0
    updated = 0
    skipped = 0

    with transaction.atomic():
        for week_index in range(weeks):
            week_monday = start + datetime.timedelta(days=7 * week_index)
            for slug, shifts in WEEKLY_SHIFTS.items():
                therapist = therapists.get(slug)
                if not therapist:
                    skipped += len(shifts)
                    continue

                for weekday, time_from_raw, time_to_raw, shift in shifts:
                    entry_date = week_monday + datetime.timedelta(days=weekday)
                    time_from = _parse_time(time_from_raw)
                    time_to = _parse_time(time_to_raw)
                    shift_type = (
                        ScheduleEntry.ShiftType.NIGHT
                        if shift == 'night'
                        else ScheduleEntry.ShiftType.DAY
                    )
                    if shift != 'night' and shift != 'day':
                        shift_type = infer_shift_type(time_from)

                    _, was_created = ScheduleEntry.objects.update_or_create(
                        therapist=therapist,
                        date=entry_date,
                        time_from=time_from,
                        defaults={
                            'time_to': time_to,
                            'shift_type': shift_type,
                            'branch': None,
                        },
                    )
                    if was_created:
                        created += 1
                    else:
                        updated += 1

    return {'created': created, 'updated': updated, 'skipped': skipped}

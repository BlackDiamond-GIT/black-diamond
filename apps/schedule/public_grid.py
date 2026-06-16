"""Public schedule grid context (black-velvet layout)."""

from __future__ import annotations

import datetime
from dataclasses import dataclass

from django.utils import timezone
from django.utils.translation import get_language

from apps.therapists.models import Therapist

from .addresses import WORK_ADDRESS
from .models import ScheduleEntry
from .week import (
    business_date,
    entry_is_live_now,
    fetch_entries_for_range,
    monday_of,
    operational_date_for_entry,
    schedule_sort_key,
    week_dates,
)

DAYS_SHORT = {
    'cs': ['Po', 'Út', 'St', 'Čt', 'Pá', 'So', 'Ne'],
    'en': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    'ru': ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
}

SLOT_AVAILABLE = 'available'
SLOT_BOOKED = 'booked'


@dataclass(frozen=True)
class ScheduleSlotDisplay:
    entry: ScheduleEntry
    status: str
    is_night: bool


@dataclass(frozen=True)
class ScheduleDayDisplay:
    date: datetime.date
    weekday_short: str
    is_today: bool
    slots: tuple[ScheduleSlotDisplay, ...]


@dataclass(frozen=True)
class TherapistPanel:
    therapist: Therapist
    specialty_labels: tuple[str, ...]
    days: tuple[ScheduleDayDisplay, ...]
    tab_index: int


@dataclass(frozen=True)
class LiveShiftDisplay:
    entry: ScheduleEntry


def current_iso_week() -> tuple[datetime.date, datetime.date, list[datetime.date]]:
    today = business_date()
    week_start = monday_of(today)
    week_end = week_start + datetime.timedelta(days=6)
    return week_start, week_end, week_dates(week_start)


def weekday_short(day: datetime.date, lang: str) -> str:
    code = (lang or 'cs')[:2]
    labels = DAYS_SHORT.get(code, DAYS_SHORT['cs'])
    return labels[day.weekday()]


def slot_status(entry: ScheduleEntry) -> str:
    if entry.therapist.is_busy:
        return SLOT_BOOKED
    return SLOT_AVAILABLE


def specialty_labels(therapist: Therapist, lang: str, limit: int = 3) -> tuple[str, ...]:
    labels: list[str] = []
    for service in therapist.specialties.filter(is_active=True).order_by('order')[:limit]:
        labels.append(service.get_title(lang))
    return tuple(labels)


def fetch_live_entries(entries) -> list[LiveShiftDisplay]:
    now = timezone.localtime()
    return [
        LiveShiftDisplay(entry=entry)
        for entry in entries
        if entry_is_live_now(entry, now)
    ]


def build_therapist_panels(
    dates: list[datetime.date],
    entries,
    lang: str,
) -> list[TherapistPanel]:
    today = business_date()
    by_therapist: dict[int, dict[datetime.date, list[ScheduleEntry]]] = {}

    for entry in entries:
        op_date = operational_date_for_entry(entry.date, entry.time_from)
        if op_date not in dates:
            continue
        by_therapist.setdefault(entry.therapist_id, {day: [] for day in dates})
        by_therapist[entry.therapist_id][op_date].append(entry)

    therapists = list(
        Therapist.objects.filter(is_active=True)
        .prefetch_related('specialties')
        .order_by('sort_order', 'name')
    )

    panels: list[TherapistPanel] = []
    for idx, therapist in enumerate(therapists):
        day_map = by_therapist.get(therapist.pk, {day: [] for day in dates})
        days: list[ScheduleDayDisplay] = []
        for day in dates:
            raw_slots = sorted(day_map.get(day, []), key=schedule_sort_key)
            slots = tuple(
                ScheduleSlotDisplay(
                    entry=slot_entry,
                    status=slot_status(slot_entry),
                    is_night=slot_entry.shift_type == ScheduleEntry.ShiftType.NIGHT,
                )
                for slot_entry in raw_slots
            )
            days.append(
                ScheduleDayDisplay(
                    date=day,
                    weekday_short=weekday_short(day, lang),
                    is_today=day == today,
                    slots=slots,
                )
            )
        panels.append(
            TherapistPanel(
                therapist=therapist,
                specialty_labels=specialty_labels(therapist, lang),
                days=tuple(days),
                tab_index=idx,
            )
        )
    return panels


def build_schedule_page_context() -> dict:
    lang = (get_language() or 'cs')[:2]
    week_start, week_end, dates = current_iso_week()
    entries = list(fetch_entries_for_range(week_start, week_end))

    return {
        'week_start': week_start,
        'week_end': week_end,
        'today': business_date(),
        'work_address': WORK_ADDRESS,
        'live_entries': fetch_live_entries(entries),
        'therapist_panels': build_therapist_panels(dates, entries, lang),
    }

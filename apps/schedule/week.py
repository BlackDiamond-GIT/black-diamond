"""Week helpers for schedule grouping and navigation."""

from __future__ import annotations

import datetime
from dataclasses import dataclass
from typing import TYPE_CHECKING

from django.utils import timezone

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from .models import ScheduleEntry

ROLLING_DAYS = 7
MAX_WEEKS = 5
BUSINESS_DAY_CUTOFF_HOUR = 6


def business_date() -> datetime.date:
    """Return the operational calendar date (night shifts count until 06:00)."""
    now = timezone.localtime()
    today = now.date()
    if now.hour < BUSINESS_DAY_CUTOFF_HOUR:
        return today - datetime.timedelta(days=1)
    return today


def max_anchor(today: datetime.date) -> datetime.date:
    """Latest anchor date for public schedule (5 rolling weeks from today)."""
    return today + datetime.timedelta(days=(MAX_WEEKS - 1) * ROLLING_DAYS)


def is_overnight_continuation(time_from: datetime.time) -> bool:
    """Early-morning slots belong to the previous operational day."""
    return time_from.hour < BUSINESS_DAY_CUTOFF_HOUR


def operational_date_for_entry(entry_date: datetime.date, time_from: datetime.time) -> datetime.date:
    """Map a DB row to the operational day shown in the public schedule."""
    if is_overnight_continuation(time_from):
        return entry_date - datetime.timedelta(days=1)
    return entry_date


def schedule_sort_key(entry: ScheduleEntry) -> int:
    """Sort slots within a day: morning → evening → after-midnight."""
    minutes = entry.time_from.hour * 60 + entry.time_from.minute
    if is_overnight_continuation(entry.time_from):
        minutes += 24 * 60
    return minutes


def entry_is_live_now(entry: ScheduleEntry, now: datetime.datetime | None = None) -> bool:
    """True when the therapist is currently on this shift."""
    now = now or timezone.localtime()
    op_date = operational_date_for_entry(entry.date, entry.time_from)
    if op_date != business_date():
        return False

    current = now.time()
    start = entry.time_from
    end = entry.time_to
    if end > start:
        return start <= current <= end
    return current >= start or current <= end


@dataclass(frozen=True)
class ScheduleEntryDisplay:
    entry: ScheduleEntry
    is_live: bool = False


@dataclass(frozen=True)
class DaySchedule:
    date: datetime.date
    weekday_label: str
    is_today: bool
    entries: list[ScheduleEntryDisplay]


def monday_of(d: datetime.date) -> datetime.date:
    """Return Monday of the ISO week containing *d*."""
    return d - datetime.timedelta(days=d.weekday())


def week_range(week_start: datetime.date) -> tuple[datetime.date, datetime.date]:
    """Return (monday, sunday) for the week starting on *week_start*."""
    start = monday_of(week_start)
    return start, start + datetime.timedelta(days=6)


def rolling_dates(anchor: datetime.date) -> list[datetime.date]:
    """Return *ROLLING_DAYS* consecutive dates starting from *anchor*."""
    return [anchor + datetime.timedelta(days=i) for i in range(ROLLING_DAYS)]


def parse_anchor_param(raw: str | None) -> datetime.date:
    """Parse ?from=YYYY-MM-DD; clamp to the public schedule window (today … 5 weeks)."""
    today = business_date()
    if not raw:
        return today
    try:
        parsed = datetime.date.fromisoformat(raw)
    except ValueError:
        return today
    return min(max(parsed, today), max_anchor(today))


def parse_week_param(raw: str | None) -> datetime.date:
    """Parse ?week=YYYY-MM-DD and normalize to Monday; fallback to current ISO week."""
    today = business_date()
    if not raw:
        return monday_of(today)
    try:
        parsed = datetime.date.fromisoformat(raw)
    except ValueError:
        return monday_of(today)
    return monday_of(parsed)


def week_dates(week_start: datetime.date) -> list[datetime.date]:
    """Seven consecutive dates from Monday through Sunday."""
    start = monday_of(week_start)
    return [start + datetime.timedelta(days=i) for i in range(7)]


def fetch_entries_for_range(
    start: datetime.date,
    end: datetime.date,
) -> QuerySet[ScheduleEntry]:
    """Schedule entries for the range, including next-day overnight slots."""
    from .models import ScheduleEntry

    extended_end = end + datetime.timedelta(days=1)
    qs = ScheduleEntry.objects.filter(date__range=(start, extended_end))
    return (
        qs.select_related("therapist", "therapist__main_cloudinary_photo")
        .prefetch_related("therapist__gallery_cloudinary")
        .order_by("date", "time_from")
    )


def fetch_week_entries(week_start: datetime.date) -> QuerySet[ScheduleEntry]:
    """All schedule entries for the given ISO week (Mon–Sun). Used by admin."""
    start, end = week_range(week_start)
    return fetch_entries_for_range(start, end)


def group_entries_by_day(
    dates: list[datetime.date],
    entries: QuerySet[ScheduleEntry] | list[ScheduleEntry],
) -> list[DaySchedule]:
    """Group entries into operational day buckets for template rendering."""
    today = business_date()
    now = timezone.localtime()
    by_date: dict[datetime.date, list[ScheduleEntry]] = {d: [] for d in dates}
    for entry in entries:
        op_date = operational_date_for_entry(entry.date, entry.time_from)
        if op_date in by_date:
            by_date[op_date].append(entry)

    result: list[DaySchedule] = []
    for day in dates:
        sorted_entries = sorted(by_date[day], key=schedule_sort_key)
        displays = [
            ScheduleEntryDisplay(
                entry=entry,
                is_live=entry_is_live_now(entry, now),
            )
            for entry in sorted_entries
        ]
        result.append(
            DaySchedule(
                date=day,
                weekday_label=day.strftime("%A"),
                is_today=day == today,
                entries=displays,
            )
        )
    return result


def build_week_context(anchor: datetime.date) -> dict:
    """Shared context dict for public views and CMS plugin."""
    from .addresses import WORK_ADDRESS

    today = business_date()
    anchor = min(max(anchor, today), max_anchor(today))
    dates = rolling_dates(anchor)
    start, end = dates[0], dates[-1]
    entries = fetch_entries_for_range(start, end)
    prev_anchor = anchor - datetime.timedelta(days=ROLLING_DAYS) if anchor > today else None
    forward = anchor + datetime.timedelta(days=ROLLING_DAYS)
    next_anchor = forward if forward <= max_anchor(today) else None
    return {
        "anchor": anchor,
        "week_start": start,
        "week_end": end,
        "prev_anchor": prev_anchor,
        "next_anchor": next_anchor,
        "prev_week": prev_anchor,
        "next_week": next_anchor,
        "today": today,
        "work_address": WORK_ADDRESS,
        "week_days": group_entries_by_day(dates, entries),
    }

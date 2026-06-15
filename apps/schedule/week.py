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


@dataclass(frozen=True)
class DaySchedule:
    date: datetime.date
    weekday_label: str
    is_today: bool
    entries: list[ScheduleEntry]


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
    branch_id: int | None = None,
) -> QuerySet[ScheduleEntry]:
    """Schedule entries between *start* and *end* inclusive."""
    from .models import ScheduleEntry

    qs = ScheduleEntry.objects.filter(date__range=(start, end))
    if branch_id:
        qs = qs.filter(branch_id=branch_id)
    return (
        qs.select_related("therapist", "therapist__main_cloudinary_photo", "branch")
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
    """Group entries into day buckets for template rendering."""
    today = business_date()
    by_date: dict[datetime.date, list[ScheduleEntry]] = {d: [] for d in dates}
    for entry in entries:
        if entry.date in by_date:
            by_date[entry.date].append(entry)

    result: list[DaySchedule] = []
    for day in dates:
        result.append(
            DaySchedule(
                date=day,
                weekday_label=day.strftime("%A"),
                is_today=day == today,
                entries=by_date[day],
            )
        )
    return result


def build_week_context(anchor: datetime.date, branch_id: int | None = None) -> dict:
    """Shared context dict for public views and CMS plugin."""
    today = business_date()
    anchor = min(max(anchor, today), max_anchor(today))
    dates = rolling_dates(anchor)
    start, end = dates[0], dates[-1]
    entries = fetch_entries_for_range(start, end, branch_id=branch_id)
    prev_anchor = anchor - datetime.timedelta(days=ROLLING_DAYS) if anchor > today else None
    forward = anchor + datetime.timedelta(days=ROLLING_DAYS)
    next_anchor = forward if forward <= max_anchor(today) else None
    return {
        "anchor": anchor,
        "branch_id": branch_id,
        "week_start": start,
        "week_end": end,
        "prev_anchor": prev_anchor,
        "next_anchor": next_anchor,
        "prev_week": prev_anchor,
        "next_week": next_anchor,
        "today": today,
        "week_days": group_entries_by_day(dates, entries),
    }

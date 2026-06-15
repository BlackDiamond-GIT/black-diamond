"""Shift type inference for schedule entries."""

from __future__ import annotations

import datetime

from .models import ScheduleEntry

NIGHT_TIME_FROM = frozenset({"18:30", "20:30", "02:00", "04:00"})


def infer_shift_type(time_from: datetime.time) -> str:
    """Return night shift for evening and after-midnight start slots."""
    if time_from.strftime("%H:%M") in NIGHT_TIME_FROM:
        return ScheduleEntry.ShiftType.NIGHT
    return ScheduleEntry.ShiftType.DAY

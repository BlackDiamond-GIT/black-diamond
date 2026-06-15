"""Availability grid helpers for booking admin."""

from __future__ import annotations

import datetime
from dataclasses import dataclass

from django.db.models import QuerySet

from apps.therapists.models import Therapist
from apps.schedule.models import ScheduleEntry

from .models import Appointment


@dataclass(frozen=True)
class AvailabilitySlot:
    time_from: datetime.time
    time_to: datetime.time
    schedule_entry: ScheduleEntry | None
    appointment: Appointment | None
    is_available: bool


@dataclass(frozen=True)
class AvailabilityRow:
    therapist: Therapist
    slots: list[AvailabilitySlot]


def _therapist_queryset(branch_id: int | None) -> QuerySet[Therapist]:
    qs = Therapist.objects.filter(is_active=True).order_by("sort_order", "name")
    if branch_id:
        qs = qs.filter(branches__id=branch_id).distinct()
    return qs


def build_availability_grid(
    target_date: datetime.date,
    branch_id: int | None = None,
) -> list[AvailabilityRow]:
    """Build therapist × schedule-slot availability for admin operators."""
    therapists = list(_therapist_queryset(branch_id))
    if not therapists:
        return []

    entries_qs = ScheduleEntry.objects.filter(date=target_date).select_related("branch")
    if branch_id:
        entries_qs = entries_qs.filter(branch_id=branch_id)

    entries_by_therapist: dict[int, list[ScheduleEntry]] = {}
    for entry in entries_qs.order_by("time_from"):
        entries_by_therapist.setdefault(entry.therapist_id, []).append(entry)

    appointments_qs = (
        Appointment.objects.filter(date=target_date)
        .exclude(status=Appointment.Status.CANCELLED)
        .select_related("service")
    )
    if branch_id:
        appointments_qs = appointments_qs.filter(branch_id=branch_id)

    appointments_map: dict[tuple[int, datetime.time], Appointment] = {}
    for appt in appointments_qs:
        appointments_map[(appt.therapist_id, appt.time_start)] = appt

    rows: list[AvailabilityRow] = []
    for therapist in therapists:
        slots: list[AvailabilitySlot] = []
        for entry in entries_by_therapist.get(therapist.pk, []):
            appt = appointments_map.get((therapist.pk, entry.time_from))
            slots.append(
                AvailabilitySlot(
                    time_from=entry.time_from,
                    time_to=entry.time_to,
                    schedule_entry=entry,
                    appointment=appt,
                    is_available=appt is None,
                )
            )
        rows.append(AvailabilityRow(therapist=therapist, slots=slots))

    return rows

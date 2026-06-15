"""Manager-only appointment statistics."""

from __future__ import annotations

import datetime

from django.db.models import Count
from django.utils import timezone

from .models import Appointment


def build_appointment_stats(days: int = 30) -> dict[str, object]:
    """Aggregate confidential booking metrics for managers."""
    days = max(1, min(days, 365))
    since = timezone.localdate() - datetime.timedelta(days=days - 1)
    qs = Appointment.objects.filter(date__gte=since).select_related("therapist", "service", "branch")

    status_counts = {
        row["status"]: row["total"]
        for row in qs.values("status").annotate(total=Count("id"))
    }
    top_therapists = list(
        qs.values("therapist__name")
        .annotate(total=Count("id"))
        .order_by("-total", "therapist__name")[:8]
    )
    recent = list(qs.order_by("-date", "-time_start", "-created_at")[:25])

    return {
        "days": days,
        "since": since,
        "total": qs.count(),
        "pending": status_counts.get(Appointment.Status.PENDING, 0),
        "confirmed": status_counts.get(Appointment.Status.CONFIRMED, 0),
        "done": status_counts.get(Appointment.Status.DONE, 0),
        "cancelled": status_counts.get(Appointment.Status.CANCELLED, 0),
        "top_therapists": top_therapists,
        "recent": recent,
    }

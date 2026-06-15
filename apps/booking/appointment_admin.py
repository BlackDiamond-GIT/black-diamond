"""Appointment admin with availability grid and manager stats."""

from __future__ import annotations

import datetime

from django.contrib import admin
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _

from apps.core.unfold_admin import BDModelAdmin

from .appointment_stats import build_appointment_stats
from .availability import build_availability_grid
from .models import Appointment


def _can_view_confidential(request: HttpRequest) -> bool:
    return request.user.has_perm("booking.view_confidential_booking") or request.user.is_superuser


@admin.register(Appointment)
class AppointmentAdmin(BDModelAdmin):
    list_display = (
        "date",
        "time_start",
        "therapist",
        "service",
        "branch",
        "status",
        "duration_min",
    )
    list_filter = ("status", "date", "branch", "therapist")
    search_fields = ("therapist__name", "client_name", "client_phone", "notes")
    autocomplete_fields = ("therapist", "branch", "service")
    date_hierarchy = "date"
    change_list_template = "admin/booking/appointment/change_list.html"

    def get_list_display(self, request: HttpRequest):
        fields = list(super().get_list_display(request))
        if _can_view_confidential(request):
            fields.extend(["client_name", "client_phone"])
        return fields

    def get_fieldsets(self, request: HttpRequest):
        base = (
            (
                None,
                {
                    "fields": (
                        "therapist",
                        "branch",
                        "service",
                        "date",
                        "time_start",
                        "duration_min",
                        "status",
                    )
                },
            ),
        )
        if _can_view_confidential(request):
            return base + ((_("Client (confidential)"), {"fields": ("client_name", "client_phone", "notes")}),)
        return base

    def get_readonly_fields(self, request: HttpRequest, obj: Appointment | None = None):
        readonly = list(super().get_readonly_fields(request, obj))
        if not _can_view_confidential(request):
            readonly.extend(["client_name", "client_phone", "notes"])
        return readonly

    def save_model(self, request: HttpRequest, obj: Appointment, form, change: bool) -> None:
        if not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                "availability/",
                self.admin_site.admin_view(self.availability_view),
                name="booking_appointment_availability",
            ),
            path(
                "stats/",
                self.admin_site.admin_view(self.stats_view),
                name="booking_appointment_stats",
            ),
        ]
        return custom + urls

    def changelist_view(self, request: HttpRequest, extra_context=None):
        extra_context = extra_context or {}
        extra_context["availability_url"] = reverse("admin:booking_appointment_availability")
        extra_context["stats_url"] = reverse("admin:booking_appointment_stats")
        extra_context["can_view_confidential"] = _can_view_confidential(request)
        return super().changelist_view(request, extra_context=extra_context)

    def availability_view(self, request: HttpRequest) -> HttpResponse:
        from apps.branches.models import Branch
        from apps.services.models import Service

        date_raw = request.GET.get("date")
        branch_raw = request.GET.get("branch", "").strip()
        branch_id: int | None = int(branch_raw) if branch_raw.isdigit() else None

        if date_raw:
            try:
                target_date = datetime.date.fromisoformat(date_raw)
            except ValueError:
                target_date = datetime.date.today()
        else:
            target_date = datetime.date.today()

        rows = build_availability_grid(target_date, branch_id=branch_id)
        context = {
            **self.admin_site.each_context(request),
            "title": _("Availability grid"),
            "opts": self.model._meta,
            "target_date": target_date,
            "branch_id": branch_id,
            "branches": Branch.objects.filter(is_active=True).order_by("order", "name"),
            "rows": rows,
            "services": Service.objects.filter(is_active=True, is_extra=False).order_by("order"),
            "add_url": reverse("admin:booking_appointment_add"),
            "can_view_confidential": _can_view_confidential(request),
        }

        if request.headers.get("HX-Request"):
            return render(request, "admin/booking/appointment/availability_grid.html", context)
        return render(request, "admin/booking/appointment/availability.html", context)

    def stats_view(self, request: HttpRequest) -> HttpResponse:
        if not _can_view_confidential(request):
            return HttpResponseForbidden(_("You do not have permission to view booking statistics."))

        days_raw = request.GET.get("days", "30")
        days = int(days_raw) if str(days_raw).isdigit() else 30
        stats = build_appointment_stats(days=days)
        context = {
            **self.admin_site.each_context(request),
            "title": _("Booking statistics"),
            "opts": self.model._meta,
            "stats": stats,
            "days": days,
        }
        return render(request, "admin/booking/appointment/stats.html", context)

    def get_changeform_initial_data(self, request: HttpRequest) -> dict:
        initial = super().get_changeform_initial_data(request)
        therapist_id = request.GET.get("therapist")
        branch_id = request.GET.get("branch")
        date_raw = request.GET.get("date")
        time_start = request.GET.get("time_start")
        if therapist_id:
            initial["therapist"] = therapist_id
        if branch_id:
            initial["branch"] = branch_id
        if date_raw:
            try:
                initial["date"] = datetime.date.fromisoformat(date_raw)
            except ValueError:
                pass
        if time_start:
            initial["time_start"] = time_start
        return initial

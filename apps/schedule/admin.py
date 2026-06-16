"""Admin for schedule app."""

from __future__ import annotations

import datetime
from collections import defaultdict
from urllib.parse import urlencode

from django.contrib import admin, messages
from django.contrib.admin import SimpleListFilter
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _

from apps.core.unfold_admin import BDModelAdmin
from apps.therapists.models import Therapist

from .addresses import WORK_ADDRESS
from .forms import ScheduleEntryAdminForm, ScheduleWeekBulkForm
from .models import ScheduleEntry
from .week import fetch_week_entries, monday_of, parse_week_param, week_dates, week_range


class CurrentWeekFilter(SimpleListFilter):
    title = _("Week")
    parameter_name = "week"

    def lookups(self, request, model_admin):
        return (
            ("current", _("Current week")),
        )

    def queryset(self, request, queryset):
        if self.value() == "current":
            start, end = week_range(monday_of(datetime.date.today()))
            return queryset.filter(date__range=(start, end))
        return queryset


@admin.register(ScheduleEntry)
class ScheduleEntryAdmin(BDModelAdmin):
    form = ScheduleEntryAdminForm
    list_display = ("therapist", "date", "time_from", "time_to", "shift_type")
    list_filter = (CurrentWeekFilter, "date", "therapist", "shift_type")
    search_fields = ("therapist__name",)
    date_hierarchy = "date"
    autocomplete_fields = ("therapist",)
    change_list_template = "admin/schedule/scheduleentry/change_list.html"
    fieldsets = (
        (None, {"fields": ("therapist", "date", "time_from", "time_to")}),
        (_("Shift"), {"fields": ("shift_type",)}),
        (_("Notes"), {"fields": ("note_cs", "note_en")}),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                "add-week/",
                self.admin_site.admin_view(self.add_week_view),
                name="schedule_scheduleentry_add_week",
            ),
            path(
                "week-grid/",
                self.admin_site.admin_view(self.week_grid_view),
                name="schedule_scheduleentry_week_grid",
            ),
        ]
        return custom + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["add_week_url"] = reverse("admin:schedule_scheduleentry_add_week")
        extra_context["week_grid_url"] = reverse("admin:schedule_scheduleentry_week_grid")
        return super().changelist_view(request, extra_context=extra_context)

    def add_week_view(self, request: HttpRequest) -> HttpResponse:
        if request.method == "POST":
            form = ScheduleWeekBulkForm(request.POST)
            if form.is_valid():
                created, skipped = form.save()
                if created:
                    messages.success(
                        request,
                        _("Created %(count)d schedule entries.") % {"count": created},
                    )
                if skipped:
                    messages.warning(
                        request,
                        _("Skipped %(count)d duplicate entries.") % {"count": skipped},
                    )
                if not created and not skipped:
                    messages.info(request, _("No entries were created."))
                return redirect("admin:schedule_scheduleentry_changelist")
        else:
            form = ScheduleWeekBulkForm()

        context = {
            **self.admin_site.each_context(request),
            "form": form,
            "title": _("Add schedule for week"),
            "opts": self.model._meta,
            "work_address": WORK_ADDRESS,
        }
        return render(request, "admin/schedule/scheduleentry/add_week.html", context)

    def week_grid_view(self, request: HttpRequest) -> HttpResponse:
        week_start = parse_week_param(request.GET.get("week"))
        week_end = week_start + datetime.timedelta(days=6)
        days = week_dates(week_start)
        entries = fetch_week_entries(week_start)

        grid: dict[int, dict[datetime.date, list[ScheduleEntry]]] = defaultdict(
            lambda: {d: [] for d in days}
        )
        for entry in entries:
            if entry.date in grid[entry.therapist_id]:
                grid[entry.therapist_id][entry.date].append(entry)

        therapists = Therapist.objects.filter(is_active=True).order_by("sort_order", "name")
        rows = []
        add_url = reverse("admin:schedule_scheduleentry_add")
        change_url_name = "admin:schedule_scheduleentry_change"

        for therapist in therapists:
            cells = []
            for day in days:
                day_entries = grid.get(therapist.pk, {}).get(day, [])
                slot_links = []
                for entry in day_entries:
                    shift_label = entry.get_shift_type_display()
                    slot_links.append(
                        {
                            "label": (
                                f"{entry.time_from.strftime('%H:%M')}–"
                                f"{entry.time_to.strftime('%H:%M')} "
                                f"({shift_label})"
                            ),
                            "change_url": reverse(change_url_name, args=[entry.pk]),
                        }
                    )
                add_params = urlencode(
                    {
                        "therapist": therapist.pk,
                        "date": day.isoformat(),
                        "time_from": "09:00",
                    }
                )
                cells.append(
                    {
                        "date": day,
                        "slots": slot_links,
                        "add_url": f"{add_url}?{add_params}",
                    }
                )
            rows.append({"therapist": therapist, "cells": cells})

        context = {
            **self.admin_site.each_context(request),
            "title": _("Week schedule grid"),
            "opts": self.model._meta,
            "week_start": week_start,
            "week_end": week_end,
            "prev_week": week_start - datetime.timedelta(days=7),
            "next_week": week_start + datetime.timedelta(days=7),
            "days": days,
            "rows": rows,
            "changelist_url": reverse("admin:schedule_scheduleentry_changelist"),
            "add_week_url": reverse("admin:schedule_scheduleentry_add_week"),
            "work_address": WORK_ADDRESS,
        }
        return render(request, "admin/schedule/scheduleentry/week_grid.html", context)

    def get_changeform_initial_data(self, request: HttpRequest) -> dict:
        initial = super().get_changeform_initial_data(request)
        therapist_id = request.GET.get("therapist")
        date_raw = request.GET.get("date")
        time_from = request.GET.get("time_from")
        if therapist_id:
            initial["therapist"] = therapist_id
        if date_raw:
            try:
                initial["date"] = datetime.date.fromisoformat(date_raw)
            except ValueError:
                pass
        if time_from:
            initial["time_from"] = time_from
        return initial

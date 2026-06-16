"""Admin forms for schedule app."""

from __future__ import annotations

import datetime

from django import forms
from django.db import IntegrityError, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.therapists.models import Therapist

from .models import ScheduleEntry
from .addresses import WORK_ADDRESS
from .shifts import infer_shift_type
from .week import monday_of, week_dates

TIME_CHOICES = [
    ("09:00", "09:00"),
    ("11:00", "11:00"),
    ("18:30", "18:30"),
    ("20:30", "20:30"),
    ("02:00", "02:00"),
    ("04:00", "04:00"),
    ("06:00", "06:00"),
]

WEEKDAY_CHOICES = [
    ("0", _("Monday")),
    ("1", _("Tuesday")),
    ("2", _("Wednesday")),
    ("3", _("Thursday")),
    ("4", _("Friday")),
    ("5", _("Saturday")),
    ("6", _("Sunday")),
]


def _parse_hh_mm(val: str) -> datetime.time:
    h, m = val.split(":")
    return datetime.time(int(h), int(m))


class ScheduleEntryAdminForm(forms.ModelForm):
    time_from = forms.ChoiceField(choices=TIME_CHOICES)
    time_to = forms.ChoiceField(choices=TIME_CHOICES)

    def clean_time_from(self) -> datetime.time:
        return _parse_hh_mm(self.cleaned_data["time_from"])

    def clean_time_to(self) -> datetime.time:
        return _parse_hh_mm(self.cleaned_data["time_to"])

    def clean(self) -> dict:
        cleaned = super().clean()
        time_from = cleaned.get("time_from")
        if time_from:
            cleaned["shift_type"] = infer_shift_type(time_from)
        return cleaned

    class Meta:
        model = ScheduleEntry
        fields = (
            'therapist', 'date', 'time_from', 'time_to',
            'shift_type', 'note_cs', 'note_en',
        )


class ScheduleWeekBulkForm(forms.Form):
    therapist = forms.ModelChoiceField(
        queryset=Therapist.objects.filter(is_active=True).order_by("sort_order", "name"),
        label=_("Therapist"),
    )
    week_start = forms.DateField(
        label=_("Week start (Monday)"),
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    weekdays = forms.MultipleChoiceField(
        choices=WEEKDAY_CHOICES,
        initial=[str(i) for i in range(7)],
        widget=forms.CheckboxSelectMultiple,
        label=_("Days of week"),
    )
    time_from = forms.ChoiceField(choices=TIME_CHOICES, label=_("From"))
    time_to = forms.ChoiceField(choices=TIME_CHOICES, label=_("To"))
    shift_type = forms.ChoiceField(
        choices=ScheduleEntry.ShiftType.choices,
        initial=ScheduleEntry.ShiftType.DAY,
        label=_("Shift"),
    )
    note_cs = forms.CharField(required=False, max_length=100, label=_("Note (CS)"))
    note_en = forms.CharField(required=False, max_length=100, label=_("Note (EN)"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.is_bound:
            self.fields["week_start"].initial = monday_of(timezone.localdate())

    def clean_week_start(self) -> datetime.date:
        return monday_of(self.cleaned_data["week_start"])

    def clean_time_from(self) -> datetime.time:
        return _parse_hh_mm(self.cleaned_data["time_from"])

    def clean_time_to(self) -> datetime.time:
        return _parse_hh_mm(self.cleaned_data["time_to"])

    def save(self) -> tuple[int, int]:
        """Create entries for selected weekdays; skip duplicates."""
        therapist = self.cleaned_data["therapist"]
        week_start = self.cleaned_data["week_start"]
        selected_offsets = {int(offset) for offset in self.cleaned_data["weekdays"]}
        time_from = self.cleaned_data["time_from"]
        time_to = self.cleaned_data["time_to"]
        shift_type = self.cleaned_data.get("shift_type") or infer_shift_type(time_from)
        note_cs = self.cleaned_data.get("note_cs", "")
        note_en = self.cleaned_data.get("note_en", "")

        created = 0
        skipped = 0

        with transaction.atomic():
            for offset in sorted(selected_offsets):
                entry_date = week_start + datetime.timedelta(days=offset)
                if entry_date not in week_dates(week_start):
                    continue
                exists = ScheduleEntry.objects.filter(
                    therapist=therapist,
                    date=entry_date,
                    time_from=time_from,
                ).exists()
                if exists:
                    skipped += 1
                    continue
                try:
                    ScheduleEntry.objects.create(
                        therapist=therapist,
                        date=entry_date,
                        time_from=time_from,
                        time_to=time_to,
                        location_address=WORK_ADDRESS,
                        shift_type=shift_type,
                        note_cs=note_cs,
                        note_en=note_en,
                    )
                    created += 1
                except IntegrityError:
                    skipped += 1

        return created, skipped

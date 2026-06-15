import datetime

from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.utils.translation import get_language
from django.views.generic import TemplateView

from apps.core.mixins import ExtraCssMixin
from apps.therapists.models import Therapist

from .models import TimeSlot
from .schedule_data import (
    DAYS_SHORT,
    OPENING_HOURS_LABEL,
    TIMES,
    build_db_grid,
    build_demo_grid,
    build_schedule_rows,
    today_weekday_index,
)


class SchedulePageView(ExtraCssMixin, TemplateView):
    template_name = 'schedule/index.html'
    extra_css = [
        'css/components/schedule.css',
        'css/components/glass.css',
        'css/components/buttons.css',
    ]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        lang = (get_language() or 'cs')[:2]
        therapists = Therapist.objects.filter(is_active=True).prefetch_related('specialties')
        today_idx = today_weekday_index()
        today = datetime.date.today()

        db_slots = TimeSlot.objects.filter(
            date__gte=today,
        ).select_related('therapist', 'service').order_by('date', 'time_start')[:200]

        if db_slots.exists():
            grid = build_db_grid(db_slots, lang)
        else:
            grid = build_demo_grid(therapists, lang)

        ctx.update({
            'therapists': therapists,
            'times': TIMES,
            'days_short': DAYS_SHORT.get(lang, DAYS_SHORT['cs']),
            'today_idx': today_idx,
            'rows': build_schedule_rows(grid, today_idx),
            'opening_hours': OPENING_HOURS_LABEL.get(lang, OPENING_HOURS_LABEL['cs']),
        })
        return ctx


def slots_fragment(request):
    """HTMX-ендпоінт: повертає HTML-фрагмент з слотами розкладу."""
    try:
        date_str = request.GET.get('date', '')
        selected_date = datetime.date.fromisoformat(date_str) if date_str else datetime.date.today()
    except ValueError:
        return HttpResponseBadRequest('Invalid date')

    therapist_id = request.GET.get('therapist', '')
    slots_qs = TimeSlot.objects.filter(date=selected_date).select_related('therapist', 'service')

    if therapist_id:
        slots_qs = slots_qs.filter(therapist_id=therapist_id)

    therapists = Therapist.objects.filter(is_active=True)

    return render(request, 'schedule/_slots.html', {
        'slots': slots_qs,
        'therapists': therapists,
        'selected_date': selected_date,
    })

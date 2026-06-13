import datetime
from django.views.generic import TemplateView
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from apps.core.mixins import ExtraCssMixin
from apps.therapists.models import Therapist
from .models import TimeSlot


class SchedulePageView(ExtraCssMixin, TemplateView):
    template_name = 'schedule/index.html'
    extra_css = [
        'css/components/schedule.css',
        'css/components/glass.css',
        'css/components/buttons.css',
    ]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = datetime.date.today()
        ctx['today'] = today
        ctx['days'] = [today + datetime.timedelta(days=i) for i in range(7)]
        ctx['therapists'] = Therapist.objects.filter(is_active=True)
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

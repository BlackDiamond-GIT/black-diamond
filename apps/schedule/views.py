import datetime

from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic import RedirectView

from .models import TimeSlot


class SchedulePageView(RedirectView):
    permanent = False
    pattern_name = 'pages:home'


def slots_fragment(request):
    """HTMX-ендпоінт: повертає HTML-фрагмент зі слотами розкладу."""
    try:
        date_str = request.GET.get('date', '')
        selected_date = datetime.date.fromisoformat(date_str) if date_str else datetime.date.today()
    except ValueError:
        return HttpResponseBadRequest('Invalid date')

    therapist_id = request.GET.get('therapist', '')
    slots_qs = TimeSlot.objects.filter(date=selected_date).select_related('therapist', 'service')

    if therapist_id:
        slots_qs = slots_qs.filter(therapist_id=therapist_id)

    from apps.therapists.models import Therapist

    therapists = Therapist.objects.filter(is_active=True)

    return render(request, 'schedule/_slots.html', {
        'slots': slots_qs,
        'therapists': therapists,
        'selected_date': selected_date,
    })

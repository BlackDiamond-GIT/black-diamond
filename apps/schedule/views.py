import datetime

from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.utils.translation import get_language
from django.views.generic import TemplateView

from apps.branches.models import Branch
from apps.core.mixins import ExtraCssMixin, HtmxMixin
from apps.core.opening_hours import get_opening_hours_display

from .models import TimeSlot
from .week import build_week_context, parse_anchor_param


class SchedulePageView(HtmxMixin, ExtraCssMixin, TemplateView):
    template_name = 'schedule/index.html'
    htmx_template = 'schedule/_week.html'
    extra_css = [
        'css/components/schedule-week.css',
        'css/components/buttons.css',
        'css/components/glass.css',
    ]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        lang = (get_language() or 'cs')[:2]
        branch_raw = self.request.GET.get('branch', '')
        branch_id = int(branch_raw) if branch_raw.isdigit() else None
        anchor = parse_anchor_param(self.request.GET.get('from'))

        ctx.update(build_week_context(anchor, branch_id=branch_id))
        ctx.update({
            'branches': Branch.objects.filter(is_active=True).order_by('order', 'name'),
            'opening_hours_text': get_opening_hours_display(lang),
            'schedule_path': self.request.path,
        })
        return ctx


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

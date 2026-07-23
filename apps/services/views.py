from django.views.generic import ListView, DetailView
from django.shortcuts import redirect

from apps.core.mixins import ExtraCssMixin
from .models import Service


LEGACY_SERVICE_REDIRECTS = {
    'aromaterapie': 'relaxacni-masaz',
    'cbd-relaxacni-masaz': 'relaxacni-masaz',
    'klasicka-masaz': 'relaxacni-masaz',
    'lymfaticka-masaz': 'relaxacni-masaz',
}


class ServiceListView(ExtraCssMixin, ListView):
    model = Service
    template_name = 'services/list.html'
    context_object_name = 'services'
    queryset = Service.objects.filter(is_active=True)
    extra_css = [
        'css/components/cards.css',
        'css/components/glass.css',
        'css/components/buttons.css',
        'css/components/price-multi.css',
    ]


class ServiceDetailView(ExtraCssMixin, DetailView):
    model = Service
    queryset = Service.objects.filter(is_active=True)
    template_name = 'services/detail.html'
    context_object_name = 'service'
    extra_css = [
        'css/components/glass.css',
        'css/components/buttons.css',
        'css/components/cards.css',
        'css/components/faq.css',
        'css/components/service-detail.css',
        'css/components/price-multi.css',
    ]

    def dispatch(self, request, *args, **kwargs):
        target_slug = LEGACY_SERVICE_REDIRECTS.get(kwargs.get('slug'))
        if target_slug:
            return redirect(
                'services:detail',
                slug=target_slug,
                permanent=True,
            )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['other_services'] = Service.objects.filter(
            is_active=True
        ).exclude(pk=self.object.pk)[:3]
        return ctx

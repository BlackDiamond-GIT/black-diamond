from django.views.generic import ListView, DetailView
from apps.core.mixins import ExtraCssMixin
from .models import Service


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

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['other_services'] = Service.objects.filter(
            is_active=True
        ).exclude(pk=self.object.pk)[:3]
        return ctx

from django.db.models import Case, IntegerField, When
from django.utils.translation import get_language
from django.views.generic import TemplateView

from apps.core.mixins import ExtraCssMixin
from apps.services.models import Service
from apps.therapists.models import Therapist

from .home_copy import FEATURED_SERVICE_SLUGS, get_home_copy


class HomeView(ExtraCssMixin, TemplateView):
    template_name = 'pages/home.html'
    extra_css = [
        'css/components/glass.css',
        'css/components/buttons.css',
        'css/components/mob-bar.css',
        'css/pages/home-v4.css',
    ]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        lang = get_language() or 'cs'
        home = get_home_copy(lang)

        order_cases = [
            When(slug=slug, then=pos)
            for pos, slug in enumerate(FEATURED_SERVICE_SLUGS)
        ]
        featured_services = (
            Service.objects.filter(slug__in=FEATURED_SERVICE_SLUGS, is_active=True)
            .annotate(
                _order=Case(
                    *order_cases,
                    default=99,
                    output_field=IntegerField(),
                )
            )
            .order_by('_order')
        )

        ctx['home'] = home
        ctx['featured_services'] = featured_services
        ctx['featured_therapists'] = list(
            Therapist.objects.filter(is_active=True).prefetch_related('specialties')[:6]
        )
        ctx['process_steps'] = [
            {'title': title, 'text': text}
            for title, text in home['steps']
        ]
        ctx['faqs'] = [
            {'q': question, 'a': answer}
            for question, answer in home['faqs']
        ]
        return ctx


class AboutView(ExtraCssMixin, TemplateView):
    template_name = 'pages/about.html'
    extra_css = [
        'css/components/glass.css',
        'css/components/buttons.css',
    ]


class SalonRulesView(ExtraCssMixin, TemplateView):
    template_name = 'pages/salon_rules.html'
    extra_css = ['css/components/glass.css']


class PrivacyView(ExtraCssMixin, TemplateView):
    template_name = 'pages/privacy.html'
    extra_css = ['css/components/glass.css']

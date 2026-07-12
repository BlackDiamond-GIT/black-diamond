import json
import re
from html import unescape
from typing import Optional

from django.db.models import Case, IntegerField, When
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.utils.translation import get_language
from django.views.generic import TemplateView

from apps.core.google_reviews import get_home_reviews, get_reviews_meta
from apps.core.mixins import ExtraCssMixin
from apps.faq.models import FAQ
from apps.services.models import Service
from apps.services.pricing_catalog import build_price_catalog

from .home_copy import FEATURED_SERVICE_SLUGS, get_home_copy


def _lang_code() -> str:
    return (get_language() or 'cs')[:2]


def _faq_items(limit: Optional[int] = None):
    lang = _lang_code()
    qs = FAQ.objects.filter(is_active=True).order_by('order', 'pk')
    if limit:
        qs = qs[:limit]
    items = []
    for faq in qs:
        question = getattr(faq, f'question_{lang}', '') or faq.question_cs
        answer = getattr(faq, f'answer_{lang}', '') or faq.answer_cs
        items.append({'q': question, 'a': answer})
    return items


def _faq_schema_json(faq_items: list[dict]) -> str:
    entities = []
    for item in faq_items:
        plain = strip_tags(item['a'])
        plain = unescape(re.sub(r'\s+', ' ', plain)).strip()
        entities.append({
            '@type': 'Question',
            'name': item['q'],
            'acceptedAnswer': {
                '@type': 'Answer',
                'text': plain,
            },
        })
    payload = {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': entities,
    }
    return mark_safe(json.dumps(payload, ensure_ascii=False))


class HomeView(ExtraCssMixin, TemplateView):
    template_name = 'pages/home.html'
    extra_css = [
        'css/components/glass.css',
        'css/components/buttons.css',
        'css/components/mob-bar.css',
        'css/components/price-multi.css',
        'css/components/reviews.css',
        'css/components/faq.css',
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

        faqs = _faq_items(limit=5)
        if not faqs:
            faqs = [{'q': q, 'a': a} for q, a in home['faqs'][:5]]

        reviews_meta = get_reviews_meta()
        rating = reviews_meta.get('rating')
        if rating is not None:
            reviews_meta = {
                **reviews_meta,
                'rating_stars': max(0, min(5, round(float(rating)))),
            }

        ctx['home'] = home
        ctx['featured_services'] = featured_services
        ctx['process_steps'] = [
            {'title': title, 'text': text}
            for title, text in home['steps']
        ]
        ctx['faqs'] = faqs
        ctx['guest_reviews'] = get_home_reviews(limit=6)
        ctx['reviews_meta'] = reviews_meta
        return ctx


class FaqView(ExtraCssMixin, TemplateView):
    template_name = 'pages/faq.html'
    extra_css = [
        'css/components/glass.css',
        'css/components/buttons.css',
        'css/components/faq.css',
        'css/pages/faq-page.css',
        'css/pages/contact.css',
    ]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        faq_items = _faq_items()
        ctx['faq_items'] = faq_items
        ctx['faq_schema_json'] = _faq_schema_json(faq_items) if faq_items else ''
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


class PricesView(ExtraCssMixin, TemplateView):
    template_name = 'pages/prices.html'
    extra_css = [
        'css/components/glass.css',
        'css/components/buttons.css',
        'css/components/price-multi.css',
        'css/pages/prices.css',
    ]

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['catalog'] = build_price_catalog()
        return ctx

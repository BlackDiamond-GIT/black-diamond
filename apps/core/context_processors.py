from django.conf import settings
from django.db import DatabaseError
from decimal import Decimal
from django.utils.translation import get_language

from .models import SiteSettings
from .opening_hours import DEFAULT_HOURS, get_opening_hours_display
from .pricing import CurrencySettings


def _page_lang(request) -> str:
    code = get_language() or getattr(request, 'LANGUAGE_CODE', None) or 'cs'
    return code.split('-')[0].lower()


def _fallback_address():
    return {
        'SITE_STREET_ADDRESS': 'Soukenická',
        'SITE_POSTAL_CODE': '110 00',
        'SITE_ADDRESS_LOCALITY': 'Praha 1',
        'SITE_ADDRESS_COUNTRY': 'CZ',
        'SITE_ADDRESS': getattr(settings, 'SITE_ADDRESS', 'Soukenická, 110 00 Praha 1'),
        'SITE_MAPS_URL': 'https://maps.google.com/?q=Soukenick%C3%A1,+110+00+Praha+1',
    }


def site_settings(request):
    lang = _page_lang(request)
    base = {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_URL': settings.SITE_URL,
        'SITE_PHONE': settings.SITE_PHONE,
        'SITE_EMAIL': settings.SITE_EMAIL,
        'PAGE_LANG': lang,
        'SITE_OPENING_HOURS': DEFAULT_HOURS.get(lang, DEFAULT_HOURS['cs']),
        'SITE_INSTAGRAM_URL': 'https://instagram.com/blackdiamondspa',
        'SITE_TELEGRAM_URL': '',
        'currency_settings': CurrencySettings(),
    }

    try:
        site = SiteSettings.load()
        base.update({
            'SITE_STREET_ADDRESS': site.address.split(',')[0].strip() if site.address else 'Soukenická',
            'SITE_POSTAL_CODE': '110 00',
            'SITE_ADDRESS_LOCALITY': 'Praha 1',
            'SITE_ADDRESS_COUNTRY': 'CZ',
            'SITE_ADDRESS': site.address or site.full_address,
            'SITE_MAPS_URL': site.map_url or f'https://maps.google.com/?q={site.maps_query}',
            'SITE_OPENING_HOURS': site.get_hours_for_language(lang),
            'SITE_INSTAGRAM_URL': (site.instagram_url or '').strip() or 'https://instagram.com/blackdiamondspa',
            'SITE_TELEGRAM_URL': (site.telegram_url or '').strip(),
            'currency_settings': CurrencySettings(
                eur_rate=Decimal(str(site.eur_rate)),
                usd_rate=Decimal(str(site.usd_rate)),
                show_eur=site.show_eur,
                show_usd=site.show_usd,
            ),
        })
    except DatabaseError:
        base.update(_fallback_address())
        base['SITE_OPENING_HOURS'] = get_opening_hours_display(lang)

    return base

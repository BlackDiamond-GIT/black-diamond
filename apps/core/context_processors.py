from django.conf import settings
from django.db import DatabaseError
from decimal import Decimal
from django.utils.translation import get_language

from .models import SiteSettings
from .opening_hours import DEFAULT_HOURS, get_opening_hours_display
from .phone_rotation import format_tel_href
from .pricing import CurrencySettings


def _page_lang(request) -> str:
    code = get_language() or getattr(request, 'LANGUAGE_CODE', None) or 'cs'
    return code.split('-')[0].lower()


def _fallback_address():
    return {
        'SITE_STREET_ADDRESS': 'Opletalova 1566/30',
        'SITE_POSTAL_CODE': '110 00',
        'SITE_ADDRESS_LOCALITY': 'Praha',
        'SITE_ADDRESS_COUNTRY': 'CZ',
        'SITE_ADDRESS': getattr(settings, 'SITE_ADDRESS', 'Opletalova 1566/30, 110 00 Praha'),
        'SITE_MAPS_URL': getattr(
            settings,
            'SITE_MAPS_URL',
            'https://maps.google.com/?q=Opletalova+1566%2F30%2C+110+00+Praha',
        ),
        'SITE_MAPS_EMBED_URL': getattr(settings, 'SITE_MAPS_EMBED_URL', ''),
    }


def site_settings(request):
    lang = _page_lang(request)
    base = {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_URL': settings.SITE_URL,
        'SITE_PHONE': settings.SITE_PHONE,
        'SITE_PHONE_TEL': format_tel_href(settings.SITE_PHONE),
        'SITE_EMAIL': settings.SITE_EMAIL,
        'PAGE_LANG': lang,
        'SITE_OPENING_HOURS': DEFAULT_HOURS.get(lang, DEFAULT_HOURS['cs']),
        'SITE_INSTAGRAM_URL': 'https://instagram.com/blackdiamondspa',
        'SITE_TELEGRAM_URL': '',
        'currency_settings': CurrencySettings(),
    }

    try:
        site = SiteSettings.load()
        from .opening_hours import ensure_hours_i18n
        ensure_hours_i18n(site)
        base.update({
            'SITE_STREET_ADDRESS': site.address.split(',')[0].strip() if site.address else 'Opletalova 1566/30',
            'SITE_POSTAL_CODE': '110 00',
            'SITE_ADDRESS_LOCALITY': 'Praha',
            'SITE_ADDRESS_COUNTRY': 'CZ',
            'SITE_ADDRESS': site.address or site.full_address,
            'SITE_PHONE': site.get_active_phone_display(),
            'SITE_PHONE_TEL': site.get_active_phone_tel(),
            'SITE_MAPS_URL': site.map_url or getattr(
                settings,
                'SITE_MAPS_URL',
                f'https://maps.google.com/?q={site.maps_query}',
            ),
            'SITE_MAPS_EMBED_URL': site.maps_embed,
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

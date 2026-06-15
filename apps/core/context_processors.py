from django.conf import settings
from django.db import DatabaseError

from .models import SiteSettings


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
    base = {
        'SITE_NAME': settings.SITE_NAME,
        'SITE_URL': settings.SITE_URL,
        'SITE_PHONE': settings.SITE_PHONE,
        'SITE_EMAIL': settings.SITE_EMAIL,
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
        })
    except DatabaseError:
        base.update(_fallback_address())

    return base

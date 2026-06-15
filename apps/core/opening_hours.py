"""Opening hours helpers — text from SiteSettings admin."""

from __future__ import annotations

from django.utils.translation import get_language

DEFAULT_HOURS = {
    'cs': 'Od 9 ráno do 4 ráno',
    'en': 'From 9 am to 4 am',
    'ru': 'С 9 утра до 4 утра',
}


def _lang_code(language_code: str | None = None) -> str:
    code = (language_code or get_language() or 'cs').split('-')[0].lower()
    return code if code in DEFAULT_HOURS else 'cs'


def get_opening_hours_display(language_code: str | None = None) -> str:
    from django.db import DatabaseError

    from .models import SiteSettings

    lang = _lang_code(language_code)
    try:
        site = SiteSettings.load()
        return site.get_hours_for_language(lang)
    except DatabaseError:
        return DEFAULT_HOURS[lang]

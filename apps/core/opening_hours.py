"""Opening hours helpers — text from SiteSettings admin."""

from __future__ import annotations

from django.utils.translation import get_language

DEFAULT_HOURS = {
    'cs': 'Denně od 9:00 do 5:00 ráno',
    'en': 'Daily from 9 AM to 5 AM',
    'ru': 'Ежедневно с 9:00 до 5:00 утра',
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
        ensure_hours_i18n(site)
        return site.get_hours_for_language(lang)
    except DatabaseError:
        return DEFAULT_HOURS[lang]


def ensure_hours_i18n(site) -> bool:
    """Fill empty EN/RU opening hours from defaults (once)."""
    updated_fields: list[str] = []
    if not (site.hours_en or '').strip():
        site.hours_en = DEFAULT_HOURS['en']
        updated_fields.append('hours_en')
    if not (site.hours_ru or '').strip():
        site.hours_ru = DEFAULT_HOURS['ru']
        updated_fields.append('hours_ru')
    if updated_fields:
        site.save(update_fields=updated_fields)
        return True
    return False

"""Core models: settings, redirects, CMS pages and interior gallery."""

from __future__ import annotations

from datetime import datetime

from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from .phone_rotation import (
    ROTATION_COUNT,
    active_index,
    format_tel_href,
    next_switch_at,
    normalize_whatsapp_digits,
    prague_now,
)


class SiteSettings(models.Model):
    """Singleton model for site-wide settings editable in admin."""

    phone_primary = models.CharField(_('Primary phone'), max_length=30, default='+420 797 669 633')
    phone_secondary = models.CharField(_('Secondary phone'), max_length=30, blank=True)
    whatsapp_number = models.CharField(
        _('WhatsApp number (no +, no spaces)'),
        max_length=20,
        default='420797669633',
        help_text=_('e.g. 420797669633 — used in wa.me/ links'),
    )
    rotation_phone_1 = models.CharField(_('Rotating phone 1'), max_length=30, default='+420 797 669 633')
    rotation_phone_2 = models.CharField(_('Rotating phone 2'), max_length=30, default='+420 777 060 456')
    rotation_phone_3 = models.CharField(_('Rotating phone 3'), max_length=30, default='+420 778 622 334')
    phone_rotation_hours = models.PositiveSmallIntegerField(
        _('Phone rotation interval (hours)'), default=2,
    )
    email = models.EmailField(_('Contact email'), default='info@blackdiamond.cz')
    address = models.CharField(
        _('Address (studio 1)'), max_length=200, default='Soukenická, 110 00 Praha 1',
    )
    location_phone_1 = models.CharField(_('Phone (studio 1)'), max_length=30, default='+420 797 669 633')
    map_url = models.URLField(_('Map URL (studio 1)'), max_length=500, blank=True)
    maps_embed_url = models.TextField(_('Google Maps embed URL (studio 1)'), blank=True)
    address_2 = models.CharField(_('Address (studio 2)'), max_length=200, blank=True)
    location_phone_2 = models.CharField(_('Phone (studio 2)'), max_length=30, blank=True)
    map_url_2 = models.URLField(_('Map URL (studio 2)'), max_length=500, blank=True)
    maps_embed_url_2 = models.TextField(_('Google Maps embed URL (studio 2)'), blank=True)
    hours = models.CharField(
        _('Opening hours (Czech — default fallback)'), max_length=100,
        default='Od 9 ráno do 4 ráno',
    )
    hours_en = models.CharField(
        _('Opening hours (English)'), max_length=100,
        blank=True, default='From 9 am to 4 am',
    )
    hours_ru = models.CharField(
        _('Opening hours (Russian)'), max_length=100,
        blank=True, default='С 9 утра до 4 утра',
    )
    instagram_url = models.URLField(_('Instagram URL'), blank=True)
    telegram_url = models.URLField(_('Telegram URL'), blank=True)
    default_meta_title = models.CharField(_('Default meta title'), max_length=200, blank=True)
    default_meta_description = models.CharField(_('Default meta description'), max_length=300, blank=True)
    og_image_url = models.URLField(_('OG image URL'), blank=True)
    require_age_confirmation = models.BooleanField(_('Require age confirmation'), default=True)
    eur_rate = models.DecimalField(_('EUR rate (1 EUR = X CZK)'), max_digits=8, decimal_places=4, default=25.0)
    usd_rate = models.DecimalField(_('USD rate (1 USD = X CZK)'), max_digits=8, decimal_places=4, default=23.0)
    show_eur = models.BooleanField(_('Show prices in EUR'), default=True)
    show_usd = models.BooleanField(_('Show prices in USD'), default=False)

    class Meta:
        verbose_name = _('Site Settings')
        verbose_name_plural = _('Site Settings')

    def __str__(self):
        return 'Site Settings'

    def clean(self):
        super().clean()
        phones = self.get_rotation_phones()
        if not all(phones):
            raise ValidationError(_('All three rotating phone numbers are required.'))
        if self.phone_rotation_hours < 1:
            raise ValidationError({'phone_rotation_hours': _('Interval must be at least 1 hour.')})

    def save(self, *args, **kwargs):
        self.pk = 1
        for field in ('rotation_phone_1', 'rotation_phone_2', 'rotation_phone_3'):
            val = getattr(self, field, '') or ''
            setattr(self, field, val.strip())
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @classmethod
    def get(cls):
        return cls.load()

    @property
    def full_address(self):
        return self.address

    @property
    def maps_query(self):
        from urllib.parse import quote_plus
        return quote_plus(self.address)

    def get_rotation_phones(self):
        return [
            (self.rotation_phone_1 or '').strip(),
            (self.rotation_phone_2 or '').strip(),
            (self.rotation_phone_3 or '').strip(),
        ]

    def get_active_phone_index(self, now: datetime | None = None) -> int:
        return active_index(now, interval_hours=self.phone_rotation_hours)

    def get_active_phone_display(self, now: datetime | None = None) -> str:
        phones = self.get_rotation_phones()
        if not all(phones):
            return (self.phone_primary or '').strip()
        return phones[self.get_active_phone_index(now)]

    def get_active_phone_tel(self, now: datetime | None = None) -> str:
        return format_tel_href(self.get_active_phone_display(now))

    def get_active_whatsapp_number(self, now: datetime | None = None) -> str:
        display = self.get_active_phone_display(now)
        digits = normalize_whatsapp_digits(display)
        if digits:
            return digits
        return normalize_whatsapp_digits(self.whatsapp_number)

    def get_rotation_preview(self, now: datetime | None = None) -> dict:
        local = prague_now(now)
        switch = next_switch_at(now, interval_hours=self.phone_rotation_hours)
        idx = self.get_active_phone_index(now)
        return {
            'active': self.get_active_phone_display(now),
            'slot': idx + 1,
            'total': ROTATION_COUNT,
            'next_switch': switch.strftime('%H:%M'),
            'prague_now': local.strftime('%Y-%m-%d %H:%M'),
        }

    def get_hours_for_language(self, language_code: str) -> str:
        code = (language_code or 'cs').split('-')[0].lower()
        if code == 'en':
            t = (self.hours_en or '').strip()
            return t if t else self.hours
        if code == 'ru':
            t = (self.hours_ru or '').strip()
            return t if t else self.hours
        return self.hours


class LegacyRedirect(models.Model):
    old_path = models.CharField(_('Old path'), max_length=500, unique=True, db_index=True)
    new_path = models.CharField(_('New path'), max_length=500, blank=True)
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Legacy Redirect')
        verbose_name_plural = _('Legacy Redirects')
        ordering = ['old_path']

    def __str__(self):
        return f'{self.old_path} → {self.new_path or "/"}'


class ContentPage(models.Model):
    class PageKey(models.TextChoices):
        PRIVACY = 'privacy', _('Privacy Policy')
        FIRST_VISIT = 'first_visit', _('First Visit')
        PRICES = 'prices', _('Price list')
        JOBS = 'jobs', _('Jobs')

    page_key = models.CharField(_('Page'), max_length=32, choices=PageKey.choices, unique=True)
    body_cs = models.TextField(_('Body (Czech, HTML)'), blank=True)
    body_en = models.TextField(_('Body (English, HTML)'), blank=True)
    body_ru = models.TextField(_('Body (Russian, HTML)'), blank=True)
    hero_sub_cs = models.CharField(_('Hero subtitle (Czech)'), max_length=300, blank=True)
    hero_sub_en = models.CharField(_('Hero subtitle (English)'), max_length=300, blank=True)
    hero_sub_ru = models.CharField(_('Hero subtitle (Russian)'), max_length=300, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Page Content')
        verbose_name_plural = _('Page Content')
        ordering = ['page_key']

    def __str__(self):
        return self.get_page_key_display()


class InteriorImage(models.Model):
    cloudinary_image = models.ForeignKey(
        'media_library.CloudinaryImage',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Cloudinary image'),
        related_name='interior_usages',
    )
    image = models.ImageField(_('Uploaded image'), upload_to='interior/', blank=True)
    static_path = models.CharField(_('Static file path'), max_length=255, blank=True)
    alt_cs = models.CharField(_('Alt text (Czech)'), max_length=300, blank=True)
    alt_en = models.CharField(_('Alt text (English)'), max_length=300, blank=True)
    alt_ru = models.CharField(_('Alt text (Russian)'), max_length=300, blank=True)
    sort_order = models.PositiveIntegerField(_('Sort order'), default=0, db_index=True)
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Interior photo')
        verbose_name_plural = _('Interior photos')
        ordering = ['sort_order', 'pk']

    def __str__(self):
        return (self.alt_cs or self.static_path or str(self.pk))[:80]

    def get_image_url(self) -> str:
        if self.cloudinary_image_id:
            return self.cloudinary_image.gallery_url
        if self.image:
            return self.image.url
        if self.static_path:
            return staticfiles_storage.url(self.static_path)
        return ''


class GuestReview(models.Model):
    text_cs = models.TextField(_('Review (Czech)'))
    text_en = models.TextField(_('Review (English)'), blank=True)
    text_ru = models.TextField(_('Review (Russian)'), blank=True)
    author_label = models.CharField(_('Author'), max_length=40)
    city = models.CharField(_('City'), max_length=80, blank=True)
    google_review_id = models.CharField(_('Google review ID'), max_length=120, blank=True, null=True, unique=True)
    rating = models.PositiveSmallIntegerField(_('Rating'), null=True, blank=True)
    order = models.IntegerField(_('Order'), default=0)
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Guest review')
        verbose_name_plural = _('Guest reviews')
        ordering = ['order', 'pk']

    def __str__(self):
        return f'{self.author_label} — {self.text_cs[:60]}'


class EtiquetteRule(models.Model):
    class Category(models.TextChoices):
        BEHAVIOR = 'behavior', _('Behavior')
        HYGIENE = 'hygiene', _('Hygiene')
        PRIVACY = 'privacy', _('Privacy')
        BOOKING = 'booking', _('Booking & Cancellation')

    category = models.CharField(_('Category'), max_length=20, choices=Category.choices)
    rule_cs = models.TextField(_('Rule (Czech)'))
    rule_en = models.TextField(_('Rule (English)'), blank=True)
    rule_ru = models.TextField(_('Rule (Russian)'), blank=True)
    order = models.PositiveSmallIntegerField(_('Order'), default=0)
    is_active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('Etiquette rule')
        verbose_name_plural = _('Etiquette rules')
        ordering = ['category', 'order']

    def __str__(self):
        return f'[{self.get_category_display()}] {self.rule_cs[:60]}'

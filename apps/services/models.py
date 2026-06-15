from django.db import models
from django.utils.translation import gettext_lazy as _


class Language(models.Model):
    code = models.CharField(_('ISO code'), max_length=5, unique=True)
    name = models.CharField(_('Name'), max_length=50)
    flag_emoji = models.CharField(_('Flag emoji'), max_length=10, blank=True)
    order = models.IntegerField(_('Order'), default=0)

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')
        ordering = ['order', 'name']

    def __str__(self):
        return f'{self.flag_emoji} {self.name}'.strip()


class HashTag(models.Model):
    slug = models.SlugField(unique=True)
    label_cs = models.CharField(_('Label (CS)'), max_length=50)
    label_en = models.CharField(_('Label (EN)'), max_length=50, blank=True)
    label_ru = models.CharField(_('Label (RU)'), max_length=50, blank=True)
    order = models.IntegerField(_('Order'), default=0)

    class Meta:
        verbose_name = _('HashTag')
        verbose_name_plural = _('HashTags')
        ordering = ['order', 'slug']

    def __str__(self):
        return self.label_cs or self.slug


class Service(models.Model):
    slug = models.SlugField(unique=True, max_length=80)
    icon = models.CharField(_('Icon ID (SVG sprite)'), max_length=50, blank=True)

    title_cs = models.CharField(max_length=120)
    title_en = models.CharField(max_length=120, blank=True)
    title_ru = models.CharField(max_length=120, blank=True)

    short_cs = models.CharField(max_length=200, blank=True)
    short_en = models.CharField(max_length=200, blank=True)
    short_ru = models.CharField(max_length=200, blank=True)

    description_cs = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    description_ru = models.TextField(blank=True)

    what_cs = models.TextField(_('What is it (CS)'), blank=True)
    what_en = models.TextField(_('What is it (EN)'), blank=True)
    what_ru = models.TextField(_('What is it (RU)'), blank=True)

    who_cs = models.TextField(_('Who is it for (CS)'), blank=True)
    who_en = models.TextField(_('Who is it for (EN)'), blank=True)
    who_ru = models.TextField(_('Who is it for (RU)'), blank=True)

    faq_cs = models.JSONField(_('FAQ (CS)'), default=list, blank=True)
    faq_en = models.JSONField(_('FAQ (EN)'), default=list, blank=True)
    faq_ru = models.JSONField(_('FAQ (RU)'), default=list, blank=True)

    meta_title_cs = models.CharField(_('Meta title (CS)'), max_length=200, blank=True)
    meta_title_en = models.CharField(_('Meta title (EN)'), max_length=200, blank=True)
    meta_title_ru = models.CharField(_('Meta title (RU)'), max_length=200, blank=True)
    meta_description_cs = models.CharField(_('Meta description (CS)'), max_length=300, blank=True)
    meta_description_en = models.CharField(_('Meta description (EN)'), max_length=300, blank=True)
    meta_description_ru = models.CharField(_('Meta description (RU)'), max_length=300, blank=True)

    hero_image_url = models.URLField(_('Hero image URL'), blank=True)
    hero_image = models.ImageField(_('Hero image (local)'), upload_to='services/heroes/', blank=True)
    image = models.ImageField(upload_to='services/', blank=True)

    duration = models.PositiveIntegerField(help_text=_('Тривалість у хвилинах'), default=60)
    price = models.DecimalField(max_digits=8, decimal_places=0, default=0)
    base_price_czk = models.PositiveIntegerField(_('Base price (CZK)'), default=0)
    base_duration_min = models.PositiveSmallIntegerField(_('Base duration (min)'), default=60)

    is_active = models.BooleanField(default=True)
    is_extra = models.BooleanField(_('Is extra service'), default=False)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'pk']
        verbose_name = _('Масаж')
        verbose_name_plural = _('Масажі')

    def __str__(self):
        return self.title_cs

    def get_title(self, lang='cs'):
        return getattr(self, f'title_{lang}', self.title_cs) or self.title_cs

    def get_description(self, lang='cs'):
        return getattr(self, f'description_{lang}', self.description_cs) or self.description_cs

    def get_what(self, lang='cs'):
        code = (lang or 'cs').split('-')[0].lower()
        value = getattr(self, f'what_{code}', '') or self.what_cs
        return value

    def get_who(self, lang='cs'):
        code = (lang or 'cs').split('-')[0].lower()
        value = getattr(self, f'who_{code}', '') or self.who_cs
        return value

    def get_faq(self, lang='cs'):
        code = (lang or 'cs').split('-')[0].lower()
        items = getattr(self, f'faq_{code}', None) or self.faq_cs
        return items if isinstance(items, list) else []


class Price(models.Model):
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name='prices', verbose_name=_('Service'),
    )
    duration_min = models.PositiveSmallIntegerField(_('Duration (minutes)'))
    price_czk = models.PositiveIntegerField(_('Price (CZK)'))
    is_highlighted = models.BooleanField(_('Highlight (best value)'), default=False)
    note_cs = models.CharField(_('Note (CS)'), max_length=100, blank=True)
    note_en = models.CharField(_('Note (EN)'), max_length=100, blank=True)

    class Meta:
        verbose_name = _('Price')
        verbose_name_plural = _('Prices')
        ordering = ['service__order', 'duration_min']
        unique_together = [('service', 'duration_min')]

    def __str__(self):
        return f'{self.service} — {self.duration_min} min — {self.price_czk} Kč'


class Extra(models.Model):
    slug = models.SlugField(unique=True)
    name_cs = models.CharField(_('Name (CS)'), max_length=100)
    name_en = models.CharField(_('Name (EN)'), max_length=100, blank=True)
    name_ru = models.CharField(_('Name (RU)'), max_length=100, blank=True)
    price_czk = models.PositiveIntegerField(_('Price (CZK)'), default=0)
    price_note_cs = models.CharField(_('Price note (CS)'), max_length=100, blank=True)
    price_note_en = models.CharField(_('Price note (EN)'), max_length=100, blank=True)
    order = models.IntegerField(_('Order'), default=0)
    is_active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('Extra Service')
        verbose_name_plural = _('Extra Services')
        ordering = ['order', 'slug']

    def __str__(self):
        return self.name_cs or self.slug

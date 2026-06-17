from django.db import models
from django.utils.translation import gettext_lazy as _


class Therapist(models.Model):
    slug = models.SlugField(unique=True, max_length=60)
    name = models.CharField(max_length=80)
    hub_slug = models.SlugField(
        max_length=80,
        blank=True,
        db_index=True,
        help_text="Slug масажистки на tantra-prague.com (для синхронізації розкладу)",
    )
    sort_order = models.IntegerField(_('Sort order'), default=0, db_index=True)

    is_active = models.BooleanField(default=True)
    has_location = models.BooleanField(_('Currently at location'), default=True)
    is_busy = models.BooleanField(_('Show as busy'), default=False)
    has_schedule = models.BooleanField(_('Has schedule entry today'), default=False)
    is_new = models.BooleanField(_('New therapist badge'), default=False)

    age = models.PositiveSmallIntegerField(_('Age'), null=True, blank=True)
    height_cm = models.PositiveSmallIntegerField(_('Height (cm)'), null=True, blank=True)
    weight_kg = models.PositiveSmallIntegerField(_('Weight (kg)'), null=True, blank=True)
    bust = models.CharField(_('Bust'), max_length=10, blank=True)

    bio_cs = models.TextField(blank=True)
    bio_en = models.TextField(blank=True)
    bio_ru = models.TextField(blank=True)
    loves_text_cs = models.TextField(_('Loves / personality (CS)'), blank=True)
    loves_text_en = models.TextField(_('Loves / personality (EN)'), blank=True)
    loves_text_ru = models.TextField(_('Loves / personality (RU)'), blank=True)
    use_default = models.BooleanField(_('Use default language content'), default=False)

    main_cloudinary_photo = models.ForeignKey(
        'media_library.CloudinaryImage',
        null=True, blank=True, on_delete=models.SET_NULL,
        related_name='therapist_main', verbose_name=_('Main photo (library)'),
    )
    gallery_cloudinary = models.ManyToManyField(
        'media_library.CloudinaryImage', blank=True,
        related_name='therapist_gallery', verbose_name=_('Gallery (library)'),
    )

    photo = models.ImageField(upload_to='masseuses/', blank=True)
    main_photo_url = models.URLField(_('Main photo URL (external)'), blank=True)
    gallery_urls = models.TextField(_('Gallery image URLs (legacy)'), blank=True)

    specialties = models.ManyToManyField(
        'services.Service', blank=True, related_name='therapists',
    )
    offers = models.ManyToManyField(
        'services.Service', blank=True, related_name='therapists_offers',
        verbose_name=_('Offers'),
    )
    loves = models.ManyToManyField(
        'services.Service', blank=True, related_name='therapists_loves',
        verbose_name=_('Loves'),
    )
    extras = models.ManyToManyField(
        'services.Extra', blank=True, verbose_name=_('Extra services'),
    )
    hashtags = models.ManyToManyField(
        'services.HashTag', blank=True, verbose_name=_('Hashtags / characteristics'),
    )
    languages = models.ManyToManyField(
        'services.Language', blank=True, verbose_name=_('Languages spoken'),
    )
    branches = models.ManyToManyField(
        'branches.Branch', blank=True, verbose_name=_('Branches'),
    )

    tagline_cs = models.CharField(_('Tagline (CS)'), max_length=120, blank=True)
    tagline_en = models.CharField(_('Tagline (EN)'), max_length=120, blank=True)
    tagline_ru = models.CharField(_('Tagline (RU)'), max_length=120, blank=True)

    faq_cs = models.JSONField(_('FAQ (CS)'), default=list, blank=True)
    faq_en = models.JSONField(_('FAQ (EN)'), default=list, blank=True)
    faq_ru = models.JSONField(_('FAQ (RU)'), default=list, blank=True)

    meta_title = models.CharField(_('Meta title (legacy)'), max_length=200, blank=True)
    meta_description = models.CharField(_('Meta description (legacy)'), max_length=300, blank=True)
    meta_title_cs = models.CharField(_('Meta title (CS)'), max_length=200, blank=True)
    meta_title_en = models.CharField(_('Meta title (EN)'), max_length=200, blank=True)
    meta_title_ru = models.CharField(_('Meta title (RU)'), max_length=200, blank=True)
    meta_description_cs = models.CharField(_('Meta description (CS)'), max_length=300, blank=True)
    meta_description_en = models.CharField(_('Meta description (EN)'), max_length=300, blank=True)
    meta_description_ru = models.CharField(_('Meta description (RU)'), max_length=300, blank=True)

    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name = _('Масажистка')
        verbose_name_plural = _('Масажистки')

    def __str__(self):
        return self.name

    def get_bio(self, lang='cs'):
        return getattr(self, f'bio_{lang}', self.bio_cs) or self.bio_cs

    def get_faq(self, lang='cs'):
        code = (lang or 'cs').split('-')[0].lower()
        items = getattr(self, f'faq_{code}', None) or self.faq_cs
        return items if isinstance(items, list) else []

    @property
    def photo_url(self):
        if self.main_cloudinary_photo_id:
            return self.main_cloudinary_photo.card_url
        if self.photo:
            return self.photo.url
        return self.main_photo_url or ''

    @property
    def card_photo_url(self) -> str:
        """URL for list/detail media-gallery (Cloudinary, upload, or static fallback)."""
        if self.photo_url:
            return self.photo_url
        from django.templatetags.static import static
        return static(f'img/masseuses/{self.slug}.webp')

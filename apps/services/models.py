from django.db import models
from django.utils.translation import gettext_lazy as _


class Service(models.Model):
    slug = models.SlugField(unique=True, max_length=80)

    title_cs = models.CharField(max_length=120)
    title_en = models.CharField(max_length=120)
    title_ru = models.CharField(max_length=120)

    short_cs = models.CharField(max_length=200, blank=True)
    short_en = models.CharField(max_length=200, blank=True)
    short_ru = models.CharField(max_length=200, blank=True)

    description_cs = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    description_ru = models.TextField(blank=True)

    duration = models.PositiveIntegerField(
        help_text=_('Тривалість у хвилинах'), default=60
    )
    price = models.DecimalField(max_digits=8, decimal_places=0)
    image = models.ImageField(upload_to='services/', blank=True)

    is_active = models.BooleanField(default=True)
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

from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.services.models import Service


class Therapist(models.Model):
    slug = models.SlugField(unique=True, max_length=60)
    name = models.CharField(max_length=80)
    photo = models.ImageField(upload_to='masseuses/', blank=True)

    bio_cs = models.TextField(blank=True)
    bio_en = models.TextField(blank=True)
    bio_ru = models.TextField(blank=True)

    specialties = models.ManyToManyField(
        Service, blank=True, related_name='therapists'
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = _('Масажистка')
        verbose_name_plural = _('Масажистки')

    def __str__(self):
        return self.name

    def get_bio(self, lang='cs'):
        return getattr(self, f'bio_{lang}', self.bio_cs) or self.bio_cs

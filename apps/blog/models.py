from django.db import models
from django.utils.translation import gettext_lazy as _


class Article(models.Model):
    slug = models.SlugField(unique=True, max_length=100)

    title_cs = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, blank=True)
    title_ru = models.CharField(max_length=200, blank=True)

    body_cs = models.TextField()
    body_en = models.TextField(blank=True)
    body_ru = models.TextField(blank=True)

    meta_description_cs = models.CharField(max_length=160, blank=True)
    meta_description_en = models.CharField(max_length=160, blank=True)
    meta_description_ru = models.CharField(max_length=160, blank=True)

    image = models.ImageField(upload_to='blog/', blank=True)
    published_at = models.DateTimeField()
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-published_at']
        verbose_name = _('Стаття')
        verbose_name_plural = _('Статті')

    def __str__(self):
        return self.title_cs

    def get_title(self, lang='cs'):
        return getattr(self, f'title_{lang}', self.title_cs) or self.title_cs

    def get_body(self, lang='cs'):
        return getattr(self, f'body_{lang}', self.body_cs) or self.body_cs

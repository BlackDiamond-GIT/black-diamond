from django.db import models
from django.utils.translation import gettext_lazy as _
from urllib.parse import quote_plus


class SiteSettings(models.Model):
    street_name = models.CharField(_('Вулиця'), max_length=120, default='Soukenická')
    street_number = models.CharField(_('Номер будинку'), max_length=20, blank=True, default='')
    postal_code = models.CharField(_('Поштовий індекс'), max_length=20, default='110 00')
    city = models.CharField(_('Місто'), max_length=80, default='Praha 1')
    country_code = models.CharField(_('Код країни'), max_length=2, default='CZ')

    class Meta:
        verbose_name = _('Налаштування сайту')
        verbose_name_plural = _('Налаштування сайту')

    def __str__(self):
        return self.full_address

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def street_address(self):
        number = self.street_number.strip()
        if number:
            return f'{self.street_name} {number}'
        return self.street_name

    @property
    def full_address(self):
        return f'{self.street_address}, {self.postal_code} {self.city}'

    @property
    def maps_query(self):
        return quote_plus(f'{self.street_address}, {self.postal_code} {self.city}')

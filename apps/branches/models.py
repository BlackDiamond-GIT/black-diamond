from django.db import models
from django.utils.translation import gettext_lazy as _


class Branch(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    address = models.CharField(_('Address'), max_length=200)
    phone = models.CharField(_('Phone'), max_length=30, blank=True)
    is_active = models.BooleanField(_('Active'), default=True)
    order = models.IntegerField(_('Order'), default=0)

    class Meta:
        verbose_name = _('Branch')
        verbose_name_plural = _('Branches')
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

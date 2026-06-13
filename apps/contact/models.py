from django.db import models
from django.utils.translation import gettext_lazy as _


class ContactRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    service = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Запит')
        verbose_name_plural = _('Запити контактів')

    def __str__(self):
        return f'{self.name} <{self.email}> — {self.created_at:%d.%m.%Y %H:%M}'

from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.therapists.models import Therapist
from apps.services.models import Service


class TimeSlot(models.Model):
    STATUS_FREE = 'free'
    STATUS_BUSY = 'busy'
    STATUS_SOON = 'soon'
    STATUS_CHOICES = [
        (STATUS_FREE, _('Вільно')),
        (STATUS_BUSY, _('Зайнято')),
        (STATUS_SOON, _('Скоро')),
    ]

    therapist = models.ForeignKey(
        Therapist, on_delete=models.CASCADE, related_name='slots'
    )
    service = models.ForeignKey(
        Service, on_delete=models.SET_NULL, null=True, blank=True
    )
    date = models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField()
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=STATUS_FREE
    )

    class Meta:
        ordering = ['date', 'time_start']
        unique_together = [('therapist', 'date', 'time_start')]
        verbose_name = _('Слот')
        verbose_name_plural = _('Слоти розкладу')

    def __str__(self):
        return f'{self.therapist.name} — {self.date} {self.time_start}'
